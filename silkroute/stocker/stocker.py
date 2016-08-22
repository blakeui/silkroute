# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
"""Stocker - stocker interactions
"""
from silkroute.entity import Entity
from silkroute.seller import Seller
from silkroute.buyer import Buyer


class Stocker(Entity):
    def __init__(self, name, location=None, reputation='0', database=None, tablename=None):
        """Stocker API for interacting with Stocks, Market
        """
        # Database Initialisation
        super(Stocker, self).__init__(name, 'stocker', location, reputation=reputation, database=database)

    def transact(self, goods, other, transaction_type, event_type):
        # Find other in database
        other_in_db = self.DB.search('entity', {'ENTITY_ID': other})

        # Fail transaction if other not found
        if not len(other_in_db) > 0:
            return False

        # Create an object of the other party to interact with
        name, entity_type, location, reputation = other_in_db[0]
        entity_class = {'stocker': Stocker, 'buyer': Buyer, 'seller': Seller}[entity_type]
        other_entity = entity_class(name, location=location, reputation=reputation)

        # Pass other's object to super
        super(Stocker, self).transact(goods, other_entity, transaction_type, event_type)
