import psutil
from ctypes import *
import win32api
import win32process


class Process:
    def __init__(self, process_name):
        self._pid = 0
        self._handle = None

        for process in psutil.process_iter():
            if process.name() == process_name:
                self._pid = process.pid

        self._handle = windll.kernel32.OpenProcess(0x1F0FFF, False, self._pid)
        self._modules = win32process.EnumProcessModules(self._handle)
        self._base_address = self._modules[0]

    def __del__(self):
        win32api.CloseHandle(self._handle)

    def read(self, offset, size=64):
        data = create_string_buffer(size)
        read_bytes = c_ulonglong()
        result = windll.kernel32.ReadProcessMemory(self._handle, self._base_address + offset, byref(data), sizeof(data), byref(read_bytes))
        e = GetLastError()

        return data
