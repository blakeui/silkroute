# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
"""Buyer - buyer interactions
"""
from silkroute.entity import Entity


class Buyer(Entity):
    def __init__(self, database=None):
        """Buyer API for interacting with Market
        """
        # Database Initialisation
        super(Entity, self).__init__(database, tablename='buyer')

    def buy(good):
        """buy goods from stocker into stock"""
        pass

    def search(stock):
        """search for goods in my area"""
        # search by item. search for item in neighbourhood
        # search by stocker. search stocker inventory
        pass
