# requirements-parser (PyPI)

원문: https://pypi.org/project/requirements-parser/

**requirements-parser** is a Python module for parsing Pip requirement files, currently at version 0.13.1.

## Core Description
The project aims to "parse everything in the Pip requirement file format spec." It handles both file-like objects and text strings as input sources.

## Installation
```
pip install requirements-parser
poetry add requirements-parser
```

## Supported Features
- Editables (git URLs)
- Version control URIs
- Egg hashes and subdirectories
- Extras notation
- URLs

## Basic Usage Example
```python
import requirements
with open('requirements.txt', 'r') as fd:
    for req in requirements.parse(fd):
        print(req.name, req.specs)
```

## Technical Details
- Current Version: 0.13.1 (released June 18, 2026)
- Python Support: 3.8 through 3.14
- Status: Production/Stable
- License: Apache 2.0
- Maintainers: Paul Horton (@madpah), David Fischer (@davidfischer)
