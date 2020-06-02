import random

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

    BATTLE_EMOJI = {EMOJI_2: 2, EMOJI_3: 3, EMOJI_4: 4, EMOJI_5: 5}

    def __init__(self, bot):
        self._bot = bot
        self._battles = {}

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
        self._battles[msg.id] = battle

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Is it a reaction to the battle invitation?
        if reaction.message.id in self._battles:
            battle = self._battles[reaction.message.id]
            msg = battle.get_invite_message_object()

            emoji = Context.get_emoji_name(reaction)
            name = Context.get_nick_or_name(user=user)

            # Did someone join the battle?
            if emoji in BattleBot.BATTLE_EMOJI:
                for i in range(random.randint(13, 14)):
                    battle.add_player(name + str(i), BattleBot.BATTLE_EMOJI[emoji])

                await msg.edit(embed=battle.get_embed_playerlist())

            # Did an admin start the battle?
            elif reaction.emoji == BattleBot.EMOJI_OK:
                if 'admin' in [role.name for role in user.roles]:
                    battle.start()
                    _id = 0
                    for message, embed in battle.get_match_messages():
                        await msg.channel.send(message, embed=embed)
                        _id += 1
                        category = await msg.guild.create_category(name=str(_id - 1))
                        await msg.guild.create_voice_channel(name=str(_id - 1) + '-team1', category=category)
                        await msg.guild.create_text_channel(name=str(_id - 1) + '-team1', category=category)
                        await msg.guild.create_voice_channel(name=str(_id - 1) + '-team2', category=category)
                        await msg.guild.create_text_channel(name=str(_id - 1) + '-team2', category=category)

                    for ch in msg.guild.channels:
                        if ch.name.lower().find('team1') >= 0 or ch.name.lower().find('team2') >= 0:
                            await ch.delete()
                    await category.delete()


    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        pass
        # if reaction.message.id in self._battles:
        #     self._battles[reaction.message.id].remove_player(Context.get_nick_or_name(user=user))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.message.author.send(text(WRONG_ROLE))

