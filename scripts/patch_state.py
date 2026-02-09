import os
import sys
import json
import requests

base = os.environ["SN_INSTANCE"].rstrip("/")
user = os.environ["SN_USERNAME"]
pw   = os.environ["SN_PASSWORD"]
chg_sysid = os.environ["SN_CHG_SYSID"]
target_state = os.environ["SN_TARGET_STATE"]

url = f"{base}/api/sn_chg_rest/change/standard/{chg_sysid}"

print(f"Patching change {chg_sysid} to state: {target_state}")

payload = {
    "state": target_state
}

r = requests.patch(
    url,
    auth=(user, pw),
    headers={"Accept": "application/json", "Content-Type": "application/json"},
    json=payload
)

print("Status:", r.status_code)

if r.status_code not in [200, 201]:
    print("ERROR - Response body:")
    print(r.text[:1000])
    sys.exit(1)

result = r.json().get("result", {})

print("\n--- Updated Change ---")
print(f"CHG: {result.get('number', {}).get('value', '?')}")
print(f"sys_id: {result.get('sys_id', {}).get('value', '?')}")
print(f"State: {result.get('state', {}).get('display_value', '?')} (value={result.get('state', {}).get('value', '?')})")

print("\n--- Machine-readable output ---")
summary = {
    "chg_sysid": chg_sysid,
    "chg_number": result.get("number", {}).get("value"),
    "new_state": {
        "value": result.get("state", {}).get("value"),
        "display_value": result.get("state", {}).get("display_value")
    }
}
print(json.dumps(summary, indent=2))
