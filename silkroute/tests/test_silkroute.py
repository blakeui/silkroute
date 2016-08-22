#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_silkroute
----------------------------------

Tests for `silkroute` module.
"""

from nose.tools import assert_equal
from click.testing import CliRunner

from silkroute import cli
from silkroute.goods import Goods
from silkroute.buyer import Buyer
from silkroute.seller import Seller
from silkroute.stocker import Stocker


class TestSilkroute(object):

    def __init__(self):
        self.database = '/tmp/silkroute-test2.db'
        self.market = None
        self.stocker = None
        self.stocker = None
        self.stocker = None

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        market = Goods(database=self.database)
        stocker = Stocker('batman', location='gotham', database=self.database)
        buyer = Buyer('superman', balance='3', location='metropolis', database=self.database)
        seller = Seller('sauron', location='mordor', database=self.database)
        market.upsert('bananas', '2', 'sauron', 'mordor')
        assert_equal(stocker.transact('bananas', 'superman', 'stock', 'initiate'), True)
        assert_equal(stocker.transact('bananas', 'sauron', 'stock', 'initiate'), True)
        assert_equal(buyer.transact('bananas', 'sauron', 'buy', 'initiate'), False)
        assert_equal(seller.transact('bananas', 'sauron', 'sell', 'initiate'), False)

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'silkroute.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    @classmethod
    def teardown_class(cls):
        pass
