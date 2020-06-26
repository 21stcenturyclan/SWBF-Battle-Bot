import re

ID = 0


def text_id():
    global ID
    ID += 1
    return ID


BOT_HELP_STATS = text_id()
BOT_HELP_NEXT_FUNWAR = text_id()
BOT_HELP_ALL_FUNWARS = text_id()
BOT_HELP_JOIN_FUNWAR = text_id()
BOT_HELP_LEAVE_FUNWAR = text_id()
BOT_HELP_NEW_FUNWAR = text_id()
BOT_HELP_FUNWAR_TEAMS = text_id()
BOT_HELP_CLEAR_FUNWARS = text_id()
ERROR = text_id()
EMPTY = text_id()
DATE = text_id()
LOBBY = text_id()
ORGANIZER = text_id()
PLAYERS = text_id()
PLAYER_TEAM_NOTICE = text_id()
MATCH = text_id()
MATCH_START = text_id()
MATCH_RESULT = text_id()
MATCH_COMMANDER = text_id()
MATCH_COMMANDER_RESPONSIBLE = text_id()
BATTLE = text_id()
BATTLE_INVITATION = text_id()
BATTLE_COMMANDER = text_id()
MATCH_TEAM1 = text_id()
MATCH_TEAM2 = text_id()
BATTLE_2v2 = text_id()
BATTLE_3v3 = text_id()
BATTLE_4v4 = text_id()
BATTLE_5v5 = text_id()
WRONG_ROLE = text_id()
DATE_INVALID = text_id()
DATE_IN_PAST = text_id()
NO_ENTRY = text_id()
ALL_CLEAR = text_id()
NO_FUNWAR = text_id()
NO_FUNWAR_WITH_ID = text_id()
FUNWAR = text_id()
FUNWARS_IN_PAST = text_id()
NEXT_FUNWAR = text_id()
NEW_FUNWAR = text_id()
JOIN_FUNWAR = text_id()
LEAVE_FUNWAR = text_id()
FUNWAR_TEAMS = text_id()
DATE_FORMAT_EU = text_id()
BATTLE_REACTION_REQUEST = text_id()
MATCH_START_MESSAGE = text_id()
MATCH_RESULT_MESSAGE = text_id()

TEXTS = {
    BOT_HELP_STATS:              str('Shows stats. (Available in the private chat)\n'
                                     'maps\n'
                                     'players\n'
                                     'teams\n'),
    BOT_HELP_NEXT_FUNWAR:        'Shows the next planned funwar. (Available in the private chat)',
    BOT_HELP_ALL_FUNWARS:        'Shows all planned funwars. (Available in the private chat)',
    BOT_HELP_JOIN_FUNWAR:        'You will join the specified Funwar. (Only available in the server channel chat)',
    BOT_HELP_LEAVE_FUNWAR:       'You will leave the specified Funwar. (Only available in the server channel chat)',
    BOT_HELP_NEW_FUNWAR:         str('Create a new funwar with date, time, and team size. '
                                     '[Admin command] (Only available in the server chat)\n'
                                     'Format: \'day.month.year\' \'hour:minute\'\n'
                                     'Examples: 16.06.2020 18:35 5\n'
                                     '          16.06 20:0 3\n'
                                     '          5.6 20 \n'),
    BOT_HELP_FUNWAR_TEAMS:       'Creates random teams for the specified Funwar. (Only available in the server chat)',
    BOT_HELP_CLEAR_FUNWARS:      'Removes all funwars. [Admin command] (Only available in the server chat)',
    EMPTY:                       '\u200b',
    PLAYERS:                     'Players',
    PLAYER_TEAM_NOTICE:          str('You will take part in the {0} match ({1}). '
                                     'You are part of team {2}. '
                                     'Team {2} will play {3} first!'),
    LOBBY:                       'Lobby',
    MATCH:                       'Match',
    MATCH_START:                 'Match Start',
    MATCH_RESULT:                'Match Result',
    MATCH_COMMANDER:             'Match Commander',
    MATCH_COMMANDER_RESPONSIBLE: str('You have been appointed as Match Commander. '
                                     'You are responsible that your team takes screenshots! '
                                     'One of the two match commanders has to post the result.'),
    BATTLE:                      'Battle',
    BATTLE_INVITATION:           'Battle Invitation',
    BATTLE_COMMANDER:            'Battle Commander',
    MATCH_TEAM1:                 'Team 1',
    MATCH_TEAM2:                 'Team 2',
    BATTLE_2v2:                  '2v2',
    BATTLE_3v3:                  '3v3',
    BATTLE_4v4:                  '4v4',
    BATTLE_5v5:                  '5v5',
    DATE:                        'Date',
    ORGANIZER:                   'Organizer',
    ERROR:                       'Ops, something went wrong.',
    WRONG_ROLE:                  'You do not have the correct role for this command.',
    DATE_IN_PAST:                'Ops, this date lies in the past, try again.',
    NO_ENTRY:                    'There is no entry for that name.',
    NO_FUNWAR:                   'There is no Funwar.',
    NO_FUNWAR_WITH_ID:           'There is no Funwar with this ID.',
    FUNWARS_IN_PAST:             'All Funwars lie in the past.',
    DATE_FORMAT_EU:              '%d.%m.%Y %H:%M',
    FUNWAR:                      str('ID: {0}\n'
                                     'Date: {1}\n'
                                     'Organizer: {2}\n'
                                     'Teamsize: {3}v{3}\n'
                                     'Members: {4}'),
    NEXT_FUNWAR:                 str('Next Funwar:\n'
                                     'ID: {0}\n'
                                     'Date: {1}\n'
                                     'Organizer: {2}\n'
                                     'Teamsize: {3}v{3}\n'
                                     'Members: {4}'),
    NEW_FUNWAR:                  str('New Funwar:\n'
                                     'ID: {0}\n'
                                     'Date: {1}\n'
                                     'Teamsize: {2}v{2}'),
    JOIN_FUNWAR:                 str('You joined the Funwar at {0} ({1}v{1}).\n'
                                     'Members: {2}'),
    LEAVE_FUNWAR:                'You left the Funwar at {0} ({1}v{1}).',
    FUNWAR_TEAMS:                str('Teams:\n'
                                     '**Team 1**:\n{0}\n\n'
                                     '**Team 2**:\n{1}'),
    BATTLE_REACTION_REQUEST:     'Please react with the team size emoji(s).',
    MATCH_START_MESSAGE:         str('Let the battle begin!\n'
                                     'Here are the teams.\n'),
    MATCH_RESULT_MESSAGE:        str('Here are the results!\n'
                                     'Please react with the designated emoji.\n')
}


def text(text_id):
    return TEXTS[text_id]


def idfy(t):
    return re.sub('\s', '-', t)


def b(t):
    return '**{0}**'.format(t)


def c(t):
    return '`{0}`'.format(t)


def cb(t):
    return '```{0}```'.format(t)
