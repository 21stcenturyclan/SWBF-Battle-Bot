from source.storage.db import DB
from source.storage.models.player import DBPlayer

db = DB('test')
# DBPlayer.create_table(db)
# DBPlayer.insert(db, ('test', 20))
# DBPlayer.insert(db, ('test', 40))
# DBPlayer.insert(db, ('test', 60))
print(DBPlayer.select(db, '*', 'name', 'test'))

