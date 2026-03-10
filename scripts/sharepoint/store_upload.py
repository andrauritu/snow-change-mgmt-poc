import os
import sys
import requests
from utils.sn_utils import set_output
from utils.sp_utils import get_token, check_sp_response, get_graph_drive_id
from sharepoint.constants import SP_DEFAULT_BASE_FOLDER, DOCX_CONTENT_TYPE

def main():
    try:
        chg_number, local_file_path, file_size = _read_inputs()
        store_link = _upload_to_sharepoint(chg_number, local_file_path)

        print(f"File: {local_file_path} ({file_size} bytes)")
        print(f"Change: {chg_number}")
        print(f"Store link: {store_link}")

        set_output("store_link", store_link)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def _read_inputs():
    chg_number = os.environ["CHG_NUMBER"]
    local_file_path = os.environ["LOCAL_FILE_PATH"]

    if not os.path.isfile(local_file_path):
        raise RuntimeError(f"File not found: {local_file_path}")

    file_size = os.path.getsize(local_file_path)
    return chg_number, local_file_path, file_size


def _upload_to_sharepoint(chg_number, local_file_path):
    token = get_token()
    site_url = os.environ["SP_SITE_URL"].rstrip("/")
    base_folder = os.environ.get("SP_FOLDER", SP_DEFAULT_BASE_FOLDER)

    site_id, drive_id = get_graph_drive_id(site_url, token)

    file_name = os.path.basename(local_file_path)
    upload_path = f"{base_folder}/{chg_number}/{file_name}"

    with open(local_file_path, "rb") as f:
        file_content = f.read()

    upload_resp = requests.put(
        f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/root:/{upload_path}:/content",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": DOCX_CONTENT_TYPE,
        },
        data=file_content,
    )
    check_sp_response(upload_resp, expected=(200, 201), context="Upload")

    return upload_resp.json()["webUrl"]


if __name__ == "__main__":
    main()
