from os.path import dirname, join
import sqlite3

default_database = join(dirname(__file__), '.silkroute.db')


class sqlDB():
    def __init__(self, database=None):
        """Initialise Database"""
        self.database = database or default_database
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def create_table(self, tablename, cols=None):
        """Create table in database with specified columns"""
        columns = []
        for col in cols:
            if 'properties' in col:
                columns.append('{name} {type} {properties}'.format(**col))
            else:
                columns.append('{name} {type}'.format(**col))
        column_string = '(' + ','.join(columns) + ')'
        create_table_string = 'CREATE TABLE IF NOT EXISTS {t_name} '.format(t_name=tablename) + column_string
        self.cursor.execute(create_table_string)

    def upsert_row(self, tablename, data):
        """Update or Insert data into table in database"""
        columns = str(data.keys())[1:-1]
        values = str(data.values())[1:-1]
        query_string = 'INSERT OR REPLACE INTO {t_name} ({columns}) VALUES ({values})'
        upsert_string = query_string.format(t_name=tablename, columns=columns, values=values)
        self.cursor.execute(upsert_string)
        return self.cursor.execute('SELECT last_insert_rowid();').fetchone()[0]

    def search(self, tablename, k_dict, cols=None):
        """Search for row in db identified by k_dict return cols"""
        if not cols:
            cols = '*'
        key = k_dict.keys()[0]
        value = k_dict.values()[0].decode('utf-8')
        query_string = 'SELECT {cols} from {t_name} where {key} = ?'
        search_query = query_string.format(t_name=tablename, cols=cols, key=key)
        return self.cursor.execute(search_query, (value,)).fetchall()

    def delete(self, tablename, k_dict):
        """Delete row in db identified by k_dict"""
        delete_string = "DELETE FROM {t_name} WHERE {key} = {value}"
        delete_query = delete_string.format(t_name=tablename, key=k_dict.keys()[0], value=k_dict.values()[0])
        return self.cursor.execute(delete_query)
