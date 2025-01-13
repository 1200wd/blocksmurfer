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
parser.add_argument("-k", "--api-key", help="API Key")
parser.add_argument("-n", "--name", help="Client name")
parser.add_argument("-c", "--credits", help="Update or add credits")
parser.add_argument("-l", "--list", help="List all API keys", action="store_true")
parser.add_argument("-d", "--db_uri", help="Link to SQLite database file")
parser.add_argument("--remove", help="Remove this key", action="store_true")
args = parser.parse_args()

db_uri = args.db_uri or '%s/db/blocksmurfer-api-keys.db' % Path(__file__).parent.parent


try:
    with sqlite3.connect(db_uri, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        if args.list:
            sql = '''SELECT * FROM api_auth_keys;'''
            rows = conn.execute(sql).fetchall()
            conn.commit()
            for row in rows:
                print(row)
        if args.api_key and args.name:
            api_auth_record = (args.api_key, args.name, args.credits or 999999)
            if not args.remove:
                sql = '''INSERT INTO api_auth_keys(auth_key, name, credits) VALUES (?, ?, ?);'''
                id = conn.execute(sql, api_auth_record)
                conn.commit()
                print("Added API Authentication Key for %s" % args.name)
            else:
                sql = '''DELETE FROM api_auth_keys WHERE auth_key=? and name=?;'''
                id = conn.execute(sql, api_auth_record[:2])
                conn.commit()
                print("Executed delete statement for %s" % args.name)

except sqlite3.Error as e:
    print(e)
