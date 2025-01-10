# -*- coding: utf-8 -*-
#
#    Blocksmurfer
#
#   Simple tool to add and remove API keys
#   - not production ready, just to experiment!
#

import sqlite3
from pathlib import Path
import argparse

parser = argparse.ArgumentParser("Add API Authentication key")
parser.add_argument("-k", "--api-key", help="API Key", required=True)
parser.add_argument("-n", "--name", help="Client name", required=True)
parser.add_argument("-d", "--db_uri", help="Link to SQLite database file")
parser.add_argument("--remove", help="Remove this key", action="store_true")
args = parser.parse_args()

db_uri = args.db_uri or '%s/db/blocksmurfer-api-keys.db' % Path(__file__).parent.parent


try:
    with sqlite3.connect(db_uri, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        api_auth_record = (args.api_key, args.name)
        if not args.remove:
            sql = '''INSERT INTO api_auth_keys(auth_key, name) VALUES (?, ?);'''
            id = conn.execute(sql, api_auth_record)
            conn.commit()
            print("Added API Authentication Key for %s" % args.name)
        else:
            sql = '''DELETE FROM api_auth_keys WHERE auth_key=? and name=?;'''
            id = conn.execute(sql, api_auth_record)
            conn.commit()
            print("Executed delete statement for %s" % args.name)

except sqlite3.Error as e:
    print(e)
