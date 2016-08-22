# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:

from silkroute.goods import Goods
from nose.tools import assert_equal

test_market = Goods(database='/tmp/silkroute-goods-test.db')


def test_upsert():
    apple_id = test_market.upsert('apple', '3', 'batman', 'gotham')
    assert_equal(apple_id, 1)
    test_market.upsert('pineapple', '5', 'joker', 'gotham')
    test_market.upsert('bananas', '2', 'superman', 'metropolis')


def test_search():
    goods_id, name, cost, owner, location = test_market.search('apple')
    assert_equal((cost, owner, location), (3, 'batman', 'gotham'))
    assert_equal(test_market.search('bagel'), None)


def test_valid():
    assert_equal(test_market.valid('bananas', 'buy'), True)
    assert_equal(test_market.valid('brownie', 'buy'), False)
