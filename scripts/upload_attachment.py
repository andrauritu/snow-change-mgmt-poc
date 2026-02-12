import os
import sys
import requests

instance = os.environ["SN_INSTANCE"].rstrip("/")
username = os.environ["SN_USERNAME"]
password = os.environ["SN_PASSWORD"]
task_sysid = os.environ["SN_TASK_SYSID"]
file_path = os.environ["EVIDENCE_FILE_PATH"]

with open(file_path, "rb") as f:
    file_content = f.read()

file_name = os.path.basename(file_path)

url = f"{instance}/api/now/attachment/file"
params = {
    "table_name": "change_task",
    "table_sys_id": task_sysid,
    "file_name": file_name
}

response = requests.post(
    url,
    auth=(username, password),
    headers={"Content-Type": "text/plain"},
    params=params,
    data=file_content
)

if response.status_code not in [200, 201]:
    print(f"Error: HTTP {response.status_code}")
    print(response.text[:500])
    sys.exit(1)

result = response.json()["result"]
attachment_sysid = result["sys_id"]
download_link = result["download_link"]

print(f"Uploaded attachment: {file_name}")
print(f"Download: {download_link}")

github_output = os.environ.get("GITHUB_OUTPUT")
if github_output:
    with open(github_output, "a") as f:
        f.write(f"attachment_sysid={attachment_sysid}\n")
