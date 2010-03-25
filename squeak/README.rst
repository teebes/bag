******
Squeak
******

Python helper for sqlite3. Allows to drop & alter columns.

Sample usage for a sqlite3 database 'db' with the following table:

CREATE TABLE "my_table" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar (20) NOT NULL DEFAULT ""
);

Examples from the command line
==============================

To drop the 'name' column:

::

    $ squeak.py db my_table drop_column name

To rename the 'name' column to 'first_name':

::

    $ squeak.py db my_table rename_column name first_name

To allow the 'name' column to be null:

::

    $ squeak.py db my_table replace_definition name varchar \(20\)

Same examples from the python shell
===================================

To drop the 'name' column:

::

    >>> from squeak import Squeak
    >>> s = Squeak('db', 'my_table')
    >>> s.drop_column('name')

To rename the 'name' column to 'first_name':

::

    >>> from squeak import Squeak
    >>> s = Squeak('db', 'my_table')
    >>> s.drop_column('name')

To allow the 'name' column to be null:

::

    >>> from squeak import Squeak
    >>> s = Squeak('db', 'my_table')
    >>> s.replace_definition('name', 'varchar (20)')

Tests
=====

Squeak comes with a few unit tests. Just execute ``tests.py`` to run the suite.