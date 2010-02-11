#!/usr/bin/env python

import os
import re
import sqlite3
import sys
import unittest

from squeak import Squeak

class TestDropColumn(unittest.TestCase):
    
    db = 'testdb'

    def setUp(self):
        
        # clear previous test run
        try:
            os.remove('testdb')
        except OSError: pass
        
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        
        create_my_table = """
CREATE TABLE "my_table" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar (20) NOT NULL DEFAULT ""
)
;"""
    
        create_my_seat = """
CREATE TABLE "my_seat" (
    "id" integer NOT NULL PRIMARY KEY,
    "table" integer NOT NULL REFERENCES "my_table" ("id"),
    "type" varchar(10) NOT NULL DEFAULT ""
)
;"""
    
        populate_my_table_1 = """
INSERT INTO my_table (id, name) VALUES (1, 'abc')
;"""
    
        populate_my_table_2 = """
INSERT INTO my_table (id, name) VALUES (2, 'def')
;"""

        populate_my_seat_1 = """
INSERT INTO my_seat VALUES (1, 1, 'tall')
;"""

        populate_my_seat_2 = """
INSERT INTO my_seat VALUES (2, 1, 'short')
;"""

        cursor.execute(create_my_table)
        cursor.execute(create_my_seat)
        cursor.execute(populate_my_table_1)
        cursor.execute(populate_my_table_2)
        cursor.execute(populate_my_seat_1)
        cursor.execute(populate_my_seat_2)
        
        connection.commit()
        cursor.close()
    
    def tearDown(self):
        try:
            os.remove('testdb')
        except OSError: pass
    
    def test_drop_regular_column(self):
        cursor = sqlite3.connect(self.db).cursor()
        start = len(cursor.execute("SELECT * from my_table").fetchone())
        cursor.close()

        squeak = Squeak(self.db, 'my_table')
        squeak.drop_column('name')

        cursor = sqlite3.connect(self.db).cursor()
        end = len(cursor.execute("SELECT * from my_table").fetchone())
        cursor.close()
        
        return self.assert_(start == end + 1)

    def test_drop_foreign_key_column(self):
        cursor = sqlite3.connect(self.db).cursor()
        start = len(cursor.execute("SELECT * from my_seat").fetchone())
        cursor.close()

        squeak = Squeak(self.db, 'my_seat')
        squeak.drop_column('table')

        cursor = sqlite3.connect(self.db).cursor()
        end = len(cursor.execute("SELECT * from my_seat").fetchone())
        cursor.close()
        
        return self.assert_(start == end + 1)
        
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDropColumn)
    unittest.TextTestRunner(verbosity=2).run(suite)
