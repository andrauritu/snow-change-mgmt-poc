import sys
import requests
from utils.graph_get_token import get_token


def main():
    try:
        token = get_token()

        site_resp = requests.get(
            "https://graph.microsoft.com/v1.0/sites/pgone.sharepoint.com:/sites/AccioSpace",
            headers={"Authorization": f"Bearer {token}"},
        )
        if site_resp.status_code != 200:
            raise RuntimeError(f"Site lookup failed with HTTP {site_resp.status_code}: {site_resp.text[:500]}")

        site = site_resp.json()
        print(f"Site name:  {site.get('displayName')}")
        print(f"Site ID:    {site['id']}")
        print(f"\nUse this as SP_SITE_ID in GitHub Secrets.")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
