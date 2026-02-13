import os
import sys
import requests

instance = os.environ["SN_INSTANCE"].rstrip("/")
username = os.environ["SN_USERNAME"]
password = os.environ["SN_PASSWORD"]
template_id = os.environ["SN_STD_TEMPLATE_SYSID"]
description = "DPMD GDSN+ Release"

url = f"{instance}/api/sn_chg_rest/v1/change/standard/{template_id}"
params = {"short_description": description}

response = requests.post(
    url,
    auth=(username, password),
    headers={"Accept": "application/json"},
    params=params,
    json={}
)

if response.status_code not in [200, 201]:
    print(f"Error: HTTP {response.status_code}")
    print(response.text[:500])
    sys.exit(1)

result = response.json()["result"]
chg_number = result["number"]["value"]
chg_sysid = result["sys_id"]["value"]

print(f"Created: {chg_number}")

github_output = os.environ.get("GITHUB_OUTPUT")
if github_output:
    with open(github_output, "a") as f:
        f.write(f"chg_number={chg_number}\n")
        f.write(f"chg_sysid={chg_sysid}\n")
        f.write(f"chg_description={description}\n")
