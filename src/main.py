import argparse
import json

from .fetch_data import fetch_contacts, fetch_properties, fetch_units
from .transform_data import build_records

PLATFORM = "CASAVI"
USER_ID = "DEMO"
COMPANY_NAME = "MANAGBL.AI"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/export.json")
    args = parser.parse_args()

    print("fetch contacts")
    contacts = fetch_contacts()

    print("fetch units")
    units = fetch_units()

    print("fetch properties")
    properties = fetch_properties()

    print("transform records")
    records = build_records(
        contacts,
        units,
        properties,
        platform="casavi",
        user_id="demo_Platform",
        company_name="MANAGBL.AI Platform",
    )

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"Export in {args.output}")


if __name__ == "__main__":
    main()
