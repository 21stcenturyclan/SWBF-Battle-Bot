import json


def transform_data(file):
    content = dict(json.load(open(file, 'r')))
    players = {}
    teams = {}
    maps = {}

    for fwar in content['funwars']:
        team_1 = fwar['team-1']
        team_2 = fwar['team-2']

        teams[team_1['name']] = team_1
        teams[team_2['name']] = team_2

        winner_team = 0
        if not fwar['draw']:
            winner_team = 1 if fwar['winner'] == 'team-1' else 2

        for player in team_1['players']:
            if player not in players:
                players[player] = {'wins': 0, 'losses': 0, 'draws': 0, 'tickets': 0, 'teams': []}

            # Add win/loss stats
            if winner_team == 0:
                players[player]['draws'] += 1
            elif winner_team == 1:
                players[player]['wins'] += 1
            else:
                players[player]['losses'] += 1

            # Add team
            players[player]['teams'].append(team_1['name'])

            # Add tickets
            players[player]['tickets'] += fwar['tickets'][0]

        for player in team_2['players']:
            if player not in players:
                players[player] = {'wins': 0, 'losses': 0, 'draws': 0, 'tickets': 0, 'teams': []}

            # Add win/loss stats
            if winner_team == 0:
                players[player]['draws'] += 1
            elif winner_team == 2:
                players[player]['wins'] += 1
            else:
                players[player]['losses'] += 1

            # Add team
            players[player]['teams'].append(team_2['name'])

            # Add tickets
            players[player]['tickets'] += fwar['tickets'][1]

        for m in fwar['maps']:
            if m['name'] not in maps:
                maps[m['name']] = {'choices': 0, 'matches': 0}

            maps[m['name']]['choices'] += 1

            if m['match-2']:
                maps[m['name']]['matches'] += 2
            else:
                maps[m['name']]['matches'] += 1

    return players, teams, maps


def get_map_entries(collection, name=None):
    entries = []
    if name in collection:
        m = collection[name]
        entries.append([name, m['choices'], m['matches']])
    else:
        for m in collection:
            v = collection[m]
            entries.append([m, v['choices'], v['matches']])
    return entries
