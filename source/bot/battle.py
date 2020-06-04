import random

import discord
from discord.ext import commands

from source.battle import Battle
from source.bot.context import Context
from source.util.util import check_date, log
from source.util.text import *


class BattleBot(commands.Cog):
    EMOJI_GOOD = '\U0001F44D'
    EMOJI_BAD = '\U0001F44E'
    EMOJI_2 = '2v2'
    EMOJI_3 = '3v3'
    EMOJI_4 = '4v4'
    EMOJI_5 = '5v5'
    BATTLE_ADMIN = 'admin'
    BATTLE_COMMANDER = 'Battle Commander'
    MATCH_COMMANDER = 'Match Commander'

    BATTLE_EMOJI = {EMOJI_2: 2, EMOJI_3: 3, EMOJI_4: 4, EMOJI_5: 5}

    def __init__(self, bot):
        self._bot = bot
        self._battle_invites = {}
        self._match_confirmations = {}

        bot.add_cog(self)

    @commands.command(name='battle',
                      aliases=['newbattle'],
                      help='bla')
    async def battle(self, ctx, date: str, time: str, size: str = None):
        # Check Date
        date = check_date(date + ' ' + time)
        if not date:
            await ctx.send(text(DATE_INVALID))

        # Create embed message
        battle = Battle(date, ctx.message.author, size)
        msg = await ctx.send(battle.get_invite_message(), embed=battle.get_invite_embed())
        battle.set_invite_message_object(msg)

        # Store battle with message id
        self._battle_invites[msg.id] = battle

    @commands.command(name='report',
                      aliases=['battlereport'],
                      help='bla')
    async def report(self, ctx, report_id: str, content: str=''):
        roles = Context.get_user_roles(ctx)
        if BattleBot.MATCH_COMMANDER in roles or BattleBot.BATTLE_ADMIN in roles:
            for msg_id, battle in self._battle_invites.items():
                for size, matches in battle.get_matches().items():
                    # It it a valid match id?
                    if report_id in matches:
                        if len(ctx.message.attachments) > 0:
                            content = await ctx.message.attachments[0].read()
                            content = content.decode("UTF-8")
                        match = matches[report_id]
                        match.set_results(content)

                        msg = await ctx.send(match.get_result_message(), embed=match.get_result_embed())
                        self._match_confirmations[msg.id] = match

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Is it a reaction to the battle invitation?
        if reaction.message.id in self._battle_invites:
            battle = self._battle_invites[reaction.message.id]
            msg = battle.get_invite_message_object()
            emoji = Context.get_emoji_name(reaction)

            # Did someone join the battle?
            if emoji in BattleBot.BATTLE_EMOJI:
                battle.add_player(user, BattleBot.BATTLE_EMOJI[emoji])
                await msg.edit(embed=battle.get_embed_playerlist())

            # Did an admin start the battle?
            elif reaction.emoji == BattleBot.EMOJI_GOOD:
                if BattleBot.BATTLE_ADMIN in Context.get_user_roles(user=user):
                    battle.start()

                    for _, matches in battle.get_matches().items():
                        for _, match in matches.items():

                            match.start()
                            await msg.channel.send(match.get_start_message(), embed=match.get_start_embed())

                            # Roles
                            team_color = discord.Colour(match.get_color())
                            com_color = discord.Colour(0xcccc00)
                            r1 = await msg.guild.create_role(name=match.get_role_name(1), color=team_color)
                            r2 = await msg.guild.create_role(name=match.get_role_name(2), color=team_color)
                            com1 = await msg.guild.create_role(name=match.get_commander_role_name(1), color=com_color)
                            com2 = await msg.guild.create_role(name=match.get_commander_role_name(2), color=com_color)

                            await match.get_commander(1).add_roles(com1)
                            for player in match.get_team(1):
                                await player.add_roles(r1)

                            await match.get_commander(2).add_roles(com2)
                            for player in match.get_team(2):
                                await player.add_roles(r2)

                            # Channels
                            cat = await msg.guild.create_category(name=match.get_category_name())
                            v1 = await msg.guild.create_voice_channel(name=match.get_channel_name(1), category=cat)
                            t1 = await msg.guild.create_text_channel(name=match.get_channel_name(1), category=cat)
                            v2 = await msg.guild.create_voice_channel(name=match.get_channel_name(2), category=cat)
                            t2 = await msg.guild.create_text_channel(name=match.get_channel_name(2), category=cat)

                            channels = [v1, t1, v2, t2, cat]
                            permission = {
                                msg.guild.default_role: discord.PermissionOverwrite(read_messages=True),
                                r1: discord.PermissionOverwrite(read_messages=True),
                                r2: discord.PermissionOverwrite(read_messages=True)
                            }

                            for channel in channels:
                                await channel.set_permissions(overwrite=permission)

                            match.set_channels(channels)
                            match.set_roles([r1, r2, com1, com2])

        # Is it a reaction to the match result?
        if reaction.message.id in self._match_confirmations:
            # Did an admin approve the battle?
            if reaction.emoji == BattleBot.EMOJI_GOOD:
                if BattleBot.BATTLE_ADMIN in Context.get_user_roles(user=user):
                    match = self._match_confirmations[reaction.message.id]
                    for channel in match.get_channels():
                        await channel.delete()
                    for role in match.get_roles():
                        await role.delete()

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        pass
        # if reaction.message.id in self._battles:
        #     self._battles[reaction.message.id].remove_player(Context.get_nick_or_name(user=user))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.message.author.send(text(WRONG_ROLE))

