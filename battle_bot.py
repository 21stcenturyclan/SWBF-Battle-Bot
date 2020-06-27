import signal
import threading
import time

from discord.ext import commands
from source.bot.battle import BattleBot
from source.util.util import log, get_key_from_ini_file


if __name__ == '__main__':

    KEY_DISCORD = get_key_from_ini_file('DISCORD_TEST', 'keys.ini')
    bot = commands.Bot(command_prefix='!')
    bb = BattleBot(bot)


    def signal_handler(sig, frame):
        bb.exit()
        log('Ctrl+C!')
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    t = threading.Thread(target=bot.run, args=[KEY_DISCORD], daemon=True)
    t.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            exit(0)
            break
