import os
import sys
import requests
from utils.sp_get_token import get_token


def main():
    try:
        token = get_token()

        site_url = os.environ["SP_SITE_URL"].rstrip("/")

        resp = requests.get(
            f"{site_url}/_api/web/title",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json;odata=verbose",
            },
        )
        if resp.status_code != 200:
            raise RuntimeError(f"Connectivity check failed with HTTP {resp.status_code}: {resp.text[:500]}")

        title = resp.json()["d"]["Title"]
        print(f"Connected to: {title}")
        print(f"Site URL:     {site_url}")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
