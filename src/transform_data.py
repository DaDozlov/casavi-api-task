from typing import Any, Dict, List


def resolve_address(unit: Dict[str, Any], prop: Dict[str, Any]) -> str:
    """Get an address from the unit or property."""

    # firstly, we should look if the address is included in the unit
    # if not, try to get address from the property

    if unit.get("address"):
        return unit["address"]

    for a in prop.get("addresses", []):
        if unit["id"] in a.get("units", []):
            return a.get("street", "")

    return ""


def build_records(
    contacts: List[Dict[str, Any]],
    units: List[Dict[str, Any]],
    properties: List[Dict[str, Any]],
    platform: str,
    user_id: str,
    company_name: str,
) -> List[Dict[str, Any]]:
    """Build a record using the contact, units and properties data."""

    # for each contact get their contracts, where each of the contract has
    # it's unitId and propertyId

    # id maps for units and properties
    unit_map = {u["id"]: u for u in units}
    prop_map = {p["id"]: p for p in properties}

    records: List[Dict[str, Any]] = []

    # main loop for all contacts
    for row in contacts:
        # try to get the name and companyName
        if row.get("firstName") or row.get("lastName"):
            name = " ".join(
                filter(None, [row.get("firstName"), row.get("lastName")])
            ).strip()
        else:
            name = ""

        email = row.get("email") or ""

        # depends on the customers, which is more important, mobile or telephone
        phone = row.get("telephone") or row.get("mobile") or ""

        # each contract in contact should have unitId and propertyId
        for contract in row.get("contracts", []):
            unit_id = contract.get("unitId")
            prop_id = contract.get("propertyId")

            if not unit_id or not prop_id:
                continue

            unit = unit_map.get(unit_id)
            prop = prop_map.get(prop_id)

            # if anything is missing -> continue
            if unit is None or prop is None:
                continue

            record = {
                "platform": platform,
                "user_id": user_id,
                "company_name": company_name,
                "contact_id": str(row.get("id", "")),
                "unit_id": unit_id,
                "property_id": prop_id,
                "name": name,
                "address": resolve_address(unit, prop),
                "phone": phone,
                "email": email,
            }
            records.append(record)

    return records
