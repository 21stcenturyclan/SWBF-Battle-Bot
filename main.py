from threading import Thread

import time
import signal

from discord.ext import commands
from source.bot.battle import BattleBot
from source.util.util import log, get_key_from_ini_file


if __name__ == '__main__':

    KEY_DISCORD = get_key_from_ini_file('DISCORD2', 'keys.ini')
    bot = commands.Bot(command_prefix='!')
    bb = BattleBot(bot)

    t = Thread(target=bot.run, args=[KEY_DISCORD], daemon=True)
    t.start()

    def signal_handler(sig, frame):
        log('Ctrl+C!')
        exit(0)


    signal.signal(signal.SIGINT, signal_handler)
    while True:
        try:
            time.sleep(1)
        except Exception:
            pass
