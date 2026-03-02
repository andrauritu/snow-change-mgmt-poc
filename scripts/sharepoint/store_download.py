import os
import sys
from urllib.parse import urlparse
import requests


def main():
    try:
        use_sharepoint = os.environ.get("USE_SHAREPOINT", "false").lower()
        download_to_path = os.environ["DOWNLOAD_TO_PATH"]

        if use_sharepoint == "true":
            from utils.sp_get_token import get_token

            chg_number = os.environ["CHG_NUMBER"]
            token = get_token()
            site_url = os.environ["SP_SITE_URL"].rstrip("/")
            base_folder = os.environ.get("SP_FOLDER", "GDSN/ReleaseEvidence")

            site_relative = urlparse(site_url).path
            folder_server_relative = f"{site_relative}/Shared Documents/{base_folder}/{chg_number}"

            file_name = os.path.basename(download_to_path)
            download_url = f"{site_url}/_api/web/GetFolderByServerRelativeUrl('{folder_server_relative}')/Files('{file_name}')/$value"

            download_resp = requests.get(download_url, headers={
                "Authorization": f"Bearer {token}",
            })

            if download_resp.status_code != 200:
                raise RuntimeError(f"Download failed with HTTP {download_resp.status_code}: {download_resp.text[:500]}")

            with open(download_to_path, "wb") as f:
                f.write(download_resp.content)

            file_size = os.path.getsize(download_to_path)
            print(f"Document store: SharePoint")
            print(f"File downloaded: {download_to_path} ({file_size} bytes)")

        else:
            if not os.path.isfile(download_to_path):
                raise RuntimeError(f"Expected file not found: {download_to_path}. The download-artifact step may have failed.")

            file_size = os.path.getsize(download_to_path)
            print(f"Document store: artifact (SharePoint simulation)")
            print(f"File verified: {download_to_path} ({file_size} bytes)")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
