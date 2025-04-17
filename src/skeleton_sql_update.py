import os
from typing import Any, Dict, Iterable

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert


def _get_engine():
    url = os.getenv("DB_URL")
    if not url:
        raise RuntimeError("DB_URL not set")
    return sa.create_engine(url, pool_pre_ping=True, future=True)


metadata = sa.MetaData()
records_tbl = sa.Table(
    "casavi_records",
    metadata,
    sa.Column("platform", sa.Text),
    sa.Column("user_id", sa.Text, nullable=False),
    sa.Column("company_name", sa.Text),
    sa.Column("contact_id", sa.Text, nullable=False),
    sa.Column("unit_id", sa.Integer, nullable=False),
    sa.Column("property_id", sa.Integer, nullable=False),
    sa.Column("name", sa.Text),
    sa.Column("address", sa.Text),
    sa.Column("phone", sa.Text),
    sa.Column("email", sa.Text),
    sa.PrimaryKeyConstraint("user_id", "contact_id"),
)


def upsert(records: Iterable[Dict[str, Any]]) -> None:
    if not records:
        return
    engine = _get_engine()
    with engine.begin() as conn:
        stmt = insert(records_tbl).values(list(records))
        update_cols = {
            c.name: c for c in stmt.excluded if c.name not in records_tbl.primary_key
        }
        conn.execute(
            stmt.on_conflict_do_update(
                index_elements=records_tbl.primary_key.columns, set_=update_cols
            )
        )
