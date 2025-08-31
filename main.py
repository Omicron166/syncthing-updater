import requests
import os
import json
from packaging import version
from sys import exit
import tarfile
import shutil
import argparse

# Start the argparser
parser = argparse.ArgumentParser(
#    prog="syncthing updater",
    description="A script for syncthing v2.x that mimics the syncthing v1.x auto upgrade from cli"
)

parser.add_argument("-c", "--config", help="Path to the json config file", default="config.json")
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
    print("File cannot be written")

# Fetch latest available version
upgrade_data = requests.get(config["upgrade_url"]).json()[0]
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

# Make sure "downloads" is clean before starting
if os.path.exists("downloads"): shutil.rmtree("downloads")
os.mkdir("downloads")

# Find the right download link
for asset in upgrade_data["assets"]:
    if config["architecture"] in asset["name"]:
        download_url = asset["url"]
        file_name = asset["url"].split("/").pop()

# Download the tar.gz with the syncthing binary
try:
    if args.progress:
        # Check that tqdm is installed
        try:
            from tqdm import tqdm
        except:
            print("Optional dependency tqdm is missing, use --no-download-progress to avoid it")
            exit()

        # Actual download
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
    else:
        # Just download
        print("Downloading...")
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()

            with open(f"downloads/{file_name}", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
except:
    print("Download error")
    exit()

print("Download completed. Extracting")

# Extract the downloaded tar.gz
with tarfile.open(f"downloads/{file_name}", "r:gz") as tar:
    tar.extractall("downloads")

folder_name = file_name.removesuffix(".tar.gz")

print("Upgrading syncthing")

if args.dry:
    print("Dry run, skipping binary replacement")
else:
    # Replace the binary and delete "downloads"
    try:
        shutil.move(f"downloads/{folder_name}/syncthing", config["bin_path"])
    except:
        print("Upgrade error, make sure syncthing is not running.")
        exit()

print("Syncthing upgraded. Cleaning")

shutil.rmtree("downloads")
