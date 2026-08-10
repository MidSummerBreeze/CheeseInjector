import ctypes

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def show_admin_required_dialog():
    from utils.dialogs import show_taskdialog_error
    show_taskdialog_error(
        None,
        "Administrator Required",
        "Cheese Injector",
        "This application requires administrator privileges to run.\n\nPlease restart the program as Administrator."
    )
