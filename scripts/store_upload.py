import os
import sys

use_sharepoint = os.environ.get("USE_SHAREPOINT", "false").lower()
chg_number = os.environ["CHG_NUMBER"]
local_file_path = os.environ["LOCAL_FILE_PATH"]

if use_sharepoint == "true":
    print("ERROR: SharePoint backend not implemented yet / waiting for non-prod environment.")
    sys.exit(1)

if not os.path.isfile(local_file_path):
    print(f"ERROR: File not found: {local_file_path}")
    sys.exit(1)

file_size = os.path.getsize(local_file_path)
store_link = "artifact://validation-testing-draft"

print(f"Document store: artifact (SharePoint simulation)")
print(f"File: {local_file_path} ({file_size} bytes)")
print(f"Change: {chg_number}")
print(f"Store link: {store_link}")

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"store_link={store_link}\n")
