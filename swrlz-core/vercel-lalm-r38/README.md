# §wyrlz LALM R38 — Vercel Python bootstrap

This directory is the deployable Python/Vercel bootstrap for `SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.§wyrlzx`.

## Current verified boundary

- The exact 233,640,424-byte R38 artifact is preserved losslessly inside the root `swrlz-core/SWYRLZ_VERCEL_LALM_R38_BOOTSTRAP.zip` bundle.
- Raw SHA-256: `e6732c7875f7689019b7e051675f5b4b5a901af4fe4d52f8a1fcadafec3229e7`
- Packed model SHA-256: `e57528fc34fa317fdabb67708107e0bebff864f5d9451436b70d24b11e2ac505`
- On cold start the API downloads the existing bootstrap ZIP from this repository, extracts the packed R38 model to `/tmp`, then expands it byte-for-byte.
- Python discovers the native `SXI1` integrity table and recovers integrity-bound JSON sections.
- `/api/health`, `/api/model`, and `/api/sections` are the current infrastructure verification endpoints.
- `/api/generate` intentionally returns HTTP 501 until the current R38 tokenizer/tensor/operator executor is ported. No fake inference is substituted.

## Vercel settings

- Application Preset: `Python`
- Root Directory: `swrlz-core/vercel-lalm-r38`
- Build Command: default
- Output Directory: default / N/A
- Install Command: default
- Environment Variables: none required for the bootstrap

Optional override: `SWYRLZ_BOOTSTRAP_URL` may point at another compatible bootstrap ZIP.

### Live admin workbench upload authentication

The live admin file explorer at `/api/admin` supports phone-to-SERVER uploads into `/tmp/swrlz-admin` and its subdirectories. Uploads use resumable 2 MiB browser chunks and server-side atomic finalization. To arm that write path, configure a private Vercel environment variable named `SWRLZ_ADMIN_TOKEN`, redeploy once, and enter the same value in the workbench `SWRLZ_ADMIN_TOKEN` field. The browser keeps it only in `sessionStorage`.

The upload route is intentionally disabled when `SWRLZ_ADMIN_TOKEN` is absent. `/tmp` remains Vercel instance-local and ephemeral, so a runtime recycle can invalidate an in-progress upload; the workbench detects a changed instance and fails the transfer instead of silently assembling chunks across different instances.

## Endpoints

- `GET /`
- `GET /api/health`
- `GET /api/model`
- `GET /api/sections`
- `GET /api/admin`
- `POST /api/admin?action=upload-init|upload-chunk|upload-finish|upload-cancel`
- `POST /api/generate`
- `POST /api/generate/stream`

The next implementation rung is the real R38 native tokenizer + tensor directory + LFM2 operator execution path under the stable `R38Backend` interface.
