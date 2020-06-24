class DBEntity:
    @staticmethod
    def create_table(db):
        raise NotImplemented

    @staticmethod
    def insert(db, keys: list, values: tuple):
        raise NotImplemented

    @staticmethod
    def select(db, what: str, key: str, value: str):
        raise NotImplemented