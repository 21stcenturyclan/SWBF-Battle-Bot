import random
import operator
from datetime import datetime

import discord

from source.util.text import *
from source.util.util import remove_from_list, log


class Battle:
    COLOR_INVITE = 0x0088ff
    COLOR_START = 0xff8800

    def __init__(self, date: datetime, organizer: str, size: str = None):
        self._open = True
        self._invite_msg_object = None
        self._date = date
        self._organizer = organizer
        self._sizes = []
        self._players = set()
        self._match_reactions = {4: [], 3: [], 5: [], 2: []}
        self._matches = {4: [], 3: [], 5: [], 2: []}

        self._set_size(size)

    #
    # Private
    #

    def _set_size(self, size):
        if size:
            sizes = map(int, size.split(','))
            for s in sizes:
                if s in [2, 3, 4, 5]:
                    self._sizes.append(s)

        else:
            self._sizes = [2, 3, 4, 5]

    def _get_sizes_text(self):
        sizes = []
        for s in self._sizes:
            sizes.append('{0}v{0}'.format(s))
        return ', '.join(sizes)

    def _do_matchmaking(self):
        # Number of players for every type of match
        p = {4: len(self._match_reactions[4]),
             3: len(self._match_reactions[3]),
             5: len(self._match_reactions[5]),
             2: len(self._match_reactions[2])}

        # Number of matches possible
        m1 = {4: int(p[4] / 8),
              3: int(p[3] / 6)}
        m2 = {5: int(p[5] / 10),
              2: int(p[2] / 4)}

        # Look what type generates the biggest number of matches (4v4, 3v3)
        optimal = max(m1.items(), key=operator.itemgetter(1))[0]
        if m1[optimal] > 0:
            for i in range(m1[optimal]):
                match = set()
                for j in range(optimal * 2):
                    player = self._match_reactions[optimal][j]
                    match.add(player)
                self._matches[optimal].append(match)
                for player in match:
                    remove_from_list(self._match_reactions[4], player)
                    remove_from_list(self._match_reactions[3], player)
                    remove_from_list(self._match_reactions[5], player)
                    remove_from_list(self._match_reactions[2], player)

        # Look what type generates the biggest number of matches (5v5, 2v2)
        optimal = max(m2.items(), key=operator.itemgetter(1))[0]
        if m2[optimal] > 0:
            for player in self._match_reactions[optimal]:
                remove_from_list(self._match_reactions[4], player)
                remove_from_list(self._match_reactions[3], player)
                remove_from_list(self._match_reactions[5], player)
                remove_from_list(self._match_reactions[2], player)

        log(m1)
        log(m2)
        log(self._match_reactions)
        log(self._matches)

    def _get_random_teams(self, players):
        team1, team2 = [], []
        players = list(set(players))

        for i, p in enumerate(players):
            if i % 2 == 0:
                team1.append(p)
            else:
                team2.append(p)

        return team1, team2

    #
    # Public
    #

    def set_invite_message_object(self, msg):
        self._invite_msg_object = msg

    def get_invite_message_object(self):
        return self._invite_msg_object

    def get_embed_playerlist(self):
        embed = self._invite_msg_object.embeds[0]
        embed.set_field_at(3,
                           name=b(text(PLAYERS)) + '({0})'.format(len(self._players)),
                           value=self.get_playerlist(),
                           inline=False)
        return embed

    def player_count(self):
        return len(self._players)

    def add_player(self, player, size):
        self._players.add(player)
        self._match_reactions[size].append(player)

    def get_playerlist(self):
        return ', '.join(self._players)

    def remove_player(self, player):
        if player in self._players:
            self._players.remove(player)

    def start(self):
        self._do_matchmaking()

    def get_invite_message(self):
        return b(text(BATTLE))

    def get_invite_embed(self):
        embed = discord.Embed(title=b(text(BATTLE)),
                              description=text(BATTLE_REACTION_REQUEST),
                              color=Battle.COLOR_INVITE)

        embed.add_field(name=b(text(DATE)),
                        value=self._date.strftime(text(DATE_FORMAT_EU)),
                        inline=False)

        embed.add_field(name='**Team sizes**:',
                        value=self._get_sizes_text(),
                        inline=False)

        embed.add_field(name=b(text(ORGANIZER)),
                        value=self._organizer,
                        inline=False)

        embed.add_field(name=b(text(PLAYERS)),
                        value=text(EMPTY),
                        inline=False)

        return embed

    def get_match_messages(self):
        messages = []

        for size in self._matches:
            for match in self._matches[size]:
                embed = discord.Embed(title=b(text(BATTLE)),
                                      description=text(BATTLE_START_MESSAGE),
                                      color=Battle.COLOR_START)

                team1, team2 = self._get_random_teams(match)

                embed.add_field(name=b(text(BATTLE_TEAM1)),
                                value='\n'.join(team1) or '-',
                                inline=True)

                embed.add_field(name=b(text(BATTLE_TEAM2)),
                                value='\n'.join(team2) or '-',
                                inline=True)
                messages.append([b('{0}v{0}'.format(size)), embed])

        return messages

    def get_start_message(self):
        return b(text(BATTLE))

    def get_start_embed(self):
        embed = discord.Embed(title=b(text(BATTLE)),
                              description=text(BATTLE_START_MESSAGE),
                              color=Battle.COLOR_START)

        team1, team2 = self._get_random_teams(self._matches[4][0])

        embed.add_field(name='**4v4**:',
                        value='\n'.join(self._matches[4][0]) or '-',
                        inline=False)

        embed.add_field(name=b(text(BATTLE_TEAM1)),
                        value='\n'.join(team1) or '-',
                        inline=True)

        embed.add_field(name=b(text(BATTLE_TEAM2)),
                        value='\n'.join(team2) or '-',
                        inline=True)

        return embed
