import sqlite3


class DB:
    def __init__(self, db_file: str):
        super().__init__()

        self._connection = sqlite3.connect(db_file)

    def setup(self):
        pass

    def tear_down(self):
        pass


