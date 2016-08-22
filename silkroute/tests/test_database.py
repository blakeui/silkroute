# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:

from silkroute.database import sqlDB
from nose.tools import assert_equal


def test_database():
    """Test DB CRUD"""

    # create database
    database = sqlDB('/tmp/silkroute-test.db')
    # create table
    col_1 = {'name': 'TEST_ID', 'type': 'INT', 'properties': 'PRIMARY KEY NOT NULL'}
    col_2 = {'name': 'VALUE', 'type': 'CHAR(50)'}
    print database.create_table('test', cols=[col_1, col_2])
    # insert
    database.upsert_row('test', {'TEST_ID': '12', 'VALUE': 'TEST'})
    # update
    database.upsert_row('test', {'TEST_ID': '12', 'VALUE': 'TEST2'})
    # search
    assert_equal(database.search('test', {'TEST_ID': '12'}, cols=('VALUE')), [(u'TEST2',)])
    # delete and verify
    database.delete('test', {'TEST_ID': '12'})
    assert_equal(database.search('test', {'TEST_ID': '212'}, cols=('VALUE')), [])
