import requests
from packaging import version

# Config mock so I can just copy and paste from main.py
config = {
    "upgrade_url": "https://upgrades.syncthing.net/meta.json",
    "prerelease": False
}

for upgrade in requests.get(config["upgrade_url"]).json():
    if upgrade["prerelease"] and not config["download_prerelease"]: continue
    ver = version.parse(upgrade["tag_name"])
    if ver < version.parse("v2.0.0"): continue
    upgrade_data = upgrade
    break

latest_version = upgrade_data["tag_name"]
print(f"Prereleases: {config['prerelease']}")
print(f"Latest version: {latest_version}")
print("================================")
for asset in upgrade_data["assets"]:
    if not asset["name"].endswith(".tar.gz"): continue # Man, think about the .deb users | Nah man you tweaking, they already got the apt repository
    parts = asset["name"].split("-")
    # parts[0] is always syncthing
    os = parts[1]
    arch = parts[2]
    if os == "source": continue # Sneaky bastard
    print(f"syncthing-{os}-{arch}")
