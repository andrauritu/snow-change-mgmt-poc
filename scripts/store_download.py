import os
import sys

use_sharepoint = os.environ.get("USE_SHAREPOINT", "false").lower()
download_to_path = os.environ["DOWNLOAD_TO_PATH"]

if use_sharepoint == "true":
    print("ERROR: SharePoint backend not implemented yet / waiting for non-prod environment.")
    sys.exit(1)

if not os.path.isfile(download_to_path):
    print(f"ERROR: Expected file not found: {download_to_path}")
    print("The download-artifact step may have failed.")
    sys.exit(1)

file_size = os.path.getsize(download_to_path)
print(f"Document store: artifact (SharePoint simulation)")
print(f"File verified: {download_to_path} ({file_size} bytes)")
