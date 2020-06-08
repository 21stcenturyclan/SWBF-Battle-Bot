import sqlite3


class DB:
    def __init__(self, db_file: str):
        super().__init__()

        try:
            self._connection = sqlite3.connect(db_file)
        except Exception as e:
            print(e)

    def create_table(self, name: str, fields: list):
        statement = 'CREATE TABLE IF NOT EXISTS {0} ({1});'.format(
            name, ','.join([' '.join(field) for field in fields]))

        print(statement)

        try:
            res = self._connection.cursor().execute(statement)
            print(res)
        except Exception as e:
            print(e)

    def drop_table(self, name: str):
        statement = 'DROP TABLE {0};'.format(name)

    def insert(self, table: str, keys: list, values: tuple):
        statement = 'INSERT INTO {0} ({1}) VALUES {2};'.format(table, ','.join(keys), values)

        print(statement)

        try:
            res = self._connection.cursor().execute(statement)
            print(res)
        except Exception as e:
            print(e)

    def setup(self):
        pass

    def tear_down(self):
        pass
