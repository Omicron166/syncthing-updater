import requests
import os
import json
from packaging import version
from sys import exit
import tarfile
import shutil
import argparse
from core import downloader

# Start the argparser
parser = argparse.ArgumentParser(
#    prog="syncthing updater",
    description="A script for syncthing v2.x that mimics the syncthing v1.x auto upgrade from cli"
)

parser.add_argument("-c", "--config", help="Path to the json config file (config.json by default)", default="config.json")
parser.add_argument("--force", action="store_true", help="Replace the binary without checking the version")
parser.add_argument("--dry-run", action="store_true", dest="dry", help="Do not replace the binary")
parser.add_argument("--no-tqdm", action="store_false", dest="progress", help="Disable the download progress bar, tqdm is not required if this option is used")

args = parser.parse_args()

# Load config
with open(args.config) as f:
    config = json.load(f)

# Check write access to bin_path
try:
    if os.path.isfile(config["bin_path"]):
        assert os.access(config["bin_path"], os.W_OK)
    else:
        assert os.access(os.path.dirname(config["bin_path"]), os.W_OK)
        print("Binary does not exist on the configured path, use --force to install it")
        exit()
except AssertionError:
    print("File cannot be written, run again as privileged user")
    exit()

# Fetch latest available version

for upgrade in requests.get(config["upgrade_url"]).json():
    if upgrade["prerelease"] and not config["download_prerelease"]: continue
    ver = version.parse(upgrade["tag_name"])
    if ver < version.parse("v2.0.0"): continue
    upgrade_data = upgrade
    break

latest_version = version.parse(upgrade_data["tag_name"])

if args.force:
    print(f"Force upgrade to {latest_version}, skipping version check")
else:
    # Get installed version (will crash on syncthing v1.x)
    installed_version = version.parse(os.popen(config["bin_path"] + " version").read().split()[1])

    if not installed_version < latest_version:
        print(f"Latest version already installed: v{latest_version}")
        exit()

    print(f"Upgrade available {installed_version} -> {latest_version}")

# Make sure the download dir is clean before starting
if os.path.exists(config["download_path"]) and config["download_cleaning"]: shutil.rmtree(config["download_path"])

try:
    os.mkdir(config["download_path"])
except FileExistsError:
    pass

# Find the right download link
for asset in upgrade_data["assets"]:
    if config["architecture"] in asset["name"]:
        download_url = asset["url"]
        file_name = asset["url"].split("/").pop()

# Download the tar.gz with the syncthing binary

# Check that tqdm is installed
if args.progress:
    try:
        from tqdm import tqdm
    except:
        print("Optional dependency tqdm is missing, use --no-tqdm to hide this message")
        args.progress = False

# Actual download
try:
    if args.progress:
        # Tqdm version
        downloader.progressbar_download(download_url, config["download_path"], file_name) # Making the download path an option would be nice
    else:
        # No tqdm version
        print("Downloading...")
        downloader.download(download_url, config["download_path"], file_name)
except:
    print("Download error")
    exit()

print("Download completed. Extracting")

# Extract the downloaded tar.gz
with tarfile.open(config["download_path"]+ f"/{file_name}", "r:gz") as tar:
    tar.extractall(config["download_path"])

folder_name = file_name.removesuffix(".tar.gz")

print("Upgrading syncthing")

if args.dry:
    print("Dry run, skipping binary replacement")
else:
    # Replace the binary and clean the download dir
    try:
        shutil.move(config["download_path"] + f"/{folder_name}/syncthing", config["bin_path"])
    except:
        print("Upgrade error, make sure syncthing is not running.")
        exit()

print("Syncthing upgraded.")
if config["download_cleaning"]:
    print("Cleaning.")
    shutil.rmtree(config["download_path"])
