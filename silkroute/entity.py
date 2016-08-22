# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
"""Entity - stocker, seller, buyer base interactions
"""
from abc import abstractmethod
from .database import sqlDB
from .goods import Goods


class Entity(object):
    def __init__(self, entity_name, type_, balance='0', location='nowhere',
                 reputation='0', database=None, tablename='entity'):
        """Stocker API for interacting with Stocks, Market
        """
        # Initialize variable
        self.name = entity_name
        self.location = location
        self.type_ = type_
        self.reputation = reputation
        self.balance = balance
        self.database = database

        # Initialise/Connect to database
        self.tablename = tablename
        self.columns = [{'name': 'ENTITY_ID', 'type': 'CHAR(50)', 'properties': 'PRIMARY KEY  NOT NULL'},
                        {'name': 'TYPE', 'type': 'INT'},
                        {'name': 'BALANCE', 'type': 'INT'},
                        {'name': 'LOCATION', 'type': 'CHAR(50)'},
                        {'name': 'REPUTATION', 'type': 'INT'}]

        with sqlDB(self.database) as db:  # Create self table if doesn't exist
            db.create_table(self.tablename, cols=self.columns)

            # Insert self into table
            db.upsert_row(tablename, {'ENTITY_ID': entity_name, 'TYPE': type_, 'BALANCE': balance,
                                      'LOCATION': location, 'REPUTATION': reputation})

    def transact(self, goods, other_id, transaction_type, event_type):
        # wrap other parties class around their name if they exist
        other = self.db_to_entity_class(other_id)
        if not other:
            return False

        # if transaction initiated by us, request response from other party(=> send SYN)
        if event_type == 'initiate':

            # if other party agrees to transact with us(=> recieved SYNACK)
            if other.respond(goods, self.name, transaction_type):

                # fail if transaction not possible
                if not self.valid(goods, transaction_type, from_=self, to=other):
                    return False

                # update both entity states (done at single point to keep transaction atomic)
                self.update(goods, transaction_type, from_=self, to=other)
                # update goods state
                Goods(self.database).update(goods, transaction_type, from_=self, to=other)
                # send ACK to other party
                return True

        # else if other party requests a transaction with us, evaluate request
        elif event_type == 'respond':

            # send SYNACK if we agree to request
            if self.evaluate_offer(goods, other, transaction_type):
                return True

        # if we're here means the transaction failed
        return False

    def db_to_entity_class(self, other):
        from .buyer import Buyer
        from .seller import Seller
        from .stocker import Stocker
        entity_dict = {'stocker': Stocker, 'buyer': Buyer, 'seller': Seller}

        # Find other in database
        with sqlDB(self.database) as db:
            other_in_db = db.search('entity', {'ENTITY_ID': other})

        # Fail transaction if other not found
        if not len(other_in_db) > 0:
            return False

        # Create an object of the other party to interact with
        name, entity_type, balance, location, reputation = other_in_db[0]
        entity_class = entity_dict[entity_type]
        other_entity = entity_class(name.encode('utf-8'), location=location.encode('utf-8'), balance=balance,
                                    reputation=reputation, database=self.database, tablename=self.tablename)
        return other_entity

    def valid(self, goods, transaction_type, to, from_):
        """test if 'to' has the money and 'from_' has the goods
        """
        # test if item exists in marketplace
        goods_in_db = Goods(self.database).search(goods)
        if not goods_in_db:
            return False

        goods_id, name, cost, current_owner, current_location = goods_in_db

        # test if entity buying has the money to procure goods
        if transaction_type == 'buy' and to.balance < cost:
            return False
        # test if item belongs to entity selling
        if transaction_type == 'sell' and current_owner != from_:
            return False

        # if we've reached here then the transaction seems plausible
        return True

    def update(self, goods, transaction_type, from_, to):
        goods_id, name, cost, current_owner, current_location = Goods(self.database).search(goods)
        if transaction_type == 'buy':
            with sqlDB(self.database) as db:
                # seller gains money
                db.upsert_row(self.tablename,
                              {'ENTITY_ID': to.entity_name, 'TYPE': to.type_, 'BALANCE': to.balance + cost,
                               'LOCATION': to.location, 'REPUTATION': to.reputation})
                # buyer loses money
                db.upsert_row(self.tablename,
                              {'ENTITY_ID': from_.entity_name, 'TYPE': from_.type_, 'BALANCE': from_.balance - cost,
                               'REPUTATION': from_.reputation, 'LOCATION': from_.location})
        elif transaction_type == 'sell':
            with sqlDB(self.database) as db:
                # buyer loses money
                db.upsert_row(self.tablename,
                              {'ENTITY_ID': to.entity_name, 'TYPE': to.type_, 'BALANCE': to.balance - cost,
                               'REPUTATION': to.reputation, 'LOCATION': to.location})
                # seller gains money
                db.upsert_row(self.tablename,
                              {'ENTITY_ID': from_.entity_name, 'TYPE': from_.type_, 'BALANCE': from_.balance + cost,
                               'REPUTATION': from_.reputation, 'LOCATION': from_.location})

    def initiate(self, goods, other, transaction_type):
        """initiate transaction(type_=buy, sell) with the other party"""
        # if other party is requesting to sell to us
        return self.transact(goods, other, transaction_type=transaction_type, event_type='initiate')

    def respond(self, goods, other, transaction_type):
        """respond to transaction request(type_=buy, sell) from other party"""
        return self.transact(goods, other, transaction_type=transaction_type, event_type='respond')

    def search(self, entity_id):
        with sqlDB(self.database) as db:
            entity_in_db = db.search('entity', {'ENTITY_ID': entity_id})
        if len(entity_in_db) < 1:
            return None
        else:
            return entity_in_db[0]

    @abstractmethod
    def evaluate_offer(self, goods, other, transaction_type):
        """evaluate if transaction is in self. interest"""
        return True
