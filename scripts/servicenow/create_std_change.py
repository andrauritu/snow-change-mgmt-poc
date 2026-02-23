import os
import sys
from sn_client import get_sn_session, check_response, set_output


def main():
    instance, session = get_sn_session()
    template_id = os.environ["SN_STD_TEMPLATE_SYSID"]
    description = os.environ.get("CHG_DESCRIPTION", "DPMD GDSN+ Release")

    url = f"{instance}/api/sn_chg_rest/v1/change/standard/{template_id}"
    response = session.post(url, params={"short_description": description}, json={})
    check_response(response)

    try:
        result = response.json()["result"]
    except (KeyError, ValueError) as e:
        print(f"Error parsing response: {e}")
        print(f"Response text: {response.text[:500]}")
        sys.exit(1)

    chg_number = result["number"]["value"]
    chg_sysid = result["sys_id"]["value"]

    print(f"Created: {chg_number}")

    set_output("chg_number", chg_number)
    set_output("chg_sysid", chg_sysid)
    set_output("chg_description", description)


if __name__ == "__main__":
    main()
