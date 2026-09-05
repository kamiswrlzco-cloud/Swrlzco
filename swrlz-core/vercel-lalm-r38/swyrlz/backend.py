from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import threading

from .container import R38Container

@dataclass
class GenerationConfig:
    max_tokens: int = 64
    temperature: float = 0.7
    top_p: float = 0.95

class R38Backend:
    """
    Backend boundary for the Python port.

    The supplied R38 artifact is structurally loadable and integrity-indexed.
    The remaining work for true generation is the native R38 section-1..5
    decoder/operator executor port. We intentionally fail closed here rather
    than pretending metadata inspection is inference.
    """
    def __init__(self, model_path: str | Path):
        self.model_path = Path(model_path)
        self.container = R38Container(self.model_path)
        self._lock = threading.Lock()

    @property
    def ready(self) -> bool:
        return False

    def model_info(self):
        info = self.container.summary()
        info["containerVerified"] = True
        info["graphReady"] = False
        info["interactiveReady"] = False
        info["backend"] = "R38_PYTHON_PORT_BOOTSTRAP"
        return info

    def generate(self, prompt: str, cfg: GenerationConfig) -> str:
        raise RuntimeError(
            "R38_PYTHON_NEURAL_BACKEND_PENDING: container/integrity load is working, "
            "but the R38 native tokenizer + tensor-directory + operator executor still "
            "must be ported before this endpoint may claim real LALM generation."
        )

    def stream(self, prompt: str, cfg: GenerationConfig) -> Iterable[str]:
        text = self.generate(prompt, cfg)
        yield text
