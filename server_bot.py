import signal
import threading
import time

from discord.ext import commands
from source.bot.server import ServerBot
from source.util.util import log, get_key_from_ini_file


if __name__ == '__main__':
    KEY_DISCORD = get_key_from_ini_file('DISCORD_TEST', 'keys.ini')
    bot = commands.Bot(command_prefix='!')
    sb = ServerBot(bot)

    def signal_handler(sig, frame):
        sb.exit()
        log('Ctrl+C!')
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    bot_thread = threading.Thread(target=bot.run, args=[KEY_DISCORD], daemon=True)
    bot_thread.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            exit(0)
            break
