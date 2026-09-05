from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import gzip, hashlib, json, mmap, os, struct
from typing import Any

INTEGRITY_MAGIC = b"SXI1"

@dataclass(frozen=True)
class SectionHit:
    section_id: int
    offset: int
    stored_length: int
    sha256: str
    json_keys: tuple[str, ...]

class R38Container:
    """
    Read-only inspector for the supplied §wyrlzx R38 artifact.

    Uses a read-only mmap so serverless Gate 5 inspection does not duplicate the
    ~223 MiB raw model in Python heap memory. The mapping is demand-paged by the OS.
    This class NEVER rewrites the model.
    """
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._file = self.path.open("rb")
        self._map = mmap.mmap(self._file.fileno(), 0, access=mmap.ACCESS_READ)
        self.root_digest: str | None = None
        self.integrity_offset: int | None = None
        self.section_hashes: dict[int, str] = {}
        self.section_hits: dict[int, SectionHit] = {}
        try:
            self._load_index()
        except Exception:
            self.close()
            raise

    @property
    def bytes(self):
        # Compatibility boundary for existing parser code. This is an mmap, not a
        # copied bytes object; find/index/slicing behave like bytes for our usage.
        return self._map

    def close(self) -> None:
        try:
            self._map.close()
        except Exception:
            pass
        try:
            self._file.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def __del__(self):
        self.close()

    @staticmethod
    def expand_gzip(src: str | Path, dst: str | Path) -> Path:
        src, dst = Path(src), Path(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            return dst
        tmp = dst.with_suffix(dst.suffix + ".tmp")
        with gzip.open(src, "rb") as fi, tmp.open("wb") as fo:
            while True:
                chunk = fi.read(1024 * 1024)
                if not chunk:
                    break
                fo.write(chunk)
        os.replace(tmp, dst)
        return dst

    def _load_index(self) -> None:
        data = self.bytes
        pos = data.find(INTEGRITY_MAGIC)
        if pos < 0:
            raise ValueError("SXI1 integrity section not found")
        if pos + 40 > len(data):
            raise ValueError("Truncated SXI1 integrity header")
        self.integrity_offset = pos
        self.root_digest = data[pos+4:pos+36].hex()
        count = struct.unpack_from("<I", data, pos+36)[0]
        p = pos + 40
        for _ in range(count):
            if p + 36 > len(data):
                raise ValueError("Truncated SXI1 record table")
            section_id = struct.unpack_from("<I", data, p)[0]
            digest = data[p+4:p+36].hex()
            self.section_hashes[section_id] = digest
            p += 36
        self._discover_json_sections()

    def _discover_json_sections(self) -> None:
        data = self.bytes
        digest_to_id = {v:k for k,v in self.section_hashes.items()}
        i = 0
        n = len(data)
        while i < n - 2:
            j = data.find(b'{"', i)
            if j < 0:
                break
            if j == 0 or data[j-1] == 0:
                end = data.find(b"\0", j)
                if end > j:
                    blob = data[j:end]
                    digest = hashlib.sha256(blob).hexdigest()
                    sid = digest_to_id.get(digest)
                    if sid is not None:
                        keys: tuple[str,...] = ()
                        try:
                            obj = json.loads(blob.decode("utf-8"))
                            if isinstance(obj, dict):
                                keys = tuple(obj.keys())
                        except Exception:
                            pass
                        self.section_hits[sid] = SectionHit(
                            section_id=sid, offset=j, stored_length=len(blob),
                            sha256=digest, json_keys=keys
                        )
            i = j + 2

    def section_json(self, section_id: int) -> dict[str, Any]:
        hit = self.section_hits.get(section_id)
        if hit is None:
            raise KeyError(f"Section {section_id} is not a directly recovered JSON section")
        blob = self.bytes[hit.offset:hit.offset+hit.stored_length]
        obj = json.loads(blob.decode("utf-8"))
        if not isinstance(obj, dict):
            raise ValueError(f"Section {section_id} is not a JSON object")
        return obj

    def summary(self) -> dict[str, Any]:
        lineage = self.section_json(10) if 10 in self.section_hits else {}
        generation = self.section_json(7) if 7 in self.section_hits else {}
        source_map = self.section_json(20) if 20 in self.section_hits else {}
        quant = self.section_json(6) if 6 in self.section_hits else {}
        return {
            "path": str(self.path),
            "sizeBytes": self.path.stat().st_size,
            "rootDigestSha256": self.root_digest,
            "integrityRecordCount": len(self.section_hashes),
            "recoveredJsonSectionCount": len(self.section_hits),
            "artifactRevision": lineage.get("artifactRevision"),
            "generation": lineage.get("generation"),
            "modelId": lineage.get("modelId"),
            "legacyModelId": lineage.get("legacyModelId"),
            "genesisTensorPayloadSha256": lineage.get("genesisTensorPayloadSha256"),
            "genesisTensorPayloadMutated": lineage.get("genesisTensorPayloadMutated"),
            "quantization": quant.get("tensorTypeHistogram"),
            "baseSource": source_map.get("source"),
            "generationProfile": {
                "bosTokenId": generation.get("bosTokenId"),
                "eosTokenId": generation.get("eosTokenId"),
                "padTokenId": generation.get("padTokenId"),
                "repetitionPenalty": generation.get("repetitionPenalty"),
            },
        }

    def section_catalog(self) -> list[dict[str, Any]]:
        out=[]
        for sid, digest in sorted(self.section_hashes.items()):
            hit=self.section_hits.get(sid)
            out.append({
                "sectionId": sid,
                "sha256": digest,
                "recovered": hit is not None,
                "offset": hit.offset if hit else None,
                "storedLength": hit.stored_length if hit else None,
                "jsonKeys": list(hit.json_keys[:20]) if hit else [],
            })
        return out
