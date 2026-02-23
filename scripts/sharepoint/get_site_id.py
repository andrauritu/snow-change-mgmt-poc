import sys
import requests
from graph_get_token import get_token


def main():
    token = get_token()

    site_resp = requests.get(
        "https://graph.microsoft.com/v1.0/sites/pgone.sharepoint.com:/sites/AccioSpace",
        headers={"Authorization": f"Bearer {token}"},
    )
    if site_resp.status_code != 200:
        print(f"ERROR: Site lookup failed: {site_resp.status_code}")
        print(site_resp.text[:500])
        sys.exit(1)

    site = site_resp.json()
    print(f"Site name:  {site.get('displayName')}")
    print(f"Site ID:    {site['id']}")
    print(f"\nUse this as SP_SITE_ID in GitHub Secrets.")


if __name__ == "__main__":
    main()
