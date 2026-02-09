
import os
import sys
import json
import requests

base = os.environ["SN_INSTANCE"].rstrip("/")
user = os.environ["SN_USERNAME"]
pw   = os.environ["SN_PASSWORD"]
chg_sysid = os.environ["SN_CHG_SYSID"]

url = f"{base}/api/sn_chg_rest/change/{chg_sysid}/nextstates"

print(f"Fetching next states for change sys_id: {chg_sysid}")
r = requests.get(url, auth=(user, pw), headers={"Accept": "application/json"})

print("Status:", r.status_code)
if r.status_code != 200:
    print("Body:", r.text[:500])
    sys.exit(1)

result = r.json().get("result", {})

print("\n--- Raw Response ---")
print(json.dumps(result, indent=2)[:1000])

if "current_state" in result:
    current = result["current_state"]
    if isinstance(current, dict):
        print(f"\nCurrent state: {current.get('display_value', 'unknown')} (value={current.get('value', '?')})")
    else:
        print(f"\nCurrent state: {current}")

transitions = result.get("available_states", [])
print(f"\nAvailable transitions ({len(transitions)}):")
for t in transitions:
    if isinstance(t, str):
        print(f"  ✓ {t}")
    elif isinstance(t, dict):
        available = t.get("transition_available", False)
        marker = "✓" if available else "✗"
        print(f"  {marker} {t.get('display_value', '?')} (value={t.get('value', '?')}) - available={available}")
        
        if not available and "not_available_reason" in t:
            print(f"      Reason: {t['not_available_reason']}")

print("\n--- Machine-readable output ---")
summary = {
    "chg_sysid": chg_sysid,
    "current_state": result.get("current_state"),
    "available_states": transitions
}
print(json.dumps(summary, indent=2))
