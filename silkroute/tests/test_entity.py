from silkroute.entity import Entity
from silkroute.goods import Goods
from nose.tools import assert_equal

database = '/tmp/silkroute-entity-test.db'
test_entity = Entity('batman', type_='stocker', location='gotham', database=database)
test_market = Goods(database=database)


def test_upsert():
    pass


def test_search():
    entity_id, type_, balance, location, reputation = test_entity.search('batman')
    assert_equal((type_, balance, location, reputation), ('stocker', 0, 'gotham'.decode('utf-8'), 0))


def test_valid():
    pass
