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
        self._online_num = 0
        self._current = 0
        self._info = {'name': '', 'capacity': 0}

        self._join_callback = None
        self._leave_callback = None

        self._setup()

    def _setup(self):
        name = self._process.read(self._server[0], 50).value.decode('utf-8')
        capacity = self._process.read(self._capacity[0], 1).value

        if not capacity:
            capacity = 0
        else:
            capacity = capacity[0]

        self._info = {'name': name, 'capacity': capacity}

    def process(self):
        return self._process

    def get_info(self):
        return self._info

    def update(self):
        self._online_num = 0
        for i in range(self._info['capacity']):
            name = self._process.read(self._name[0] + i * self._name[1], 50).value
            kills = self._process.read(self._kill[0] + i * self._kill[1], 1).value
            team = self._process.read(self._team[0] + i * self._team[0], 1).value
            if name:
                self._online_num += 1
                if name not in self._online:
                    self._online[name] = {'kills': 0, 'team': 0}
                kills = self._process.read(self._kill[0] + i * self._kill[1], 1).value
                team = self._process.read(self._team[0] + i * self._team[0], 1).value
                self._online[name]['kills'] = kills
                self._online[name]['team'] = team

        # if self._current != self.players_online():
        #
        #     if self._current > self.players_online():
        #         if self._join_callback:
        #             self._join_callback(self)
        #
        #     elif self._current < self.players_online():
        #         if self._leave_callback:
        #             self._leave_callback(self)
        #
        #     self._current = self.players_online()

    def has_changed(self):
        changed = False
        if self._current != self._online_num:
            changed = True

        if changed:
            self._current = self._online_num

        return changed

    def on_join(self, callback):
        self._join_callback = callback

    def on_leave(self, callback):
        self._leave_callback = callback

    def players_online(self):
        return self._online_num

    def player_names(self):
        return [x.decode('utf-8') for x in list(self._online.keys())]

    def name(self):
        return self._info['name']

    def slots(self):
        return self._info['capacity']
