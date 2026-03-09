import os
import sys
from urllib.parse import urlparse
import requests

def get_token():
    tenant_id = os.environ["SP_TENANT_ID"]
    client_id = os.environ["SP_CLIENT_ID"]
    client_secret = os.environ["SP_CLIENT_SECRET"]

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    response = requests.post(token_url, data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
    })

    if response.status_code != 200:
        raise RuntimeError(f"Token request failed with HTTP {response.status_code}: {response.text[:500]}")

    token = response.json().get("access_token")
    if not token:
        raise RuntimeError("No access_token in response")

    return token


def get_graph_drive_id(site_url, token):
    parsed = urlparse(site_url)
    hostname = parsed.hostname
    site_path = parsed.path.rstrip("/")
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    site_resp = requests.get(
        f"https://graph.microsoft.com/v1.0/sites/{hostname}:{site_path}",
        headers=headers,
    )
    check_sp_response(site_resp, context="Get site")
    site_id = site_resp.json()["id"]

    drive_resp = requests.get(
        f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive",
        headers=headers,
    )
    check_sp_response(drive_resp, context="Get drive")
    return site_id, drive_resp.json()["id"]


def check_sp_response(response, expected=(200,), context="SharePoint request"):
    if response.status_code not in expected:
        raise RuntimeError(f"{context} failed with HTTP {response.status_code}: {response.text[:500]}")


if __name__ == "__main__":
    try:
        token = get_token()
        print(f"TOKEN_OK (length={len(token)})")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
