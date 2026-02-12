import os
import sys
import requests

instance = os.environ["SN_INSTANCE"].rstrip("/")
username = os.environ["SN_USERNAME"]
password = os.environ["SN_PASSWORD"]
change_id = os.environ["SN_CHG_SYSID"]
task_sysid = os.environ["SN_TASK_SYSID"]

url = f"{instance}/api/sn_chg_rest/v1/change/{change_id}/task/{task_sysid}"
payload = {"state": 3}

response = requests.patch(
    url,
    auth=(username, password),
    headers={"Accept": "application/json", "Content-Type": "application/json"},
    json=payload
)

if response.status_code not in [200, 201]:
    print(f"Error: HTTP {response.status_code}")
    print(response.text[:500])
    sys.exit(1)

result = response.json()["result"]
task_number = result["number"]["value"]
task_state = result["state"]["display_value"]

