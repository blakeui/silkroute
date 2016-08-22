# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
"""Stocker API for interacting with Players, Goods in Market
"""
from silkroute.entity import Entity


class Stocker(Entity):
    def __init__(self, name, balance='0', location=None, reputation='0', database=None, tablename=None):
        """Stocker API for interacting with Players, Goods in Market
        """
        # Database Initialisation
        super(Stocker, self).__init__(name, type_='stocker', balance=balance,
                                      location=location, reputation=reputation, database=database)

    def transact(self, goods, other_id, transaction_type, event_type):
        return super(Stocker, self).transact(goods, other_id, transaction_type, event_type)
