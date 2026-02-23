import os
from sn_client import get_sn_session, check_response


def main():
    instance, session = get_sn_session()
    change_id = os.environ["SN_CHG_SYSID"]
    target_state = os.environ["SN_TARGET_STATE"]

    url = f"{instance}/api/sn_chg_rest/change/standard/{change_id}"
    response = session.patch(url, json={"state": target_state})
    check_response(response)

    result = response.json().get("result", {})
    change_number = result.get("number", {}).get("value", "?")
    new_state = result.get("state", {}).get("display_value", "?")
    print(f"{change_number} -> {new_state}")


if __name__ == "__main__":
    main()

