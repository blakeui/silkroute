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
        self.columns = [{'name': 'GOODS_ID', 'type': 'INT', 'properties': 'PRIMARY KEY  NOT NULL'},
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
            self.DB.upsert_row(self.tablename,
                               {'GOODS_ID': goods_id, 'GOODS_NAME': name,
                                'OWNER': current_owner, 'LOCATION': to.location})
        elif transaction_type == 'buy':
            self.DB.upsert_row(self.tablename,
                               {'GOODS_ID': goods_id, 'GOODS_NAME': name,
                                'OWNER': from_, 'LOCATION': from_.location})
        elif transaction_type == 'sell':
            self.DB.upsert_row(self.tablename,
                               {'GOODS_ID': goods_id, 'GOODS_NAME': name,
                                'OWNER': to, 'LOCATION': to.location})

    @staticmethod
    def search(self, key):
        goods_in_db = self.DB.search('goods', {'GOODS_ID': key})
        if len(goods_in_db) < 1:
            return None
        else:
            return goods_in_db[0]

    @staticmethod
    def valid(self, goods, transaction_type, to, from_):
        goods_in_db = self.search(goods)
        # if goods exist in the marketplace
        if goods_in_db:
            return True
        else:
            return False
