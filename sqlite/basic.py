#!/usr/bin/env python3

# basic example of sqlite3 (standard python module)
#
# useful packages for editing sqlite DB:
#     sudo apt install sqlite3 sqlitebrowser

from random import randint
import sqlite3


# connect to DB store in example.db file
db = sqlite3.connect('./example.db')

# create a cursor on this connection
dbc = db.cursor()

# create table (if not already exist) with a primary key 'id'
dbc.execute('CREATE TABLE IF NOT EXISTS `test` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `value` TEXT)')
# populate it with random values
for _ in range(1_000):
   v = randint(0, 0xFFFF_FFFF_FFFF_FFFF)
   dbc.execute(f"INSERT INTO `test` (`value`) VALUES ('{v:016x}')")

# commit all changes on DB and close it
db.commit()
db.close()
