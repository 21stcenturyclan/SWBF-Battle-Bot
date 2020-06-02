from threading import Thread

import time
import signal

from discord.ext import commands
from source.war import transform_data
from source.funwar import Funwars
from source.bot.battle import BattleBot
from source.util.util import log, get_key_from_ini_file

FW_FILE = 'funwars_dm'
KEY_DISCORD = get_key_from_ini_file('DISCORD2', 'keys.ini')

fws = Funwars(FW_FILE)
players, teams, maps = transform_data('wars.json')
# bot = commands.Bot(command_prefix='!')
bot = commands.Bot(command_prefix='!')
# cog = BotWrapper(bot2, fws, maps, players, teams)
bb = BattleBot(bot)

# t1 = Thread(target=bot.run, args=[KEY_DISCORD], daemon=True)
# t1.start()
t2 = Thread(target=bot.run, args=[KEY_DISCORD], daemon=True)
t2.start()

def signal_handler(sig, frame):
    log('Ctrl+C!')
    fws.write()
    exit(0)


signal.signal(signal.SIGINT, signal_handler)

while True:
    try:
        time.sleep(1)
    except Exception:
        pass
