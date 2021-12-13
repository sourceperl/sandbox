#!/usr/bin/env python3

# basic example of sqlite3 with datetime type

from datetime import datetime
import sqlite3


# connect to DB store in example.db file with a dict factory (fetchall return list of dict)
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


db = sqlite3.connect('./example.db', detect_types=sqlite3.PARSE_DECLTYPES)
db.row_factory = dict_factory

# create a cursor on this connection
dbc = db.cursor()

# create table with a datetime field
dbc.execute('CREATE TABLE IF NOT EXISTS `events` '
            '(`id` INTEGER PRIMARY KEY AUTOINCREMENT, `datetime` TIMESTAMP, `message` TEXT)')

# populate it with messages
for i in range(3):
    dt = datetime.now()
    msg = f'my msg #{i:02d}'
    dbc.execute('INSERT INTO `events` (`datetime`, `message`) VALUES (?,?)', (dt, msg))

# commit all changes on DB and close it
db.commit()

# read today message from events table
dbc.execute("SELECT * FROM `events` WHERE date(`datetime`) = date('now')")
for r in dbc.fetchall():
    print(f"{str(r['datetime']):<32} \"{r['message']}\"")

db.close()
