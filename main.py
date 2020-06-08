import signal

from discord.ext import commands
from source.bot.battle import BattleBot
from source.util.util import log, get_key_from_ini_file


def signal_handler(sig, frame):
    log('Ctrl+C!')
    exit(0)


if __name__ == '__main__':

    KEY_DISCORD = get_key_from_ini_file('DISCORD2', 'keys.ini')
    bot = commands.Bot(command_prefix='!')
    BattleBot(bot)
    signal.signal(signal.SIGINT, signal_handler)

    bot.run(KEY_DISCORD)
