import os
import sys
from utils.sn_utils import get_sn_session, check_response, set_output
from servicenow.constants import DEFAULT_CHG_DESCRIPTION

def main():
    try:
        instance, session = get_sn_session()
        template_id = os.environ["SN_STD_TEMPLATE_SYSID"]
        description = os.environ.get("CHG_DESCRIPTION", DEFAULT_CHG_DESCRIPTION)

        url = f"{instance}/api/sn_chg_rest/v1/change/standard/{template_id}"
        response = session.post(url, params={"short_description": description}, json={})
        check_response(response)

        result = response.json()["result"]
        chg_number = result["number"]["value"]
        chg_sysid = result["sys_id"]["value"]

        print(f"Created: {chg_number}")

        set_output("chg_number", chg_number)
        set_output("chg_sysid", chg_sysid)
        set_output("chg_description", description)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
