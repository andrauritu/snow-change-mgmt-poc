import os
import sys
from urllib.parse import urlparse
import requests
from utils.sp_utils import get_token, check_sp_response
from sharepoint.constants import SP_DEFAULT_BASE_FOLDER, SP_DOCUMENT_LIBRARY

def main():
    try:
        use_sharepoint, download_to_path = _read_inputs()

        if use_sharepoint == "true":
            file_size = _download_from_sharepoint(download_to_path)
            print(f"File downloaded: {download_to_path} ({file_size} bytes)")
        else:
            file_size = _verify_artifact(download_to_path)
            print(f"File verified: {download_to_path} ({file_size} bytes)")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def _read_inputs():
    use_sharepoint = os.environ.get("USE_SHAREPOINT", "false").lower()
    download_to_path = os.environ["DOWNLOAD_TO_PATH"]
    return use_sharepoint, download_to_path


def _download_from_sharepoint(download_to_path):
    chg_number = os.environ["CHG_NUMBER"]
    token = get_token()
    site_url = os.environ["SP_SITE_URL"].rstrip("/")
    base_folder = os.environ.get("SP_FOLDER", SP_DEFAULT_BASE_FOLDER)

    site_relative = urlparse(site_url).path
    folder_server_relative = f"{site_relative}/{SP_DOCUMENT_LIBRARY}/{base_folder}/{chg_number}"

    file_name = os.path.basename(download_to_path)
    download_url = f"{site_url}/_api/web/GetFolderByServerRelativeUrl('{folder_server_relative}')/Files('{file_name}')/$value"

    download_resp = requests.get(download_url, headers={
        "Authorization": f"Bearer {token}",
    })

    check_sp_response(download_resp, context="Download")

    with open(download_to_path, "wb") as f:
        f.write(download_resp.content)

    return os.path.getsize(download_to_path)


def _verify_artifact(download_to_path):
    if not os.path.isfile(download_to_path):
        raise RuntimeError(f"Expected file not found: {download_to_path}. The download-artifact step may have failed.")
    return os.path.getsize(download_to_path)


if __name__ == "__main__":
    main()
