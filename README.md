# Syncthing updater
Syncthing v1.x has `syncthing serve -u`, which upgrades the binary without loading syncthing itself.

Syncthing v2.x auto upgrade requires the syncthing service to be able to write the binary. If you have syncthing in `/usr/bin/` you either have to boot the syncthing server as root or manually replace the binary.

This script is a replacement for the old auto upgrade on syncthing v2.x.
# Installation
This script requires `requests` and `packaging` to work. Additionally, you can install `tqdm` to have a download progress bar (or avoid it using `--no-tqdm`)

You can either install the dependencies on a virtual enviroment or install them as `python3-requests python3-packaging python3-tqdm` on ubuntu (probably debian) based distros.

# Configuration
The available options are very straightforward.
- `bin_path` is the path to the syncthing binary.
- `upgrade_url` is the url of the syncthing upgrade server, don't change it unless you know what you're doing.
- `architecture` is the version of syncthing to download. It works by getting the first version that has the text in this field, so if you have a linux pc either `syncthing-linux-amd64` and `linux-amd64` will work.

You can either copy and fill `config_sample.json` or run the interactive config generator `gen-config.py`.
# Usage
```
$ python3 main.py -h
usage: main.py [-h] [-c CONFIG] [--force] [--dry-run] [--no-tqdm]

A script for syncthing v2.x that mimics the syncthing v1.x auto upgrade from cli

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the json config file
  --force               Replace the binary without checking the version
  --dry-run             Do not replace the binary
  --no-tqdm             Disable the download progress bar, tqdm is not required if this option is used
```
# Install and or update v1.x syncthing
By using the `--force` option, you can install syncthing or update syncthing from v1.x to v2.x. If you try to update syncthing v1.x without this option, the script will crash.
