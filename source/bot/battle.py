import discord
from discord.ext import commands

from source.battle import Battle, Match
from source.bot.context import Context
from source.storage.db import DB
from source.storage.models.player import DBPlayer
from source.util.settings import *
from source.util.util import check_date, log
from source.util.text import *


class BattleBot(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self._db = DB('BattleBot')
        self._battle_invites = {}
        self._match_confirmations = {}

        bot.add_cog(self)

        DBPlayer.create_table(self._db)

    #
    # Private
    #

    async def _setup(self, guild):
        await Context.get_or_create_role(text(MATCH_TEAM1), guild, discord.Colour(TEAM_1_COLOR))
        await Context.get_or_create_role(text(MATCH_TEAM2), guild, discord.Colour(TEAM_2_COLOR))
        await Context.get_or_create_role(text(MATCH_COMMANDER), guild, discord.Colour(COMMANDER_COLOR))

    async def _create_roles(self, guild, match):
        log('Create roles')
        try:
            match_role = await guild.create_role(name=match.get_role_name(0), color=discord.Colour(match.get_color()))
            team1 = await Context.get_or_create_role(text(MATCH_TEAM1), guild, discord.Colour(TEAM_1_COLOR))
            team2 = await Context.get_or_create_role(text(MATCH_TEAM2), guild, discord.Colour(TEAM_2_COLOR))
            commander = await Context.get_or_create_role(text(MATCH_COMMANDER), guild, discord.Colour(COMMANDER_COLOR))

            match.set_role(match_role)

            size = match.get_size()
            mid = match.get_match_id()

            log('  - assign roles')
            # Assign roles
            await match.get_commander(1).add_roles(commander)
            await match.get_commander(1).send(text(MATCH_COMMANDER_RESPONSIBLE))
            for player in match.get_team(1):
                await player.add_roles(match_role)
                await player.add_roles(team1)
                await player.send(text(PLAYER_TEAM_NOTICE).format(size, mid, 1, 'REB/CIS'))

            await match.get_commander(2).add_roles(commander)
            await match.get_commander(2).send(text(MATCH_COMMANDER_RESPONSIBLE))
            for player in match.get_team(2):
                await player.add_roles(match_role)
                await player.add_roles(team2)
                await player.send(text(PLAYER_TEAM_NOTICE).format(size, mid, 2, 'EMP/REP'))

        except Exception as e:
            log(e)

    async def _create_channels(self, guild, match):
        log('Create channels')
        try:
            match_role = match.get_role()
            bot_role = await Context.get_or_create_role(name=BOT_ROLE, guild=guild)
            team1 = await Context.get_or_create_role(name=text(MATCH_TEAM1), guild=guild, color=discord.Colour(TEAM_1_COLOR))
            team2 = await Context.get_or_create_role(name=text(MATCH_TEAM2), guild=guild, color=discord.Colour(TEAM_2_COLOR))

            log('  - set up permissions')
            permission_match = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                match_role:         discord.PermissionOverwrite(read_messages=True),
                bot_role:           discord.PermissionOverwrite(read_messages=True)
            }
            permission_team1 = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                team1:              discord.PermissionOverwrite(read_messages=True),
                bot_role:           discord.PermissionOverwrite(read_messages=True)
            }
            permission_team2 = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                team2:              discord.PermissionOverwrite(read_messages=True),
                bot_role:           discord.PermissionOverwrite(read_messages=True)
            }

            # Category
            cat = await guild.create_category(match.get_category_name(), overwrites=permission_match)

            # Global Channels
            voice0 = await guild.create_voice_channel(text(LOBBY), category=cat)
            text0 = await guild.create_text_channel(text(LOBBY), category=cat)

            # Team 1 Channels
            t1_name = text(MATCH_TEAM1) + ' (REB/CIS)'
            voice1 = await guild.create_voice_channel(t1_name, category=cat, overwrites=permission_team1)
            #text1 = await guild.create_text_channel(match.get_channel_name(1), category=cat, overwrites=permission_team1)

            # Team 2 Channels
            t2_name = text(MATCH_TEAM2) + ' (EMP/REP)'
            voice2 = await guild.create_voice_channel(t2_name, category=cat, overwrites=permission_team2)
            #text2 = await guild.create_text_channel(match.get_channel_name(2), category=cat, overwrites=permission_team2)

            log('  - set channels')
            #match.set_channels([voice0, text0, voice1, text1, voice2, text2, cat])
            match.set_channels([voice0, text0, voice1, voice2, cat])

        except Exception as e:
            log(e)

    #
    # Public
    #

    def exit(self):
        pass

    @commands.command(name='battle',
                      aliases=['newbattle'],
                      help='bla')
    @commands.has_any_role(*OrganizerRoles)
    async def battle(self, ctx, date: str, time: str, size: str = None):
        log('!battle: ', date, time, size)

        # Check Date
        date = check_date(date + ' ' + time)
        if not date:
            log('  - invalid date')
            await ctx.send(text(DATE_INVALID))

        # Create embed message
        log('  - send invite')
        battle = Battle(date, ctx.message.author, size)
        msg = await ctx.send(battle.get_invite_message(), embed=battle.get_invite_embed())
        battle.set_invite_message_object(msg)

        # Store battle with message id
        log('  - insert battle')
        self._battle_invites[msg.id] = battle

    @commands.command(name='report',
                      aliases=['battlereport', 'result'],
                      help='bla')
    @commands.has_any_role(*ReporterRoles)
    async def report(self, ctx, report_id: str, content: str = ''):
        log('!report', report_id, content)

        for _, battle in self._battle_invites.items():
            for size, matches in battle.get_matches().items():

                # It it a valid match id?
                if report_id in matches:
                    log('  - match id found')
                    if len(ctx.message.attachments) > 0:
                        content = await ctx.message.attachments[0].read()
                        content = content.decode("UTF-8")
                    match = matches[report_id]
                    match.set_results(content)

                    log('  - send result')
                    msg = await ctx.send(match.get_result_message(), embed=match.get_result_embed())
                    self._match_confirmations[msg.id] = match

    @commands.command(name='leaderboard',
                      aliases=['update'],
                      help='bla')
    @commands.has_any_role(*AdministratorRoles)
    async def leaderboard(self, ctx):
        log('!leaderboard')

        if len(ctx.message.attachments) > 0:
            content = await ctx.message.attachments[0].read()
            content = content.decode("UTF-8")

            try:
                i = 0
                for line in content:
                    nick, kills, deaths, cp, w, d, l, p = line.split(' ')

                    result = self._db.select(
                        'Player',
                        'kills, deaths, cp, wins, draws, losses',
                        'nick',
                        nick)

                    if not result:
                        result = (0, 0, 0, 0, 0, 0, 40)

                    self._db.insert_or_update(
                        'Player',
                        ['kills', 'deaths', 'cp', 'wins', 'draws', 'losses'],
                        (result[0] + kills,
                         result[1] + deaths,
                         result[2] + cp,
                         result[3] + w,
                         result[4] + d,
                         result[5] + l,
                         result[6] + p),
                        'nick',
                        nick)

                    i += 1

                log('All good updated {} entries!'.format(i))

            except Exception as e:
                log(e)

    @commands.command(name='stats',
                      aliases=['statistics'],
                      help='bla')
    @commands.has_any_role(*ParticipantRoles)
    async def stats(self, ctx, name: str):
        log('!stats')

        result = self._db.select('Player', '*', 'nick', name)
        await ctx.send(result)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        log('#add reaction')

        # Is it a reaction to the battle invitation?
        if reaction.message.id in self._battle_invites:
            battle = self._battle_invites[reaction.message.id]
            msg = battle.get_invite_message_object()
            emoji = Context.get_emoji_name(reaction)

            # Did someone join the battle?
            if emoji in BATTLE_EMOJI:
                log('  - join battle')
                battle.add_player(user, BATTLE_EMOJI[emoji])
                await msg.edit(embed=battle.get_embed_playerlist())

            # Did an admin start the battle?
            elif reaction.emoji == EMOJI_GOOD:
                if Context.has_any_role(user=user, roles=AdministratorRoles):
                    log('  - admin confirmation')
                    battle.start()

                    # TODO debug battle._matches[2]['123456'] = Match('20.05 20:30', 2)

                    for _, matches in battle.get_matches().items():
                        for _, match in matches.items():
                            log('  - start match')
                            match.start()
                            await msg.channel.send(match.get_start_message(), embed=match.get_start_embed())
                            await self._create_roles(msg.guild, match)
                            await self._create_channels(msg.guild, match)

                # Did someone agree to the battle
                elif Context.has_any_role(user=user, roles=ParticipantRoles):
                    battle.add_invite_approval()

        # Is it a reaction to the match result?
        if reaction.message.id in self._match_confirmations:
            # Did an admin approve the battle?
            if reaction.emoji == EMOJI_GOOD:
                if Context.has_any_role(user=user, roles=AdministratorRoles):
                    log('  - result confirmation')
                    match = self._match_confirmations[reaction.message.id]

                    match.store(self._db)

                    log('  - remove roles')
                    team1 = await Context.get_or_create_role(text(MATCH_TEAM1), reaction.message.guild)
                    team2 = await Context.get_or_create_role(text(MATCH_TEAM2), reaction.message.guild)
                    for player in match.get_players():
                        player.remove_roles([team1, team2])

                    log('  - delete role')
                    await match.get_role().delete()

                    channels = match.get_channels()
                    for channel in channels:
                        log('  - delete channel ', channel.name)
                        await channel.delete()

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        log('#remove reaction')

        if reaction.message.id in self._battle_invites:
            battle = self._battle_invites[reaction.message.id]
            msg = battle.get_invite_message_object()
            emoji = Context.get_emoji_name(reaction)

            # Did someone join the battle?
            if emoji in BATTLE_EMOJI:
                log('  - leave battle')
                battle.remove_player(user, BATTLE_EMOJI[emoji])
                await msg.edit(embed=battle.get_embed_playerlist())

            # Did some remove their approval
            elif reaction.emoji == EMOJI_GOOD:
                if Context.has_any_role(user=user, roles=ParticipantRoles):
                    battle.remove_invite_approval()


    @commands.Cog.listener()
    async def on_ready(self):
        log('Ready!')
        await self._setup(self._bot.guilds[0])

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.message.author.send(text(WRONG_ROLE))
