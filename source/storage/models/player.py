from source.storage.models.DBEntity import DBEntity


class DBPlayer(DBEntity):
    TABLE = 'Player'

    def __init__(self, name: str):
        super().__init__(name)

        self.id = 0
        self.name = ''
        self.kills = 0
        self.deaths = 0
        self.cps = 0
        self.wins = 0
        self.losses = 0
        self.draw = 0
        self.tickets = 0
        self.matches = 0
        self.skirmishes = 0

    @staticmethod
    def create_table(db):
        db.create_table(
            DBPlayer.TABLE,
            [
                ['id', 'INTEGER', 'PRIMARY KEY'],
                ['name', 'TEXT'],
                ['nick', 'TEXT', 'NOT NULL'],
                ['kills', 'INTEGER'],
                ['deaths', 'INTEGER'],
                ['cp', 'INTEGER'],
                ['kd', 'FLOAT'],
                ['wins', 'INTEGER'],
                ['draws', 'INTEGER'],
                ['points', 'FLOAT'],
                ['losses', 'INTEGER'],
                ['tickets', 'INTEGER'],
                ['battles', 'INTEGER'],
                ['matches', 'INTEGER'],
            ])

    @staticmethod
    def insert(db, keys: list, values: tuple):
        db.insert(DBPlayer.TABLE, keys, values)

    @staticmethod
    def update(db, keys: list, values: tuple, key: str, value: str):
        db.update(DBPlayer.TABLE, keys, values, key, value)

    @staticmethod
    def select(db, what: str, key: str, value: str):
        return db.select(DBPlayer.TABLE, what, key, value)
