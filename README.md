# casavi-api-task

This Python project provides an interface to fetch data from the CASAVI API [https://api.mycasavi.com/v2/docs/manager], specifically for:
- Contacts (`/contacts`)
- Units (`/units`)
- Properties (`/properties`)

It handles authentication via token and supports paginated results automatically.

## Installation (for Linux OS)

1. Clone the repository:

```bash
git clone git@github.com:DaDozlov/casavi-api-task.git
cd casavi-api-task
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

> Make sure you have Python 3.10+ installed.

## How to Run:

Before running, make sure you have:
- A valid API token stored in `token.json` or another file used in your script.
- If not valid token is stored, you can generate it yourself by running:
```bash
python src/auth.py
```
But you need .env file stored with `CASAVI_API_KEY` and `CASAVI_API_SECRET`

Example usage:

```bash
python src/main.py
```

## Results

After running the script, you get `export.json` file in your data directory.

Below is an explanation of the fields:

```
platform     : Platform name (extern)
user_id      : Username (extern)
company_name : Companyname (extern)
contact_id   : intern contact ID
unit_id      : intern unit ID
property_id  : intern property ID
name         : intern name of the tenant/owner
address      : intern address
phone        : intern phone of the tenant/owner
email        : intern email of the tenant/owner
```
