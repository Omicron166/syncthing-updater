# Syncthing updater
> Warning: This is just a quick prototype I made in an afternoon, use at your own risk.
## Why?
Syncthing v1.x has `syncthing serve -u`, which upgrades the binary without loading syncthing itself.

Syncthing v2.x auto upgrade requires the syncthing service to be able to write the binary. If you have syncthing in `/usr/bin/` you either have to boot the syncthing server as root or manually replace the binary.

This script is a replacement for the old auto upgrade on syncthing v2.x.

## How to use
1. Install the dependencies (requirements.txt).
2. Copy `config_sample.json` to `config.json` and fill it.
3. Pray to God.
4. Run `main.py`