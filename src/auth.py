import json
import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.mycasavi.com/v2/authenticate"
TOKEN_FILE = "token.json"


def get_token() -> str:
    """Get a token and save it as token.json."""
    key = os.getenv("CASAVI_API_KEY")
    secret = os.getenv("CASAVI_API_SECRET")
    if not key or not secret:
        raise RuntimeError("CASAVI_API_KEY und CASAVI_API_SECRET must be presented.")

    payload = {"key": key, "secret": secret}

    resp = requests.post(API_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()

    # get the time when token was received
    data["fetchedAt"] = datetime.now(timezone.utc).isoformat()
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return data["token"]


def load_token_from_file() -> str:
    """Load token from the token.json file."""
    with open("token.json") as f:
        return json.load(f)["token"]


if __name__ == "__main__":
    get_token()
