import sqlite3

from source.util.util import log


class DB:
    def __init__(self, db_file: str):
        super().__init__()

        self._connection = None
        self._statement = ''

        try:
            self._connection = sqlite3.connect(db_file)
        except Exception as e:
            log('init: {}'.format(e))

    def _print_statement(self):
        print(self._statement)

    def create_table(self, name: str, fields: list):
        self._statement = 'CREATE TABLE IF NOT EXISTS {0} ({1});'.format(
            name, ','.join([' '.join(field) for field in fields]))

        try:
            self._connection.cursor().execute(self._statement)
            self._connection.commit()
        except Exception as e:
            log('create_table: {}\n {}'.format(e, self._statement))

    def drop_table(self, name: str):
        self._statement = 'DROP TABLE {0};'.format(name)

        try:
            self._connection.cursor().execute(self._statement)
            self._connection.commit()
        except Exception as e:
            log('drop_table: {}\n {}'.format(e, self._statement))

    def insert(self, table: str, keys: list, values: tuple):
        self._statement = 'INSERT INTO {0} ({1}) VALUES {2};'.format(
            table, ','.join(keys), values)

        try:
            self._connection.cursor().execute(self._statement)
            self._connection.commit()
        except Exception as e:
            log('insert: {}\n {}'.format(e, self._statement))

    def update(self, table: str, keys: list, values: tuple, key: str, value: str):
        new_values = ','.join(['{0} = {1}'.format(str(k), str(v)) for k,v in zip(keys, values)])

        self._statement = 'UPDATE {0} SET {1} WHERE {2} = "{3}";'.format(
            table, new_values, key, value)

        try:
            self._connection.cursor().execute(self._statement)
            self._connection.commit()
        except Exception as e:
            log('update: {}\n {}'.format(e, self._statement))

    def insert_or_update(self, table: str, keys: list, values: tuple, key: str, value: str):
        try:
            result = self.select(table, keys, key, value)

            if not result:
                self.insert(table, keys, values)
            else:
                self.update(table, keys, values, key, value)

        except Exception as e:
            log('insert_or_update: {}\n {}'.format(e, self._statement))

    def select(self, table: str, what: list, key: str, value: str):
        self._statement = 'SELECT {0} FROM {1} WHERE {2}="{3}";'.format(
            ','.join(what), table, key, value)

        try:
            return self._connection.cursor().execute(self._statement).fetchall()
        except Exception as e:
            log('select: {}\n {}'.format(e, self._statement))

    def setup(self):
        pass

    def tear_down(self):
        pass
