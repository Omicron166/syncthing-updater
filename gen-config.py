import json

config = {
    "bin_path": "/usr/bin/syncthing",
    "upgrade_url": "https://upgrades.syncthing.net/meta.json",
    "architecture": "syncthing-linux-amd64"
}

config["bin_path"] = input("Enter the path to the syncthing binary: ")

upgrade_url = input("Enter the upgrade url (leave blank to use official syncthing update url): ")

if upgrade_url:
    config["upgrade_url"] = upgrade_url

config["architecture"] = input("Enter device architecture (e.g. syncthing-linux-amd64): ")

if input("Do you want to download prereleases? (yes/no, default: no): ").lower() in "yes":
    config["download_prereleases"] = True
else
    config["download_prereleases"] = False

print("Writing generated configuration to config.json")

with open("config.json", "w") as f:
    json.dump(config, f)
