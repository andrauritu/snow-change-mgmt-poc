import os
import requests

def get_sn_session():
    instance = os.environ["SN_INSTANCE"].rstrip("/")
    username = os.environ["SN_USERNAME"]
    password = os.environ["SN_PASSWORD"]

    session = requests.Session()
    session.auth = (username, password)
    session.headers.update({
        "Accept": "application/json",
        "Content-Type": "application/json",
    })

    return instance, session


def check_response(response, expected=(200, 201)):
    if response.status_code not in expected:
        raise RuntimeError(f"HTTP {response.status_code}: {response.text[:500]}")


def set_output(key, value):
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"{key}={value}\n")
