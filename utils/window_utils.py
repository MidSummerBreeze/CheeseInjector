import ctypes
from ctypes import wintypes, WINFUNCTYPE, byref


def get_window_title_for_pid(pid: int) -> str:
    # Enumerate all top-level windows and return the first visible
    # window title that belongs to the given process ID
    HWND = wintypes.HWND
    LPARAM = wintypes.LPARAM
    BOOL = wintypes.BOOL
    WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, LPARAM)

    titles = []

    def enum_callback(hwnd, lparam):
        process_id = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, byref(process_id))

        if process_id.value == pid:
            if ctypes.windll.user32.IsWindowVisible(hwnd):
                buf = ctypes.create_unicode_buffer(256)
                ctypes.windll.user32.GetWindowTextW(hwnd, buf, 256)
                title = buf.value.strip()
                if title:
                    titles.append(title)
        return True

    enum_proc = WNDENUMPROC(enum_callback)
    ctypes.windll.user32.EnumWindows(enum_proc, 0)

    return titles[0] if titles else ""