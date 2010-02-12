#!/usr/bin/env python

"""
Python helper for sqlite3. Allows to drop columns, alter columns and add a
not null constraint.

Usage from the command line:

$ ./squeak.py <db> <table_name> subcommand
Available subcommands:
  drop_column <db_name> <column_name> [safe]
  add_constraint not_null
  drop_constraint not_null
"""

import re
import sqlite3
import sys

class SqueakError(Exception): pass

class Squeak(object):

    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name
        self.connection = sqlite3.connect(self.db)
        
        cursor = self.connection.cursor()
        
        self.creation_sql = cursor.execute(
            "select sql from sqlite_master where tbl_name = ?;",
            (table_name,)
        ).fetchone()
        
        if not self.creation_sql:
            raise SqueakError("No such table: '%s'" % table_name)
            
        # -- parse the creation sql to get a list of field creation SQLs
        
        inline_creation_sql = ' '.join(self.creation_sql[0].split('\n'))
        
        # get the part of the query string that deals with fields
        fields = re.match(
            r'^create\s+table\s+["\']?\w+["\']?\s+\((?P<fields>.*)\)\s*$',
            inline_creation_sql, re.IGNORECASE
        ).group('fields')
        
        # remove the preceding blank spaces and split on ','
        # TODO: will need to beef up this formatting eventually as there
        # can be commas within clauses
        fields = [re.sub('^\s+', '', field) for field in fields.split(',')]
        
        self.fields = fields
        
        cursor.close()

    def drop_column(self, column_name, safe=False):
        #connection = sqlite3.connect(self.db)
        cursor = self.connection.cursor()

        # filter out the column that is no longer wanted and save the names
        # of the columns that will be copied
        columns = []
        new_fields = []
        found = False
        col_re = r'["\']?(?P<column>\w+)["\']?'
        for field in self.fields:
            column = re.match(col_re, field, re.IGNORECASE).group('column')
            if column == column_name:
                found = True
                continue
            else:
                columns.append(column)
                new_fields.append(field)
        
        # provided column doesn't exist
        if not found:
            return False, u"No such column: '%s'" % column_name
        
        # create the new creation line
        fields = ', '.join(new_fields)

        # create the temporary table
        cursor.execute("CREATE TABLE %s_tmp (%s);" % (self.table_name,
                                                      fields))

        # copy the filtered data to the temp table
        columns = map(lambda x: '"%s"' % x, columns)
        columns_arg = (', ').join(columns)
        cursor.execute("INSERT INTO %s_tmp (%s) "
                       "SELECT %s FROM %s;" % (self.table_name,
                                              columns_arg,
                                              columns_arg,
                                              self.table_name))

        if safe:
            # rename the initial table but keep it around
            cursor.execute("ALTER TABLE %s RENAME TO %s_initial;" % (
                                                            self.table_name,
                                                            self.table_name))
        else:
            # drop the initial table
            cursor.execute("DROP TABLE %s;" % self.table_name)

        # rename the temp table to the initial table
        cursor.execute("ALTER TABLE %s_tmp RENAME TO  %s;" % (self.table_name,
                                                              self.table_name))

        self.connection.commit()
        cursor.close()
        
        return True, u"Column '%s' droped" % column_name

def main():
    def print_usage():
        print ("Usage: squeak.py <db> <table_name> subcommand\n\n"
               "Available subcommands:\n"
               "  drop_column <db_name> <column_name> [safe]\n"
               "  rename_column <db_name> <old_column> <new_column>\n"
               "  add_constraint not_null\n"
               "  drop_constraint not_null")

    if len(sys.argv) < 3:
        print_usage()
        return
    
    try:
        squeak = Squeak(sys.argv[1], sys.argv[2])
    except SqueakError, e:
        print "Error: %s" % e
        return
    
    subcommand = sys.argv[3]
    if subcommand == 'drop_column':
        safe = False
        if len(sys.argv) >= 6:
            safe = True
        print squeak.drop_column(sys.argv[4], safe=safe)[1]
        return
    elif subcommand == 'add_constraint': pass
    elif subcommand == 'drop_constraint': pass
    else:
        print "Invalid subcommand: %s\n" % subcommand
        print_usage()
        return

if __name__ == '__main__':
    main()

"""
Copyright (c) 2010 Thibaud Morel l'Horset <teebes@teebes.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""