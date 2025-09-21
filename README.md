# Syncthing updater
Syncthing v1.x has `syncthing serve -u`, which upgrades the binary without loading syncthing itself.

Syncthing v2.x auto upgrade requires the syncthing service to be able to write the binary. If you have syncthing in `/usr/bin/` you either have to boot the syncthing server as root or manually replace the binary.

This script brings back the old auto upgrade to syncthing v2.x.
# Installation
### For windows users
This script right now does not (and probably will never) support the `.zip` files used to distribute windows binaries of syncthing.
> Just use [GermanCoding's synctrayzor](https://github.com/GermanCoding/SyncTrayzor).
### Getting the code
Download the [ZIP with the latest changes](https://github.com/Omicron166/syncthing-updater/archive/refs/heads/master.zip) and unzip it

or

Clone the repo with git:
```
git clone https://github.com/Omicron166/syncthing-updater.git
```
### Installing dependencies
This script requires `requests` and `packaging` to work. Additionally, you can install `tqdm` to have a download progress bar (or avoid it using `--no-tqdm`)

You can either install the dependencies on a virtual enviroment or install them as `python3-requests python3-packaging python3-tqdm` on debian based distros.

# Configuration
The available options are very straightforward.
- `bin_path` is the path to the syncthing binary.
- `upgrade_url` is the url of the syncthing upgrade server, don't change it unless you know what you're doing.
- `architecture` is the version of syncthing to download. Run `list-architectures.py` and select yours.
- `download_prereleases` indicates if you want to download syncthing prereleases (true) or just the stable releases (false)
- `download_path` is the path where temporal files will be stored.
- `download_cleaning` indicates if you want to remove (true) or keep (false) the temporal files after upgrading syncthing.

You can either copy and fill `config_sample.json` or run the interactive config generator `gen-config.py`.
# Usage
```
$ python3 main.py -h
usage: main.py [-h] [-c CONFIG] [--force] [--dry-run] [--no-tqdm]

A script for syncthing v2.x that mimics the syncthing v1.x auto upgrade from cli

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the json config file (config.json by default)
  --force               Replace the binary without checking the version
  --dry-run             Do not replace the binary
  --no-tqdm             Disable the download progress bar, tqdm is not required if this option is used
```
# Install syncthing or update from v1.x
By using the `--force` option, you can install syncthing, reinstall it if you forgot to change the settings and got the amd64 version on a raspberry pi or update syncthing from v1.x to v2.x. If you try to update syncthing v1.x without this option, the script will crash.
# Tested systems
- Raspberry Pi OS 64 bit (raspberry pi 3b)
- Linux Mint 21.3 (x86_64 PC)
