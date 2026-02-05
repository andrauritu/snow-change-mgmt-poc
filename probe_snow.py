import os
import requests

base = os.environ["SN_INSTANCE"].rstrip("/")
user = os.environ["SN_USERNAME"]
pw   = os.environ["SN_PASSWORD"]

url = f"{base}/api/sn_chg_rest/v1/change/model?sysparm_limit=1"

r = requests.get(url, auth=(user, pw), headers={"Accept":"application/json"})
print("URL:", url)
print("Status:", r.status_code)
print("Body (first 500 chars):", r.text[:500])
r.raise_for_status()
print("OK: sn_chg_rest reachable and auth works")