from functools import reduce
from hashlib import sha1
from datetime import datetime
from time import time

import discord

from source.bot.context import Context
from source.util.text import *
from source.util.util import remove_from_list, log, get_max


class Match:
    def __init__(self, date, size):
        self._id = time()
        self._date = date
        self._match_id = sha1(str(reversed(str(self._id))).encode('UTF-8')).hexdigest()[0:6]
        self._size = size
        self._players = []
        self._roles = []
        self._channels = []
        self._results = []
        self._approvals = []
        self._commander1 = None
        self._team1 = []
        self._commander2 = None
        self._team2 = []

    #
    # Private
    #

    def _get_random_teams(self):
        team1, team2 = [], []
        players = list(set(self._players))

        for i, p in enumerate(players):
            if i % 2 == 0:
                team1.append(p)
            else:
                team2.append(p)

        return team1, team2

    #
    # Public
    #

    def add_player(self, player):
        self._players.append(player)

    def get_players(self):
        return self._players

    def get_id(self):
        return self._id

    def get_match_id(self):
        return self._match_id

    def get_color(self):
        return int(self._match_id, 16)

    def player_names(self):
        players = []
        for player in self._players:
            players.append(player.name)

    def get_commander(self, team):
        return self._commander1 if team == 1 else self._commander2

    def get_team(self, team):
        return self._team1 if team == 1 else self._team2

    def set_results(self, content: str):
        try:
            lines = []
            if content.find('\r\n') >= 0:
                lines = content.split('\r\n')
            elif content.find('\n') >= 0:
                lines = content.split('\n')

            for line in lines:
                map_name = ''
                if line.find(':') >= 0:
                    map_name, line = line.split(':')
                if line.find(' ') >= 0:
                    tickets = line.split(' ')
                    if len(tickets) >= 2:
                        self._results.append({'map': map_name,
                                              'team-1': int(tickets[-2]),
                                              'team-2': int(tickets[-1])})
        except:
            # Formatting error
            pass

    def player_mentions(self):
        players = []
        for player in self._players:
            players.append(player.mention)

    def get_category_name(self):
        return '{0}: {1}'.format(text(MATCH), self.get_match_id())

    def get_channel_name(self, team: int):
        return '{0}-{1}'.format(self.get_match_id(), idfy(text(MATCH_TEAM1)) if team == 1 else idfy(text(MATCH_TEAM2)))

    def set_channels(self, channels: list):
        self._channels = channels

    def get_channels(self):
        return self._channels

    def get_role_name(self, team: int):
        return '{0} {1}'.format(self.get_match_id(), text(MATCH_TEAM1) if team == 1 else text(MATCH_TEAM2))

    def get_commander_role_name(self, team: int):
        return '{0} {1} {2}'.format(self.get_match_id(), text(MATCH_COMMANDER), team)

    def set_roles(self, roles: list):
        self._roles = roles

    def get_roles(self):
        return self._roles

    def get_start_message(self):
        return b('{0} ({1}v{1}) - ID: {2}'.format(text(MATCH_START), self._size, self._match_id))

    def get_start_embed(self):
        embed = discord.Embed(title=b(text(MATCH)),
                              description=text(MATCH_START_MESSAGE),
                              color=Battle.COLOR_START)

        team1, team2 = self._get_random_teams()

        embed.add_field(name=b(text(MATCH_TEAM1)),
                        value='\n'.join(team1) or '-',
                        inline=True)

        embed.add_field(name=b(text(MATCH_TEAM2)),
                        value='\n'.join(team2) or '-',
                        inline=True)

        return embed

    def get_result_message(self):
        return b('{0} ({1}v{1}) - ID: {2}'.format(text(MATCH), self._size, self._match_id))

    def get_result_embed(self):
        embed = discord.Embed(title=b(text(MATCH_RESULT)),
                              description=text(MATCH_RESULT_MESSAGE),
                              color=Battle.COLOR_RESULT)

        for result in self._results:
            embed.add_field(name=text(EMPTY),
                            value='{0}: {1}-{2}'.format(b(result['map']), result['team-1'], result['team-2']),
                            inline=False)
        return embed


class Battle:
    COLOR_INVITE = 0x0088ff
    COLOR_START = 0xff8800
    COLOR_RESULT = 0x00ff88

    def __init__(self, date: datetime, organizer, size: str = None):
        self._open = True
        self._invite_msg_object = None
        self._date = date
        self._organizer = organizer
        self._sizes = []
        self._reactions = {4: [], 3: [], 5: [], 2: []}
        self._matches = {4: {}, 3: {}, 5: {}, 2: {}}

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

    def _calculate_reaction_pool(self):
        # Number of players for every type of match
        reactions = {4: len(self._reactions[4]),
                     3: len(self._reactions[3]),
                     5: len(self._reactions[5]),
                     2: len(self._reactions[2])}

        # Number of matches possible
        primary_matches = {4: int(reactions[4] / 8),
                           3: int(reactions[3] / 6)}
        secondary_matches = {5: int(reactions[5] / 10),
                             2: int(reactions[2] / 4)}

        return primary_matches, secondary_matches

    def _calculate_match_sizes(self, primary_matches, secondary_matches):
        # Look what type generates the biggest number of matches (4v4, 3v3)
        match_size, number_of_matches = get_max(primary_matches)

        # If no 4v4 or 3v3 can take place, choose 5v5 or 2v2
        if number_of_matches == 0:
            match_size, number_of_matches = get_max(secondary_matches)

        return match_size, number_of_matches

    def _remove_players_from_reaction_pool(self, players):
        for player in players:
            remove_from_list(self._reactions[4], player)
            remove_from_list(self._reactions[3], player)
            remove_from_list(self._reactions[5], player)
            remove_from_list(self._reactions[2], player)

    def _do_matchmaking(self):
        primary_matches, secondary_matches = self._calculate_reaction_pool()
        match_size, number_of_matches = self._calculate_match_sizes(primary_matches, secondary_matches)

        while number_of_matches > 0:

            for i in range(number_of_matches):
                match = Match(self._date, match_size)

                for j in range(match_size * 2):
                    player = self._reactions[match_size][j]
                    match.add_player(player)

                self._matches[match_size][match.get_match_id()] = match
                self._remove_players_from_reaction_pool(match.get_players())

            primary_matches, secondary_matches = self._calculate_reaction_pool()
            match_size, number_of_matches = self._calculate_match_sizes(primary_matches, secondary_matches)

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
                           name=b(text(PLAYERS)) + '({0})'.format(self.player_count()),
                           value=self.get_playerlist(),
                           inline=False)
        return embed

    def player_count(self):
        return reduce(lambda count, l: count + len(l), self._reactions.values(), 0)

    def add_player(self, player, size):
        self._reactions[size].append(player)

    def get_playerlist(self):
        return '\n'.join(['{0}v{0}: {1}'.format(b(k), ', '.join(v)) for k, v in self._reactions.items()])

    def get_matches(self):
        return self._matches

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
                        value=Context.get_nick_or_name(user=self._organizer),
                        inline=False)

        embed.add_field(name=b(text(PLAYERS)),
                        value=text(EMPTY),
                        inline=False)

        return embed
