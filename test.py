# from source.storage.db import DB
# from source.storage.models.player import Player
#
# db = DB('test')
# Player.create_table(db)
# Player.insert(db, ('test', 20))

import time

from source.memory.offsets import Offsets
from source.memory.process import Process
from source.memory.swbf_server import SWBFServer


process = Process('Battlefront.exe')
offsets = Offsets('offsets.json')
server = SWBFServer(process, offsets)


while True:
    server.update()
    time.sleep(1)


