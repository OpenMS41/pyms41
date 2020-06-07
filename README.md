# pyms41

Simple python library and CLI utility for common MS41 ECU flashing tasks.

```sh
% ms41-util    
Usage: ms41-util [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  rom  Utilities for working with MS41 ECU rom and .bin files
  vin  Convert VIN between hex/ascii
```

## Install
This repository is under heavy development, to keep up-to-date the recommended approach is to clone the repository and use `pip` to do a symlink install.
```sh
git clone https://github.com/OpenMS41/pyms41.git && cd pyms41
pip install -e .
```

To update to the latest simply run `git pull` and `ms41-util` and `pyms41` library will be updated without further steps.
