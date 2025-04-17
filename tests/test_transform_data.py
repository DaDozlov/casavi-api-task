from src.transform_data import build_records, resolve_address


def _mini_contact(**kwargs):
    """Produce a minimal contact with 1 contract."""
    defaults = dict(
        id=1,
        firstName="",
        lastName="",
        companyName="Test Orga",
        email="",
        telephone="",
        mobile="",
        contracts=[{"unitId": 10, "propertyId": 20}],
    )
    defaults.update(kwargs)
    return defaults


def test_resolve_address_prefers_unit():
    unit = {"id": 1, "address": "Unit‑Addr"}
    prop = {"addresses": [{"street": "Prop‑Addr", "units": [1]}]}
    assert resolve_address(unit, prop) == "Unit‑Addr"


def test_resolve_address_falls_back_to_property():
    unit = {"id": 2}  # no address
    prop = {"addresses": [{"street": "Prop‑Addr", "units": [2]}]}
    assert resolve_address(unit, prop) == "Prop‑Addr"


def test_resolve_address_no_match_returns_empty() -> None:
    unit = {"id": 99}
    prop = {"addresses": [{"street": "Some St", "units": [1, 2]}]}
    assert resolve_address(unit, prop) == ""


def test_build_records_happy_path():
    contacts = [
        {
            "id": 10,
            "firstName": "Ada",
            "lastName": "Lovelace",
            "email": "ada@example.com",
            "telephone": "",
            "mobile": "+49111",
            "contracts": [{"unitId": 1, "propertyId": 100}],
        }
    ]
    units = [{"id": 1, "address": "Unit‑Addr"}]
    properties = [{"id": 100, "addresses": []}]

    recs = build_records(
        contacts,
        units,
        properties,
        platform="CASAVI",
        user_id="demo",
        company_name="MANAGBL.AI",
    )

    assert len(recs) == 1
    rec = recs[0]
    assert rec["name"] == "Ada Lovelace"
    assert rec["address"] == "Unit‑Addr"
    assert rec["platform"] == "CASAVI"


def test_build_records_companyname_and_phone_fallback() -> None:
    contacts = [
        _mini_contact(
            telephone="",
            mobile="+49123",
            firstName="",
            lastName="",
        )
    ]
    units = [{"id": 10, "address": ""}]
    properties = [{"id": 20, "addresses": []}]

    [rec] = build_records(
        contacts,
        units,
        properties,
        platform="CASAVI",
        user_id="u1",
        company_name="Managbl",
    )

    assert rec["name"] == ""
    assert rec["phone"] == "+49123"
    assert rec["email"] == ""
    assert rec["address"] == ""


def test_build_records_multiple_contracts_produce_multiple_records() -> None:
    contacts = [
        _mini_contact(
            id=42,
            firstName="Ada",
            lastName="Lovelace",
            contracts=[
                {"unitId": 1, "propertyId": 100},
                {"unitId": 2, "propertyId": 200},
            ],
        )
    ]
    units = [
        {"id": 1, "address": "Addr 1"},
        {"id": 2, "address": "Addr 2"},
    ]
    properties = [
        {"id": 100, "addresses": []},
        {"id": 200, "addresses": []},
    ]

    recs = build_records(contacts, units, properties, "CASAVI", "userX", "Managbl")

    # two contracts -> two records
    assert len(recs) == 2

    # order of contracts preserved
    assert recs[0]["unit_id"] == 1 and recs[1]["unit_id"] == 2

    # name composed from first and last
    assert recs[0]["name"] == "Ada Lovelace"


def test_build_records_skips_missing_ids_and_missing_refs() -> None:
    contacts = [
        # contract has no propertyId -> skip
        _mini_contact(contracts=[{"unitId": 10, "propertyId": None}]),
        # contract references unknown unit / property -> skip
        _mini_contact(contracts=[{"unitId": 999, "propertyId": 888}]),
    ]
    units = [{"id": 10, "address": "X"}]
    properties = [{"id": 20, "addresses": []}]

    recs = build_records(contacts, units, properties, "p", "u", "c")
    assert recs == []
