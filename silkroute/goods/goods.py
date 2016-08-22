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
        self.database = database
        self.tablename = tablename
        self.columns = [{'name': 'GOODS_ID', 'type': 'INTEGER', 'properties': 'PRIMARY KEY'},
                        {'name': 'NAME', 'type': 'CHAR(50)'},
                        {'name': 'COST', 'type': 'INT'},
                        {'name': 'OWNER', 'type': 'CHAR(50)'},
                        {'name': 'LOCATION', 'type': 'CHAR(50)'}]

        # Create table if doesn't exist
        with sqlDB(self.database) as db:
            db.create_table(self.tablename, cols=self.columns)

    def update(self, goods, transaction_type, to='nowhere', from_='nowhere'):
        """update state of goods
        """
        if not to or not from_:
            raise ValueError

        # search for goods in marketplace
        goods_id, name, cost, current_owner, current_location = self.search(goods)
        if transaction_type == 'stock':
            self.upsert(name, cost, current_owner, location=to.location, goods_id=goods_id)
        elif transaction_type == 'buy':
            self.upsert(name, cost, from_, location=from_.location, goods_id=goods_id)
        elif transaction_type == 'sell':
            self.upsert(name, cost, to, location=to.location, goods_id=goods_id)

    def search(self, key):
        """search for item by name in marketplace"""
        with sqlDB(self.database) as db:
            goods_in_db = db.search(self.tablename, {'NAME': key})
        if len(goods_in_db) < 1:
            return None
        else:
            return goods_in_db[0]

    def valid(self, goods, transaction_type=None, to='nowhere', from_='nowhere'):
        """test if items exists in marketplace"""
        return (self.search(goods) != None)

    def upsert(self, goods_name, cost, owner, location='nowhere', goods_id=None):
        """update or insert goods row"""
        # if item exists append its GOODS_ID to upsert_row_
        upsert_row_ = {'NAME': goods_name.encode('utf-8'), 'COST': cost,
                       'OWNER': owner.encode('utf-8'), 'LOCATION': location}
        if not goods_id:
            goods_row = Goods(self.database, tablename=self.tablename).search('goods_name')
            if goods_row:
                upsert_row_['GOODS_ID'] = goods_row[0]
        # upsert to item into DB
        with sqlDB(self.database) as db:
            goods_id = db.upsert_row(self.tablename, upsert_row_)
        # return item row_id
        return goods_id
