import os
import sys
import requests


def main():
    use_sharepoint = os.environ.get("USE_SHAREPOINT", "false").lower()
    download_to_path = os.environ["DOWNLOAD_TO_PATH"]

    if use_sharepoint == "true":
        from graph_get_token import get_token

        chg_number = os.environ["CHG_NUMBER"]
        token = get_token()
        site_id = os.environ["SP_SITE_ID"]
        base_folder = os.environ.get("SP_FOLDER", "GDSN/ReleaseEvidence")
        folder = f"{base_folder}/{chg_number}"

        file_name = os.path.basename(download_to_path)
        download_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/root:/{folder}/{file_name}:/content"

        download_resp = requests.get(download_url, headers={
            "Authorization": f"Bearer {token}",
        })

        if download_resp.status_code != 200:
            print(f"ERROR: Download failed with HTTP {download_resp.status_code}")
            print(download_resp.text[:500])
            sys.exit(1)

        with open(download_to_path, "wb") as f:
            f.write(download_resp.content)

        file_size = os.path.getsize(download_to_path)
        print(f"Document store: SharePoint")
        print(f"File downloaded: {download_to_path} ({file_size} bytes)")

    else:
        if not os.path.isfile(download_to_path):
            print(f"ERROR: Expected file not found: {download_to_path}")
            print("The download-artifact step may have failed.")
            sys.exit(1)

        file_size = os.path.getsize(download_to_path)
        print(f"Document store: artifact (SharePoint simulation)")
        print(f"File verified: {download_to_path} ({file_size} bytes)")


if __name__ == "__main__":
    main()
