import os
import pickle
import datetime


class Player:
    def __init__(self, player_id: int):
        self._matches = None
        self._teams = []


class Team:
    def __init__(self, players: list):
        self._players = players


class Funwar:
    def __init__(self, fw_id: int, fw_date: datetime.datetime):
        self._id = fw_id
        self._date = fw_date
        self._team_size = None
        self._players = []


class Funwars:
    def __init__(self, file):
        self._file = file
        self._fws = {}
        self._id = 0

        if not os.path.isfile(file):
            pickle.dump(self._fws, open(self._file, 'wb'))

        self._fws = pickle.load(open(file, 'rb'))
        if self._fws:
            self._id = max(self._fws, key=int) + 1

    def next(self):
        _next = None, None
        now = datetime.datetime.now()
        _min = datetime.datetime(now.year + 10, now.month, now.day) - now
        for _id, fw in self._fws.items():
            diff = fw['date'] - now
            if diff < _min:
                _min = diff
                _next = _id, fw

        if _min < now - now:
            return -1, None

        return _next

    def wars(self):
        return self._fws

    def clear(self):
        self._fws = {}
        self._id = 0

    def add(self, _date, _size, _organizer):
        _id = self._id
        self._fws[_id] = {'date': _date, 'size': _size, 'members': set(), 'organizer': _organizer}
        self._id += 1
        return _id

    def join(self, _id, _member):
        if _id in self._fws:
            self._fws[_id]['members'].add(_member)
            return True
        return False

    def leave(self, _id, _member):
        if _id in self._fws:
            self._fws[_id]['members'].remove(_member)
            return True
        return False

    def write(self):
        pickle.dump(self._fws, open(self._file, 'wb'))