# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:

from silkroute.stocker import Stocker


def test_stocker():
    stocker = Stocker('test_stocker', location='venice', database='/tmp/silkroute-stocker-test.db')
    assert stocker.name == 'test_stocker'
    assert stocker.type_ == 'stocker'
    assert stocker.reputation == '0'
    # assert_raises(sqlite3.OperationalError, stocker.cursor.execute, stocker.create_table)
