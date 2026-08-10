import ctypes
from ctypes import wintypes

def show_taskdialog_error(parent_hwnd, title, main_instruction, content):
    comctl32 = ctypes.windll.comctl32
    comctl32.InitCommonControls()
    TDCBF_OK_BUTTON = 0x0001
    TD_ERROR_ICON = 0xFFFE
    comctl32.TaskDialog.argtypes = [
        wintypes.HWND, wintypes.HINSTANCE, ctypes.c_wchar_p,
        ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint,
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)
    ]
    comctl32.TaskDialog.restype = ctypes.c_long
    response = ctypes.c_int()
    result = comctl32.TaskDialog(
        parent_hwnd, None, title, main_instruction, content,
        TDCBF_OK_BUTTON, ctypes.c_void_p(TD_ERROR_ICON), ctypes.byref(response)
    )
    return result == 0
