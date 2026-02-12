import os
import sys
import requests

instance = os.environ["SN_INSTANCE"].rstrip("/")
username = os.environ["SN_USERNAME"]
password = os.environ["SN_PASSWORD"]
change_id = os.environ["SN_CHG_SYSID"]

url = f"{instance}/api/sn_chg_rest/v1/change/{change_id}/task"
response = requests.get(url, auth=(username, password), headers={"Accept": "application/json"})

if response.status_code != 200:
    print(response.text[:500])
    sys.exit(1)

tasks = response.json()["result"]

implement_task = None
for task in tasks:
    if task["change_task_type"]["value"] == "implementation":
        implement_task = task
        break

if not implement_task:
    sys.exit(1)

task_sysid = implement_task["sys_id"]["value"]
task_number = implement_task["number"]["value"]



github_output = os.environ.get("GITHUB_OUTPUT")
if github_output:
    with open(github_output, "a") as f:
        f.write(f"implement_task_sysid={task_sysid}\n")
        f.write(f"implement_task_number={task_number}\n")
