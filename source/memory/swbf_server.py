class SWBFServer:
    def __init__(self, process, offsets):
        self._process = process
        self._offsets = offsets
        self._server = self._offsets['SERVER_NAME']
        self._capacity = self._offsets['SERVER_SLOT']
        self._name = self._offsets['PLAYER_NAME']
        self._kill = self._offsets['PLAYER_KILL']
        self._team = self._offsets['PLAYER_TEAM']
        self._online = {}
        self._current = 0
        self._info = {'name': '', 'capacity': 0}

        self._join_callback = None

        self._setup()

    def _setup(self):
        name = self._process.read(self._server[0], 50).value.decode('utf-8')
        capacity = self._process.read(self._capacity[0], 1).value

        if not capacity:
            capacity = 0
        else:
            capacity = capacity[0]

        self._info = {'name': name, 'capacity': capacity}

    def get_info(self):
        return self._info

    def update(self):
        for i in range(self._info['capacity']):
            name = self._process.read(self._name[0] + i * self._name[1], 50).value
            kills = self._process.read(self._kill[0] + i * self._kill[1], 1).value
            team = self._process.read(self._team[0] + i * self._team[0], 1).value
            print(name, kills, team)
            if name:
                if name not in self._online:
                    self._online[name] = {'kills': 0, 'team': 0}
                kills = self._process.read(self._kill[0] + i * self._kill[1], 1).value
                team = self._process.read(self._team[0] + i * self._team[0], 1).value
                self._online[name]['kills'] = kills
                self._online[name]['team'] = team

        if self._current != self.players_online():
            self._current = self.players_online()
            print(self._current)
            if self._join_callback:
                self._join_callback()

    def on_join(self, callback):
        self._join_callback = callback

    def players_online(self):
        return len(self._online)

    def name(self):
        return self._info['name']

    def slots(self):
        return self._info['capacity']
