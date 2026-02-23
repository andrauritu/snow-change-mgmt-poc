import os
import sys
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
        print(f"ERROR: Token request failed with HTTP {response.status_code}")
        print(response.text[:500])
        sys.exit(1)

    token = response.json().get("access_token")
    if not token:
        print("ERROR: No access_token in response")
        print(response.text[:500])
        sys.exit(1)

    return token


if __name__ == "__main__":
    token = get_token()
    print(f"TOKEN_OK (length={len(token)})")
