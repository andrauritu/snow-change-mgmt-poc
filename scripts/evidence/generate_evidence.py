import os
import sys
from datetime import datetime, timezone


def main():
    try:
        chg_number = os.environ["SN_CHG_NUMBER"]
        version = os.environ["VERSION"]
        pipeline_url = os.environ["PIPELINE_URL"]
        scope = os.environ.get("SCOPE", "N/A")

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        content = f"""Deployment Evidence
===================

Change Request: {chg_number}
Version: {version}
Timestamp: {timestamp}
Pipeline: {pipeline_url}
Scope: {scope}

"""

        output_file = "deployment-evidence.txt"
        with open(output_file, "w") as f:
            f.write(content)
        print(f"Generated: {output_file}")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
