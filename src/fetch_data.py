from typing import Any, Dict, List, Optional

import requests

from .auth import load_token_from_file

BASE_URL = "https://api.mycasavi.com/v2"


def fetch_all(path: str, params: Optional[Dict[str, Any]] = None) -> List[Dict]:
    """Fetch all items from a paginated API endpoint."""
    token = load_token_from_file()
    headers = {"token": token}
    url = f"{BASE_URL}{path}"
    items: List[Dict] = []

    while url:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        payload = resp.json()

        # get lists from payload with key 'list'
        page_items = payload.get("list", [])
        items.extend(page_items)

        # read next page
        links = payload.get("_links", {})
        url = links.get("next")

        # clear the params because they are already in the URL
        params = {}

    return items


def fetch_contacts(
    is_registered: Optional[bool] = None,
    is_invited: Optional[bool] = None,
    modified_after: Optional[str] = None,
    role: Optional[str] = None,
) -> List[Dict]:
    """Fetch all contacts with optional filters."""
    params: Dict[str, Any] = {}

    if is_registered is not None:
        params["isRegistered"] = str(is_registered).lower()

    if is_invited is not None:
        params["isInvited"] = str(is_invited).lower()

    if modified_after:
        params["modifiedAfter"] = modified_after

    if role:
        params["role"] = role

    return fetch_all("/contacts", params)


def fetch_units(
    include_inactive_contracts: Optional[bool] = None,
    modified_after: Optional[str] = None,
) -> List[Dict]:
    """Fetch all units with optional filters."""
    params: Dict[str, Any] = {}

    if include_inactive_contracts is not None:
        params["includeInactiveContracts"] = str(include_inactive_contracts).lower()

    if modified_after:
        params["modifiedAfter"] = modified_after

    return fetch_all("/units", params)


def fetch_properties(modified_after: Optional[str] = None) -> List[Dict]:
    """Fetch all properties with optional modification filter."""
    params: Dict[str, Any] = {}
    if modified_after:
        params["modifiedAfter"] = modified_after
    return fetch_all("/properties", params)


# if __name__ == "__main__":
#     contacts = fetch_contacts()
#     units = fetch_units()
#     properties = fetch_properties()

#     print(
#         f"{Contacts: len(contacts)}, Units: {len(units)}, Properties: {len(properties)}"
#     )
#     print("Contact[0]:", contacts[0])
#     print("Unit[0]:   ", units[0])
#     print("Property[0]:", properties[0])
