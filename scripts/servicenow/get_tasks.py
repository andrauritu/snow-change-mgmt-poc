import os
import sys
from sn_client import get_sn_session, check_response, set_output

TASK_TYPE_IMPLEMENT = "implementation"

instance, session = get_sn_session()
change_id = os.environ["SN_CHG_SYSID"]

url = f"{instance}/api/sn_chg_rest/v1/change/{change_id}/task"
response = session.get(url)
check_response(response, expected=(200,))

tasks = response.json()["result"]

implement_task = None
for task in tasks:
    if task["change_task_type"]["value"] == TASK_TYPE_IMPLEMENT:
        implement_task = task
        break

if not implement_task:
    print(f"ERROR: No '{TASK_TYPE_IMPLEMENT}' task found on change {change_id}")
    sys.exit(1)

task_sysid = implement_task["sys_id"]["value"]
task_number = implement_task["number"]["value"]
print(f"Found: {task_number} ({task_sysid})")

set_output("implement_task_sysid", task_sysid)
set_output("implement_task_number", task_number)
