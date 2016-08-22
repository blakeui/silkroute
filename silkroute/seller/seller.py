# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
"""Seller - seller interactions
"""
from silkroute.entity import Entity


class Seller(Entity):
    def __init__(self, database=None):
        """Seller API for interacting with Market
        """
        # Database Initialisation
        super(Entity, self).__init__(database, tablename='seller')

    def sell(self, goods, amount, buyer=None):
        """buy goods from stocker into stock"""
        # if seller is requesting to sell to us
        if buyer:
            return self.DB.upsert_row(self.tablename, goods, amount)
        # if seller agrees to sell to us
        elif buyer.sell(goods, amount):
            return self.DB.upsert_row(self.tablename, goods, amount)
        else:
            return False

    def stock(self, good):
        """stock goods with stocker"""
        pass

    def search(self, stocker):
        """search for stockers"""
        # search by item. search for item in neighbourhood
        # search by stocker. search stocker inventory
        pass
