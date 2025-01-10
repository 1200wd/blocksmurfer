# -*- coding: utf-8 -*-
#
#    Blocksmurfer - Database to store keys for API authentication
#
#    © 2020-2025 Januari - 1200 Web Development
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#

import sqlite3
from config import Config
from pathlib import Path


sql_schema = """
    CREATE TABLE IF NOT EXISTS api_auth_keys (
        auth_key TEXT PRIMARY KEY,
        name TEXT NOT NULL)
"""


def init_db():
    db = get_db()
    db.executescript(sql_schema)


def get_db():
    Path("db").mkdir(exist_ok=True)
    db = sqlite3.connect(
        "db/%s" % Config.API_AUTH_DATABASE_FILE,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row

    return db

def check_api_auth_key(auth_key):
    db = get_db()
    cur = db.cursor()
    res = cur.execute("SELECT * FROM api_auth_keys WHERE auth_key='%s'" % auth_key)
    return res.fetchone()

#
#
# def close_db(e=None):
#     db = g.pop('db', None)
#
#     if db is not None:
#         db.close()