# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:

from silkroute.database import sqlDB
from nose.tools import assert_equal


def test_database():
    """Test DB CRUD"""

    # create database
    database = '/tmp/silkroute-test.db'
    # create table
    col_1 = {'name': 'TEST_ID', 'type': 'INT', 'properties': 'PRIMARY KEY NOT NULL'}
    col_2 = {'name': 'VALUE', 'type': 'CHAR(50)'}
    col_3 = {'name': 'VALUE2', 'type': 'CHAR(50)'}

    with sqlDB(database) as db:
        db.create_table('test', cols=[col_1, col_2, col_3])
        # insert
        db.upsert_row('test', {'TEST_ID': '12', 'VALUE': 'TEST1', 'VALUE2': 'TEST11'})
        # update
        db.upsert_row('test', {'TEST_ID': '12', 'VALUE': 'TEST2', 'VALUE2': 'TEST12'})
        # search
        assert_equal(db.search('test', {'TEST_ID': '12'}, cols=('VALUE')), [(u'TEST2',)])
        # delete and verify
        db.delete('test', {'TEST_ID': '12'})
        assert_equal(db.search('test', {'TEST_ID': '212'}, cols=('VALUE')), [])
