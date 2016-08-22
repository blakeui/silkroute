# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
"""Entity - stocker, seller, buyer base interactions
"""
from .database import sqlDB
from abc import abstractmethod


class Entity(object):
    def __init__(self, entity_name, type_, location=None, reputation='0', database=None, tablename='entity'):
        """Stocker API for interacting with Stocks, Market
        """
        # Initialise/Connect to database
        self.name = entity_name
        self.location = location
        self.type_ = type_
        self.reputation = reputation
        self.DB = sqlDB(database)
        self.tablename = tablename
        self.columns = [{'name': 'ENTITY_ID', 'type': 'CHAR(50)', 'properties': 'PRIMARY KEY  NOT NULL'},
                        {'name': 'TYPE', 'type': 'INT'},
                        {'name': 'LOCATION', 'type': 'INT'},
                        {'name': 'REPUTATION', 'type': 'INT'}]
        self.DB.create_table(self.tablename, cols=self.columns)
        self.DB.upsert_row(tablename, {'ENTITY_ID': entity_name, 'REPUTATION': self.reputation, 'LOCATION': location})

    def transact(self, goods, amount, other, transaction_type, event_type):
        # if transaction initiated by us, request response from other party(=> send SYN)
        if event_type == 'initiate':
            # Find other in database
            other_in_db = self.DB.search('entity', {'ENTITY_ID': other})

            # Fail transaction, if other not found
            if not len(other_in_db) > 0:
                return False

            # Create an object of the other party to interact with
            name, entity_type, location, reputation = other_in_db[0]
            other_object = Entity(name, entity_type, location=location, reputation=reputation)

            # if other party agrees to transact with us(=> recieved SYNACK)
            if other_object.respond(goods, amount, self, transaction_type):
                # update goods state
                goods.update(goods, amount, transaction_type, initiator=self, responder=other_object)
                self.DB.upsert_row(self.tablename, goods, amount, transaction_type)
                # send ACK to other party
                return True

        # else if other party requests a transaction with us, evaluate request
        elif event_type == 'respond':
            # send SYNACK if we agree to request
            if self.validate(goods, amount, transaction_type):
                return True
        # if we're here means the transaction failed
        return False

    @abstractmethod
    def validate(goods, amount, other):
        """evaluate if transaction is possible and beneficial to self"""
        pass
