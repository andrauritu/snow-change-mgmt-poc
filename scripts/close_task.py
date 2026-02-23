import os
from sn_client import get_sn_session, check_response

STATE_CLOSED = 3

instance, session = get_sn_session()
change_id = os.environ["SN_CHG_SYSID"]
task_sysid = os.environ["SN_TASK_SYSID"]

url = f"{instance}/api/sn_chg_rest/v1/change/{change_id}/task/{task_sysid}"
response = session.patch(url, json={"state": STATE_CLOSED})
check_response(response)

result = response.json()["result"]
task_number = result["number"]["value"]
task_state = result["state"]["display_value"]
print(f"Closed: {task_number} ({task_state})")

