"""Indian medicine lookup backed by a local SQLite copy of the
Indian Medicine Dataset (~254k brands sold in India, MIT licensed):
https://github.com/junioralive/Indian-Medicine-Dataset

The CSV (~30 MB) is downloaded once and loaded into data/medicines.db.
Run `python setup_data.py` to do this ahead of time, or it happens
automatically the first time a search is made.
"""

import csv
import io
import os
import re
import sqlite3

import requests

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_PATH = os.path.join(DATA_DIR, "medicines.db")
CSV_URL = (
    "https://raw.githubusercontent.com/junioralive/Indian-Medicine-Dataset/"
    "main/DATA/indian_medicine_data.csv"
)
SOURCE_NAME = "Indian Medicine Dataset (junioralive, MIT)"


def is_ready():
    if not os.path.exists(DB_PATH):
        return False
    try:
        with sqlite3.connect(DB_PATH) as conn:
            return conn.execute("SELECT COUNT(*) FROM medicines").fetchone()[0] > 0
    except sqlite3.Error:
        return False


def build_database(progress=None):
    """Download the CSV and load it into SQLite. Returns the row count."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if progress:
        progress("Downloading Indian medicine dataset (~30 MB)...")
    resp = requests.get(CSV_URL, timeout=120)
    resp.raise_for_status()
    text = resp.content.decode("utf-8-sig")

    if progress:
        progress("Building local medicine database...")
    tmp_path = DB_PATH + ".tmp"
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    conn = sqlite3.connect(tmp_path)
    conn.execute("""
        CREATE TABLE medicines (
            id INTEGER PRIMARY KEY,
            name TEXT,
            name_lower TEXT,
            price REAL,
            discontinued INTEGER,
            manufacturer TEXT,
            type TEXT,
            pack_size TEXT,
            composition1 TEXT,
            composition2 TEXT,
            composition_key TEXT
        )
    """)

    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        try:
            price = float(r.get("price(₹)") or 0)
        except ValueError:
            price = None
        comp1 = (r.get("short_composition1") or "").strip()
        comp2 = (r.get("short_composition2") or "").strip()
        name = (r.get("name") or "").strip()
        rows.append((
            int(r["id"]), name, name.lower(), price,
            1 if (r.get("Is_discontinued") or "").upper() == "TRUE" else 0,
            (r.get("manufacturer_name") or "").strip(),
            (r.get("type") or "").strip(),
            (r.get("pack_size_label") or "").strip(),
            comp1, comp2, composition_key(comp1, comp2),
        ))
    conn.executemany(
        "INSERT INTO medicines VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows
    )
    conn.execute("CREATE INDEX idx_name ON medicines(name_lower)")
    conn.execute("CREATE INDEX idx_comp ON medicines(composition_key)")
    conn.commit()
    conn.close()
    os.replace(tmp_path, DB_PATH)
    return len(rows)


def ensure_database(progress=None):
    if not is_ready():
        build_database(progress)


def composition_key(comp1, comp2=""):
    """Normalised composition so identical salts+strengths match."""
    parts = [p.strip().lower() for p in (comp1, comp2) if p and p.strip()]
    return " + ".join(sorted(parts))


def _row_to_dict(row):
    keys = ["id", "name", "price", "discontinued", "manufacturer",
            "type", "pack_size", "composition1", "composition2"]
    d = dict(zip(keys, row))
    d["discontinued"] = bool(d["discontinued"])
    d["composition"] = " + ".join(
        c for c in (d["composition1"], d["composition2"]) if c
    )
    return d


_COLUMNS = ("id, name, price, discontinued, manufacturer, type, "
            "pack_size, composition1, composition2")


def search_medicines(query, limit=10, include_discontinued=False):
    """Search by brand name first, then by salt/composition."""
    ensure_database()
    q = (query or "").strip().lower()
    if len(q) < 2:
        return []
    disc = "" if include_discontinued else "AND discontinued = 0"
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            f"SELECT {_COLUMNS} FROM medicines WHERE name_lower LIKE ? {disc} "
            "ORDER BY length(name) LIMIT ?",
            (q + "%", limit),
        ).fetchall()
        if len(rows) < limit:
            seen = {r[0] for r in rows}
            more = conn.execute(
                f"SELECT {_COLUMNS} FROM medicines "
                f"WHERE (name_lower LIKE ? OR composition_key LIKE ?) {disc} "
                "ORDER BY length(name) LIMIT ?",
                ("%" + q + "%", "%" + q + "%", limit * 2),
            ).fetchall()
            rows += [r for r in more if r[0] not in seen][: limit - len(rows)]
    return [_row_to_dict(r) for r in rows]


def get_medicine(medicine_id):
    ensure_database()
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            f"SELECT {_COLUMNS} FROM medicines WHERE id = ?", (medicine_id,)
        ).fetchone()
    return _row_to_dict(row) if row else None


def find_alternatives(medicine, limit=10):
    """Other brands with exactly the same composition, cheapest first."""
    key = composition_key(medicine["composition1"], medicine["composition2"])
    if not key:
        return []
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            f"SELECT {_COLUMNS} FROM medicines WHERE composition_key = ? "
            "AND discontinued = 0 AND id != ? AND price > 0 "
            "ORDER BY price LIMIT ?",
            (key, medicine["id"], limit),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def salt_names(medicine):
    """'Amoxycillin (500mg)' -> 'Amoxycillin'."""
    names = []
    for comp in (medicine.get("composition1"), medicine.get("composition2")):
        if comp:
            name = re.sub(r"\(.*?\)", "", comp).strip()
            if name:
                names.append(name)
    return names
