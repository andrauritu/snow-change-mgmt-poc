import os
import sys
import requests

use_sharepoint = os.environ.get("USE_SHAREPOINT", "false").lower()
chg_number = os.environ["CHG_NUMBER"]
local_file_path = os.environ["LOCAL_FILE_PATH"]

if not os.path.isfile(local_file_path):
    print(f"ERROR: File not found: {local_file_path}")
    sys.exit(1)

file_size = os.path.getsize(local_file_path)

if use_sharepoint == "true":
    from graph_get_token import get_token

    token = get_token()
    site_id = os.environ["SP_SITE_ID"]
    base_folder = os.environ.get("SP_FOLDER", "GDSN/ReleaseEvidence")
    folder = f"{base_folder}/{chg_number}"

    file_name = os.path.basename(local_file_path)
    upload_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/root:/{folder}/{file_name}:/content"

    with open(local_file_path, "rb") as f:
        upload_resp = requests.put(upload_url, headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }, data=f)

    if upload_resp.status_code not in [200, 201]:
        print(f"ERROR: Upload failed with HTTP {upload_resp.status_code}")
        print(upload_resp.text[:500])
        sys.exit(1)

    result = upload_resp.json()
    store_link = result.get("webUrl", upload_url)

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

from sn_client import set_output
set_output("store_link", store_link)
