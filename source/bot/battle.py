import random

import discord
from discord.ext import commands

from source.battle import Battle
from source.bot.context import Context
from source.util.util import check_date, log
from source.util.text import *


class BattleBot(commands.Cog):
    EMOJI_OK = '\U0001F44D'
    EMOJI_2 = '2v2'
    EMOJI_3 = '3v3'
    EMOJI_4 = '4v4'
    EMOJI_5 = '5v5'
    BATTLE_ADMIN = 'admin'
    BATTLE_COMMANDER = 'Battle Commander'

    BATTLE_EMOJI = {EMOJI_2: 2, EMOJI_3: 3, EMOJI_4: 4, EMOJI_5: 5}

    def __init__(self, bot):
        self._bot = bot
        self._battle_invites = {}
        self._battle_reports = {}

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
        battle = Battle(date, Context.get_nick_or_name(ctx), size)
        msg = await ctx.send(battle.get_invite_message(), embed=battle.get_invite_embed())
        battle.set_invite_message_object(msg)

        # Store battle with message id
        self._battle_invites[msg.id] = battle

    @commands.command(name='report',
                      aliases=['battlereport'],
                      help='bla')
    async def report(self, ctx, battle_id=None):
        log(Context.get_user_roles(ctx))
        if BattleBot.BATTLE_ADMIN in Context.get_user_roles(ctx):
            log(ctx.message.__repr__)
            log(str(ctx.message))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Is it a reaction to the battle invitation?
        if reaction.message.id in self._battle_invites:
            battle = self._battle_invites[reaction.message.id]
            msg = battle.get_invite_message_object()

            emoji = Context.get_emoji_name(reaction)
            name = Context.get_nick_or_name(user=user)

            # Did someone join the battle?
            if emoji in BattleBot.BATTLE_EMOJI:
                for i in range(random.randint(13, 36)):
                    battle.add_player(name + str(i), random.choice(list(BattleBot.BATTLE_EMOJI.values())))

                await msg.edit(embed=battle.get_embed_playerlist())

            # Did an admin start the battle?
            elif reaction.emoji == BattleBot.EMOJI_OK:
                if BattleBot.BATTLE_ADMIN in Context.get_user_roles(user=user):
                    battle.start()

                    for _, matches in battle.get_matches().items():
                        for match in matches:

                            color = discord.Colour(match.get_color())
                            commander = discord.Colour(0xcccc00)

                            await msg.channel.send(match.get_match_message(), embed=match.get_match_embed())
                            r1 = await msg.guild.create_role(name=match.get_role_name(1), color=color)
                            r2 = await msg.guild.create_role(name=match.get_role_name(2), color=color)
                            com = await msg.guild.create_role(name=text(MATCH_COMMANDER), color=commander)
                            cat = await msg.guild.create_category(name=match.get_category_name())
                            v1 = await msg.guild.create_voice_channel(name=match.get_channel_name(1), category=cat)
                            t1 = await msg.guild.create_text_channel(name=match.get_channel_name(1), category=cat)
                            v2 = await msg.guild.create_voice_channel(name=match.get_channel_name(2), category=cat)
                            t2 = await msg.guild.create_text_channel(name=match.get_channel_name(2), category=cat)

                            match.set_channels([cat, v1, t1, v2, t2])
                            match.set_roles([r1, r2, com])

                    for _, matches in battle.get_matches().items():
                        for match in matches:
                            for channel in match.get_channels():
                                await channel.delete()

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        pass
        # if reaction.message.id in self._battles:
        #     self._battles[reaction.message.id].remove_player(Context.get_nick_or_name(user=user))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.message.author.send(text(WRONG_ROLE))

