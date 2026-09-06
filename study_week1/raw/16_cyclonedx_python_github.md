# cyclonedx-python — SBOM generator (GitHub README)

원문: https://github.com/CycloneDX/cyclonedx-python

## Overview
"Probably the most accurate, complete SBOM generator for any python-related projects." Generates SBOM documents in OWASP CycloneDX format.

## Supported Data Sources
- Python (virtual) environments
- Poetry manifest and lockfile
- Pipenv manifest and lockfile
- Pip's requirements.txt format
- PDM and uv virtual environments (indirect)
- Conda environments (indirect, v4+)

## Requirements
Python `>=3.9,<4` (older tool versions support `>=2.7`).

## Installation
```
python -m pip install cyclonedx-bom
pipx install cyclonedx-bom
poetry add cyclonedx-bom
uv tool install cyclonedx-bom
```

## Usage Commands
```
cyclonedx-py environment (env, venv)   # from Python environment
cyclonedx-py requirements              # from Pip requirements.txt
cyclonedx-py pipenv                    # from Pipenv manifest
cyclonedx-py poetry                    # from Poetry project
```
Alternative invocation: `python3 -m cyclonedx_py`

## Notes
No public API is exposed — CLI only, internal code may change without notice. License: Apache 2.0 (OWASP Foundation).
