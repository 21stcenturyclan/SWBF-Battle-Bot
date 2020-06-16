import time
import wmi
import sys

from source.memory.offsets import Offsets
from source.memory.process import Process
from source.memory.swbf_server import SWBFServer


pids = []
servers = {}
id = 0
offsets = Offsets('offsets.json')
c = wmi.WMI()

for process in c.Win32_Process():
    if process.Name == 'Battlefront.exe':
        pids.append(process.ProcessId)

for pid in pids:
    process = Process(pid=pid)
    server = SWBFServer(process, offsets)
    servers[server.get_info()['name']] = server

while True:
    for name, server in servers.items():
        server.update()
        print(name, server.slots(), server.players_online())
        sys.stdout.flush()
    time.sleep(5)
