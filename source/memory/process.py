from ctypes import *
import win32api
import win32process
import wmi


class Process:
    def __init__(self, process_name='', pid=None):
        self._handle = None
        self._modules = []
        self._base_address = 0
        self._pid = pid

        if not self._pid:
            c = wmi.WMI()

            for process in c.Win32_Process():
                if process.Name == process_name:
                    self._pid = process.ProcessId
                    break

        if self._pid:
            self._handle = windll.kernel32.OpenProcess(0x1F0FFF, False, self._pid)
            self._modules = win32process.EnumProcessModules(self._handle)
            self._base_address = self._modules[0]

    def __del__(self):
        win32api.CloseHandle(self._handle)

    def pid(self):
        return self._pid

    def read(self, offset, size=64):
        data = create_string_buffer(size)
        read_bytes = c_ulonglong()

        if not windll.kernel32.ReadProcessMemory(self._handle,
                                                 self._base_address + offset,
                                                 byref(data), sizeof(data),
                                                 byref(read_bytes)):
            pass # print(GetLastError())

        return data
