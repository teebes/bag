******
Squeak
******

What is it?
===========

Squeak is a script and helper library for alterine Sqlite3 tables.

* Contained in only 1 file, very easy to get via wget or curl

* Both a straight forward executable script and a library that can be used by other scripts

Examples
========

Here is an example of how Squeak might be used as an executable::

    $ sqlite3 db
    SQLite version 3.6.12
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite> CREATE TABLE "my_table" (
       ...>     "id" integer NOT NULL PRIMARY KEY,
       ...>     "name" varchar (20) NOT NULL DEFAULT ""
       ...> )
       ...> ;
    sqlite> .quit

    $ ./squeak.py db my_table drop_column name
    Column 'name' droped

    $ sqlite3 db
    SQLite version 3.6.12
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite> .schema
    CREATE TABLE "my_table" ("id" integer NOT NULL PRIMARY KEY);
    sqlite> .quit

