import os
import sys
from urllib.parse import urlparse
import requests
from utils.sn_client import set_output

DOCX_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def ensure_folder_exists(site_url, folder_server_relative, headers):
    resp = requests.post(
        f"{site_url}/_api/web/folders",
        headers={**headers, "Content-Type": "application/json;odata=verbose"},
        json={"__metadata": {"type": "SP.Folder"}, "ServerRelativeUrl": folder_server_relative},
    )
    if resp.status_code == 201:
        return
    if resp.status_code == 500 and "-2130575338" in resp.text: #this is a specific sharepoint internall error corde 
        return  
    raise RuntimeError(f"Folder creation failed with HTTP {resp.status_code}: {resp.text[:500]}")


def main():
    try:
        use_sharepoint = os.environ.get("USE_SHAREPOINT", "false").lower()
        chg_number = os.environ["CHG_NUMBER"]
        local_file_path = os.environ["LOCAL_FILE_PATH"]

        if not os.path.isfile(local_file_path):
            raise RuntimeError(f"File not found: {local_file_path}")

        file_size = os.path.getsize(local_file_path)

        if use_sharepoint == "true":
            from utils.sp_get_token import get_token

            token = get_token()
            site_url = os.environ["SP_SITE_URL"].rstrip("/")
            base_folder = os.environ.get("SP_FOLDER", "GDSN/ReleaseEvidence")

            site_relative = urlparse(site_url).path
            folder_server_relative = f"{site_relative}/Shared Documents/{base_folder}/{chg_number}"

            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json;odata=verbose",
            }

            ensure_folder_exists(site_url, folder_server_relative, headers)

            file_name = os.path.basename(local_file_path)
            upload_url = f"{site_url}/_api/web/GetFolderByServerRelativeUrl('{folder_server_relative}')/Files/add(url='{file_name}',overwrite=true)"

            with open(local_file_path, "rb") as f:
                file_content = f.read()

            upload_resp = requests.post(upload_url, headers={
                **headers,
                "Content-Type": DOCX_CONTENT_TYPE,
            }, data=file_content)

            if upload_resp.status_code not in (200, 201):
                raise RuntimeError(f"Upload failed with HTTP {upload_resp.status_code}: {upload_resp.text[:500]}")

            server_relative = upload_resp.json()["d"]["ServerRelativeUrl"]
            hostname = f"https://{urlparse(site_url).hostname}"
            store_link = f"{hostname}{server_relative}"

            print(f"Document store: SharePoint")
            print(f"File: {local_file_path} ({file_size} bytes)")
            print(f"Change: {chg_number}")
            print(f"Store link: {store_link}")

        else:
            store_link = "artifact://validation-testing-draft"
            print(f"Document store: artifact (SharePoint simulation)")
            print(f"File: {local_file_path} ({file_size} bytes)")
            print(f"Change: {chg_number}")
            print(f"Store link: {store_link}")

        set_output("store_link", store_link)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
