from source.util.util import get_config_from_json


class Offsets:
    def __init__(self, file, platform='GOG'):
        self._offsets = {}

        config = get_config_from_json(file)[platform]

        if config:
            self._offsets = config

    def __getitem__(self, item):
        if item in self._offsets:
            offset = self._offsets[item]
            return int(offset['OFFSET'], 16), int(offset['SIZE'], 16)
