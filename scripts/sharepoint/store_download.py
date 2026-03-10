import os
import sys
import requests
from utils.sp_utils import get_token, check_sp_response, get_graph_drive_id
from sharepoint.constants import SP_DEFAULT_BASE_FOLDER

def main():
    try:
        download_to_path = _read_inputs()
        file_size = _download_from_sharepoint(download_to_path)
        print(f"File downloaded: {download_to_path} ({file_size} bytes)")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def _read_inputs():
    download_to_path = os.environ["DOWNLOAD_TO_PATH"]
    return download_to_path


def _download_from_sharepoint(download_to_path):
    chg_number = os.environ["CHG_NUMBER"]
    token = get_token()
    site_url = os.environ["SP_SITE_URL"].rstrip("/")
    base_folder = os.environ.get("SP_FOLDER", SP_DEFAULT_BASE_FOLDER)

    site_id, drive_id = get_graph_drive_id(site_url, token)

    file_name = os.path.basename(download_to_path)
    download_path = f"{base_folder}/{chg_number}/{file_name}"

    download_resp = requests.get(
        f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/root:/{download_path}:/content",
        headers={"Authorization": f"Bearer {token}"},
    )
    check_sp_response(download_resp, context="Download")

    with open(download_to_path, "wb") as f:
        f.write(download_resp.content)

    return os.path.getsize(download_to_path)


if __name__ == "__main__":
    main()
