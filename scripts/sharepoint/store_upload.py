import os
import sys
from urllib.parse import urlparse
import requests
from utils.sn_utils import set_output
from utils.sp_utils import get_token, check_sp_response
from sharepoint.constants import *

def main():
    try:
        use_sharepoint, chg_number, local_file_path, file_size = _read_inputs()

        if use_sharepoint == "true":
            store_link = _upload_to_sharepoint(chg_number, local_file_path)
            print(f"Document store: SharePoint")
        else:
            store_link = _upload_to_artifact()
            print(f"Document store: artifact (SharePoint simulation)")

        print(f"File: {local_file_path} ({file_size} bytes)")
        print(f"Change: {chg_number}")
        print(f"Store link: {store_link}")

        set_output("store_link", store_link)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def _read_inputs():
    use_sharepoint = os.environ.get("USE_SHAREPOINT", "false").lower()
    chg_number = os.environ["CHG_NUMBER"]
    local_file_path = os.environ["LOCAL_FILE_PATH"]

    if not os.path.isfile(local_file_path):
        raise RuntimeError(f"File not found: {local_file_path}")

    file_size = os.path.getsize(local_file_path)
    return use_sharepoint, chg_number, local_file_path, file_size


def _upload_to_sharepoint(chg_number, local_file_path):
    token = get_token()
    site_url = os.environ["SP_SITE_URL"].rstrip("/")
    base_folder = os.environ.get("SP_FOLDER", SP_DEFAULT_BASE_FOLDER)

    site_relative = urlparse(site_url).path
    folder_server_relative = f"{site_relative}/{SP_DOCUMENT_LIBRARY}/{base_folder}/{chg_number}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json;odata=verbose",
    }

    _ensure_folder_exists(site_url, folder_server_relative, headers)

    file_name = os.path.basename(local_file_path)
    upload_url = f"{site_url}/_api/web/GetFolderByServerRelativeUrl('{folder_server_relative}')/Files/add(url='{file_name}',overwrite=true)"

    with open(local_file_path, "rb") as f:
        file_content = f.read()

    upload_resp = requests.post(upload_url, headers={
        **headers,
        "Content-Type": DOCX_CONTENT_TYPE,
    }, data=file_content)

    check_sp_response(upload_resp, expected=(200, 201), context="Upload")

    server_relative = upload_resp.json()["d"]["ServerRelativeUrl"]
    hostname = f"https://{urlparse(site_url).hostname}"
    return f"{hostname}{server_relative}"


def _ensure_folder_exists(site_url, folder_server_relative, headers):
    resp = requests.post(
        f"{site_url}/_api/web/folders",
        headers={**headers, "Content-Type": "application/json;odata=verbose"},
        json={"__metadata": {"type": "SP.Folder"}, "ServerRelativeUrl": folder_server_relative},
    )
    if resp.status_code == 201 or (resp.status_code == 500 and SP_ERR_FOLDER_ALREADY_EXISTS in resp.text):
        return
    raise RuntimeError(f"Folder creation failed with HTTP {resp.status_code}: {resp.text[:500]}")


def _upload_to_artifact():
    return "artifact://validation-testing-draft"


if __name__ == "__main__":
    main()
