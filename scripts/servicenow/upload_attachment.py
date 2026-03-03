import os
import sys
from utils.sn_utils import get_sn_session, check_response, set_output
from servicenow.constants import SN_TABLE_CHANGE_TASK, DOCX_CONTENT_TYPE

def main():
    try:
        instance, session = get_sn_session()
        task_sysid = os.environ["SN_TASK_SYSID"]
        file_path = os.environ["EVIDENCE_FILE_PATH"]

        with open(file_path, "rb") as f:
            file_content = f.read()

        file_name = os.path.basename(file_path)

        url = f"{instance}/api/now/attachment/file"
        params = {
            "table_name": SN_TABLE_CHANGE_TASK,
            "table_sys_id": task_sysid,
            "file_name": file_name,
        }

        session.headers["Content-Type"] = DOCX_CONTENT_TYPE
        response = session.post(url, params=params, data=file_content)
        check_response(response)

        result = response.json()["result"]
        attachment_sysid = result["sys_id"]
        print(f"Attached: {file_name} ({attachment_sysid})")

        set_output("attachment_sysid", attachment_sysid)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
