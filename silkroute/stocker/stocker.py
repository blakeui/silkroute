# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
"""Stocker - stocker interactions
"""
from silkroute.entity import Entity


class Stocker(Entity):
    def __init__(self, name, location=None, reputation='0', database=None, tablename=None):
        """Stocker API for interacting with Stocks, Market
        """
        # Database Initialisation
        super(Stocker, self).__init__(name, 'stocker', location, reputation=reputation, database=database)

    def initiate(self, goods, amount, other, transaction_type):
        """initiate transaction(type_=buy, sell) with the other party"""
        # if other party is requesting to sell to us
        return self.transact(goods, amount, other, transaction_type=transaction_type, event_type='initiate')

    def respond(self, goods, amount, other, transaction_type):
        """respond to transaction request(type_=buy, sell) from other party"""
        return self.transact(goods, amount, other, transaction_type=transaction_type, event_type='respond')

    def search(self, goods):
        """search for goods in stock"""
        return self.DB.search(goods)
