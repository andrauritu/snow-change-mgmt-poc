import os, requests

base = os.environ["SN_INSTANCE"].rstrip("/")
user = os.environ["SN_USERNAME"]
pw   = os.environ["SN_PASSWORD"]
tpl  = os.environ["SN_STD_TEMPLATE_SYSID"]

url = f"{base}/api/sn_chg_rest/v1/change/standard/{tpl}"
params = {"short_description": "PoC: create standard change from GitHub Actions"}
r = requests.post(url, auth=(user,pw), headers={"Accept":"application/json"}, params=params, json={})

print("Status:", r.status_code)
print("Body (first 500 chars):", r.text[:500])
r.raise_for_status()

rec = r.json()["result"][0]
print("CHG:", rec["number"]["value"])
print("sys_id:", rec["sys_id"]["value"])