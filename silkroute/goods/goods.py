# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
"""Goods - goods interactions
"""
from silkroute.database import sqlDB


class Goods():
    def __init__(self, database=None, tablename='goods'):
        """Goods API for interacting with goods in marketplace
        """

        # Create/Connect to Database
        self.DB = sqlDB(database)
        self.tablename = tablename
        self.columns = [{'name': 'GOODS_ID', 'type': 'INTEGER', 'properties': 'PRIMARY KEY'},
                        {'name': 'NAME', 'type': 'CHAR(50)'},
                        {'name': 'COST', 'type': 'INT'},
                        {'name': 'OWNER', 'type': 'CHAR(50)'},
                        {'name': 'LOCATION', 'type': 'CHAR(50)'}]

        # Create table if doesn't exist
        self.DB.create_table(self.tablename, cols=self.columns)

    @staticmethod
    def update(self, goods, transaction_type, to=None, from_=None):
        """update state of goods
        """
        if not to or from_:
            raise ValueError

        # search for goods in marketplace
        goods_id, name, cost, current_owner, current_location = self.search(goods)
        if transaction_type == 'stock':
            self.upsert({goods_id, name, cost, current_owner, to.location})
        elif transaction_type == 'buy':
            self.upsert({goods_id, name, cost, from_, from_.location})
        elif transaction_type == 'sell':
            self.upsert({goods_id, name, cost, to, to.location})

    def search(self, key):
        goods_in_db = self.DB.search('goods', {'NAME': key})
        if len(goods_in_db) < 1:
            return None
        else:
            return goods_in_db[0]

    def valid(self, goods, transaction_type, to=None, from_=None):
        goods_in_db = self.search(goods)
        # if goods exist in the marketplace
        if goods_in_db:
            return True
        else:
            return False

    def upsert(self, goods_name, cost, owner, location=''):
        return self.DB.upsert_row(self.tablename, {'NAME': goods_name, 'COST': cost,
                                                   'OWNER': owner, 'LOCATION': location})
