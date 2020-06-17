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


def update_server(servers):
    while True:
        for name, server in servers.items():
            server.update()
            #print(server.player_names())
            sys.stdout.flush()
        time.sleep(10)


class ServerBot(commands.Cog):

    def __init__(self, bot):
        self._ready = False
        self._bot = bot
        self._channel = None
        self._server_messages = {}

        bot.add_cog(self)

    def exit(self):
        pass

    def join(self, server):
        pid = server.process().pid()
        message = server.name() + ' ' + ', '.join(server.player_names)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._server_messages[pid].edit(content=message))


    def leave(self, server):
        pid = server.process().pid()
        message = server.name() + ' ' + ', '.join(server.player_names)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._server_messages[pid].edit(content=message))

    @commands.Cog.listener()
    async def on_ready(self):
        for channel in self._bot.guilds[0].channels:
            if channel.name == 'status':
                self._channel = channel
                break
        self._ready = True

        pids = []
        servers = {}
        pythoncom.CoInitialize()
        c = wmi.WMI()
        offsets = Offsets('offsets.json')
        for process in c.Win32_Process():
            if process.Name == 'Battlefront.exe':
                pids.append(process.ProcessId)

        for pid in pids:
            process = Process(pid=pid)
            server = SWBFServer(process, offsets)
            server.on_join(self.join)
            server.on_leave(self.leave)
            servers[server.get_info()['name']] = server

            message = server.get_info()['name'] + ' is up!'
            self._server_messages[pid] = await self._channel.send(message)

        server_thread = threading.Thread(target=update_server, args=[servers], daemon=True)
        server_thread.start()