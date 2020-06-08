class Player:
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
            'Player',
            [
                ['id', 'INTEGER', 'PRIMARY KEY'],
                ['name', 'TEXT', 'NOT NULL'],
                ['kills', 'INTEGER']
            ])

    @staticmethod
    def insert(db, values: tuple):
        db.insert('Player', ['name', 'kills'], values)
