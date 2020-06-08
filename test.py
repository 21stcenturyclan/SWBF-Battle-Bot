# from source.storage.db import DB
# from source.storage.models.player import Player
#
# db = DB('test')
# Player.create_table(db)
# Player.insert(db, ('test', 20))

import time
from source.memory.process import Process
from source.util.util import get_config_from_json


class PlayerInfo:
    def __init__(self):
        self.name = ''
        self.kills = 0
        self.team = 0

    def __str__(self):
        return '{0} ({1}): {2}'.format(self.name, self.team, self.kills)


p = Process('Battlefront.exe')
player_count = 20
current_players = 0
players = [PlayerInfo] * player_count
offsets = get_config_from_json('offsets.json')['GOG']

name_offset = int(offsets['PLAYER_NAME']['OFFSET'], 16)
name_size = int(offsets['PLAYER_NAME']['SIZE'], 16)
kill_offset = int(offsets['PLAYER_KILL']['OFFSET'], 16)
kill_size = int(offsets['PLAYER_KILL']['SIZE'], 16)
team_offset = int(offsets['PLAYER_TEAM']['OFFSET'], 16)
team_size = int(offsets['PLAYER_TEAM']['SIZE'], 16)

print(name_offset)

while True:
    players_on_servers = 0
    for i in range(player_count):
        name = p.read(name_offset + i * name_size, 50).value
        kills = p.read(kill_offset + i * kill_size, 1).value
        team = p.read(team_offset + i * team_size, 1).value
        print(name, kills, team)
        if name:
            players_on_servers += 1
    if players_on_servers > 0:
        if current_players != players_on_servers:
            current_players = players_on_servers
            print('Players on server: ' + str(current_players))
        s = ''
        for i in range(player_count):
            s += str(players[i]) + ' | '
        print(s)
    time.sleep(1)


