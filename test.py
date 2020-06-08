# from source.storage.db import DB
# from source.storage.models.player import Player
#
# db = DB('test')
# Player.create_table(db)
# Player.insert(db, ('test', 20))

# import time
# from source.memory.process import Process
#
# OFFSETS = {
#     # KEY: (offset address, chunk size)
#     "SERVER_NAME": (0x0046AB30, 0xF0),
#     "PLAYER_KILL": (0x004F7A80, 0x60),
#     "PLAYER_NAME": (0x005048C4, 0x1C8),
#     "PLAYER_TEAM": (0x004F2034, 0x60), # not correct yet
# }
#
# class PlayerInfo:
#     def __init__(self):
#         self.name = ''
#         self.kills = 0
#         self.team = 0
#
#     def __str__(self):
#         return '{0} ({1}): {2}'.format(self.name, self.team, self.kills)
#
#
# p = Process('Battlefront.exe')
# player_count = 20
# players = [PlayerInfo] * player_count
#
# while True:
#     empty = True
#     for i in range(player_count):
#         name = p.read(0x005048C4 + i * 0x1C8, 50).value
#         kills = p.read(0x004F7A80 + i * 0x60, 1).value
#         team = p.read(0x004F2034 + i * 0x60, 1).value
#         if name:
#             empty = False
#     if not empty:
#         s = ''
#         for i in range(player_count):
#             s += str(players[i]) + ' | '
#         print(s)
#     time.sleep(1)


