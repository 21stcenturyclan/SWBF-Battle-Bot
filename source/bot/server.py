import asyncio
import sys
import time

import pythoncom
import wmi
import threading

from discord.ext import commands

from source.memory.offsets import Offsets
from source.memory.process import Process
from source.memory.swbf_server import SWBFServer


class ServerBot(commands.Cog):

    def __init__(self, bot):
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

                if server.has_changed():
                    message = server.name() + ': ' + ', '.join(server.player_names())
                    pid = server.process().pid()
                    await self._server_messages[pid].edit(content=message)
            time.sleep(10)

    @commands.Cog.listener()
    async def on_ready(self):
        for channel in self._bot.guilds[0].channels:
            if channel.name == 'status':
                self._channel = channel
                break
        self._ready = True

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

            message = server.name() + ' is up: ' + ', '.join(server.player_names())
            self._server_messages[pid] = await self._channel.send(message)


        self._bot.loop.create_task(self.update_servers())