# pipreqs — Generate requirements.txt from actual imports

원문: https://github.com/bndr/pipreqs

## Description
"pipreqs - Generate pip requirements.txt file based on imports of any project."

## Installation
```
pip install pipreqs
```

## Usage
```
pipreqs [options] [<path>]
```

Key options:
- `--use-local`: use only local package info
- `--pypi-server <url>`: custom PyPI server
- `--ignore <dirs>`: exclude directories
- `--savepath <file>`: write requirements to a specific file
- `--print`: print to stdout instead of writing a file
- `--force`: overwrite existing requirements.txt
- `--diff <file>`: compare current requirements against project imports
- `--clean <file>`: remove unused modules from requirements.txt
- `--mode <scheme>`: versioning scheme (compat, gt, non-pin)
- `--scan-notebooks`: include Jupyter notebooks

## Example
```
$ pipreqs /home/project/location
Successfully saved requirements file in /home/project/location/requirements.txt
```

## Why not `pip freeze`?
- Captures only the packages the project actually imports, not every package installed in the environment
- Works without pre-installing the project first
- Useful for generating requirements.txt for a new/undocumented project — exactly the situation our Dependency Collector will face when scanning an arbitrary AI agent repo that has no clean requirements.txt
