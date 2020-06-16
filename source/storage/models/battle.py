from source.storage.models.DBEntity import DBEntity


class DBBattle(DBEntity):
    def __init__(self, name: str):
        super().__init__(name)

        self.id = 0

    @staticmethod
    def create_table(db):
        db.create_table(
            'Battle',
            [
                ['id', 'INTEGER', 'PRIMARY KEY'],
                ['msg', 'INTEGER', 'UNIQUE'],
                ['date', 'TEXT', 'NOT NULL'],
                ['status', 'TEXT', 'NOT NULL']
            ])

    @staticmethod
    def insert(db, values: tuple):
        db.insert('Battle', ['msg', 'date'], values)

    @staticmethod
    def select(db, what: str, key: str, value: str):
        return db.select('Battle', what, key, value)
