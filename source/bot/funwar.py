import datetime
from random import shuffle

from discord.ext import commands

from source.bot.util import create_embed_table
from source.util.text import *
from source.war import get_map_entries


class BotWrapper(commands.Cog):
    def __init__(self, bot, fws, maps, players, teams):
        self.bot = bot
        self.fws = fws
        self.maps = maps
        self.players = players
        self.teams = teams

        bot.add_cog(self)

    @commands.command(name='stats?',
                      aliases=['stats'],
                      help=text(BOT_HELP_STATS))
    async def stats(self, ctx, stat_type, name=None):
        if stat_type.find('map') >= 0:
            headers = ['Map', 'Matches', 'Banns']
            entries = get_map_entries(self.maps, name)
        # elif stat_type.find('player') >= 0:
        #     headers = ['Player', 'Matches', 'Wins']
        #     entries = get_stats(self.players, name)
        # elif stat_type.find('team') >= 0:
        #     headers = ['Team', 'Players', '']
        #     entries = get_stats(self.teams, name)

        embed = create_embed_table('**Statistics**', headers=headers, entries=entries)

        await ctx.send('Here are some statistics', embed=embed)

    @commands.command(name='nextFW?',
                      aliases=['nextFW', 'nextfw?', 'nextfw'],
                      help=text(BOT_HELP_NEXT_FUNWAR))
    async def nextfunwar(self, ctx):
        _id, fw = self.fws.next()

        if _id is not None:
            if _id is not -1:
                msg = text(NEXT_FUNWAR).format(
                    _id,
                    fw['date'].strftime('%d.%m.%y %H:%M'),
                    fw['organizer'],
                    fw['size'] or 'X',
                    ', '.join(fw['members']))
            else:
                msg = text(FUNWARS_IN_PAST)
        else:
            msg = text(NO_FUNWAR)

        await ctx.send(msg)

    @commands.command(name='allfunwars?',
                      aliases=['allFW', 'allfw'],
                      help=text(BOT_HELP_ALL_FUNWARS))
    async def allfunwars(self, ctx):
        wars = self.fws.wars()

        if wars:
            msg = '\n**Funwars**:\n\n'
            for _id, fw in wars.items():
                msg += text(FUNWAR) + '\n'.format(
                    _id,
                    fw['date'].strftime('%d.%m.%y %H:%M'),
                    fw['organizer'],
                    fw['size'] or 'X',
                    ', '.join(fw['members']))
        else:
            msg = text(NO_FUNWAR)

        await ctx.send(msg)

    @commands.command(name='newfunwar',
                      aliases=['newFW', 'newfw'],
                      help=text(BOT_HELP_NEW_FUNWAR))
    async def newfunwar(self, ctx, fw_date: str, fw_time: str, fw_team_size: int = None):
        now = datetime.datetime.now()

        fw_date = fw_date.split('.')
        fw_time = fw_time.split(':')

        year = now.year if len(fw_date) < 3 else fw_date[2]
        month = fw_date[1]
        day = fw_date[0]

        minute = 0 if len(fw_time) < 2 else fw_time[1]
        hour = fw_time[0]

        date = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
        if date < now:
            msg = text(DATE_IN_PAST)
        else:
            name = ctx.message.author.nick if ctx.message.author.nick is not None else ctx.message.author.name
            fw_id = self.fws.add(date, fw_team_size, name)
            msg = text(NEW_FUNWAR).format(
                fw_id,
                date.strftime('%d.%m.%y %H:%M'),
                fw_team_size or 'X')

        await ctx.send(msg)

    @commands.command(name='joinfunwar',
                      aliases=['joinFW', 'joinfw'],
                      help=text(BOT_HELP_JOIN_FUNWAR))
    async def joinfunwar(self, ctx, _id):
        _id = int(_id)
        if _id in self.fws.wars():
            name = ctx.message.author.nick if ctx.message.author.nick is not None else ctx.message.author.name
            if self.fws.join(_id, name):
                fw = self.fws.wars()[_id]
                msg = text(JOIN_FUNWAR).format(
                    fw['date'].strftime('%d.%m.%y %H:%M'),
                    fw['size'] or 'X',
                    ', '.join(fw['members']))
            else:
                msg = text(ERROR)
        else:
            msg = text(NO_FUNWAR_WITH_ID)

        await ctx.send(msg)

    @commands.command(name='leavefunwar',
                      aliases=['leaveFW', 'leavefw'],
                      help=text(BOT_HELP_LEAVE_FUNWAR))
    async def leavefunwar(self, ctx, _id):
        _id = int(_id)
        if _id in self.fws.wars():
            name = ctx.message.author.nick if ctx.message.author.nick is not None else ctx.message.author.name
            if self.fws.leave(_id, name):
                fw = self.fws.wars()[_id]
                msg = text(LEAVE_FUNWAR).format(
                    fw['date'].strftime('%d.%m.%y %H:%M'),
                    fw['size'] or 'X')
            else:
                msg = text(ERROR)
        else:
            msg = text(NO_FUNWAR_WITH_ID)

        await ctx.send(msg)

    @commands.command(name='funwarteams',
                      aliases=['FWteams', 'fwteams'],
                      help=text(BOT_HELP_FUNWAR_TEAMS))
    async def funwarteams(self, ctx, _id):
        _id = int(_id)

        if _id in self.fws.wars():
            members = list(self.fws.wars()[_id]['members'])
            shuffle(members)
            team1 = ''
            team2 = ''
            for i, m in enumerate(members):
                if i % 2 == 0:
                    team1 += m + '\n'
                else:
                    team2 += m + '\n'

            msg = text(FUNWAR_TEAMS).format(team1, team2)

        else:
            msg = text(NO_FUNWAR_WITH_ID)

        await ctx.send(msg)

    @commands.command(name='clearfunwars',
                      aliases=['clearFW', 'clearfw'],
                      help=text(BOT_HELP_CLEAR_FUNWARS))
    @commands.has_role('admin')
    async def clearfunwars(self, ctx):
        self.fws.clear()
        await ctx.send(text(ALL_CLEAR))


