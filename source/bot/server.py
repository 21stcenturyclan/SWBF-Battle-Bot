import time

import pythoncom
import wmi

from discord.ext import commands

from source.memory.offsets import Offsets
from source.memory.process import Process
from source.memory.swbf_server import SWBFServer


class ServerBot(commands.Cog):

    def __init__(self, bot):
        self._is_init = False
        self._ready = False
        self._bot = bot
        self._channel = None
        self._server_messages = {}
        self._servers = {}

        bot.add_cog(self)

    def exit(self):
        pass

    async def update_servers(self):
        while True:
            for name, server in self._servers.items():
                server.update()

                message = '{} [{}/{}] {}'.format(
                    server.name(),
                    server.players_online(),
                    server.slots(),
                    ', '.join(server.player_names()))

                pid = server.process().pid()
                new_message = await self._server_messages[pid].edit(content=message)
                self._server_messages[pid] = new_message
            time.sleep(15)

    @commands.Cog.listener()
    async def on_ready(self):
        for channel in self._bot.guilds[0].channels:
            if channel.name == 'status':
                self._channel = channel
                break
        self._ready = True

        if not self._is_init:
            pids = []
            pythoncom.CoInitialize()
            c = wmi.WMI()
            offsets = Offsets('offsets.json')
            for process in c.Win32_Process():
                if process.Name == 'Battlefront.exe':
                    pids.append(process.ProcessId)

            for pid in pids:
                process = Process(pid=pid)
                server = SWBFServer(process, offsets)
                self._servers[server.name()] = server

                message = '{} [{}/{}] {}'.format(
                    server.name(),
                    server.players_online(),
                    server.slots(),
                    ', '.join(server.player_names()))

                self._server_messages[pid] = await self._channel.send(message)

            self._is_init = True
            self._bot.loop.create_task(self.update_servers())