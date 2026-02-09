import os
import sys
import requests

instance = os.environ["SN_INSTANCE"].rstrip("/")
username = os.environ["SN_USERNAME"]
password = os.environ["SN_PASSWORD"]
change_id = os.environ["SN_CHG_SYSID"]
target_state = os.environ["SN_TARGET_STATE"]

url = f"{instance}/api/sn_chg_rest/change/standard/{change_id}"
payload = {"state": target_state}

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

result = response.json().get("result", {})
change_number = result.get("number", {}).get("value", "?")
new_state = result.get("state", {}).get("display_value", "?")
print(f"{change_number} → {new_state}")

