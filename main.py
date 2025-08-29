import requests
import os
import json
from packaging import version
from sys import exit
from tqdm import tqdm
import tarfile
import shutil

# Load config
with open("config.json") as f:
    config = json.load(f)

# Check write access to bin_path
try:
    if os.path.isfile(config["bin_path"]):
        assert os.access(config["bin_path"], os.W_OK)
    else:
        assert os.access(os.path.dirname(config["bin_path"]), os.W_OK)
except AssertionError:
    print("File cannot be written")

# Fetch latest available version
upgrade_data = requests.get(config["upgrade_url"]).json()[0]
latest_version = version.parse(upgrade_data["tag_name"])

# Get installed version (will crash on syncthing v1.x)
installed_version = version.parse(os.popen("syncthing version").read().split()[1])


if not installed_version < latest_version:
    print(f"Latest version already installed: v{latest_version}")
    exit()

print(f"Upgrade available {installed_version} -> {latest_version}")

# Make sure "downloads" is clean before starting
if os.path.exists("downloads"): shutil.rmtree("downloads")
os.mkdir("downloads")

# Find the right download link
for asset in upgrade_data["assets"]:
    if config["architecture"] in asset["name"]:
        download_url = asset["url"]

file_name = asset["url"].split("/").pop()

# Download the tar.gz with the syncthing binary
with requests.get(download_url, stream=True) as r:
    r.raise_for_status()

    total = int(r.headers.get("content-length", 0))

    with open(f"downloads/{file_name}", "wb") as f, tqdm(
        desc=file_name,
        total=total,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))

print("Download completed. Extracting")

# Extract the downloaded tar.gz
with tarfile.open(f"downloads/{file_name}", "r:gz") as tar:
    tar.extractall("downloads")

folder_name = file_name.removesuffix(".tar.gz")

print("Upgrading syncthing")

# Replace the binary and delete "downloads"
shutil.move(f"downloads/{folder_name}/syncthing", config["bin_path"])

print("Syncthing upgraded. Cleaning")

shutil.rmtree("downloads")
