import requests

def progressbar_download(download_url, file_path, file_name):
    from tqdm import tqdm
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()

        total = int(r.headers.get("content-length", 0))

        with open(f"{file_path}/{file_name}", "wb") as f, tqdm(
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

def download(download_url, file_path, file_name):
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(f"{file_path}/{file_name}", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
