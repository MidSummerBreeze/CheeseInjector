import ctypes


def is_admin() -> bool:
    # Check if the current process is running with elevated privileges
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def show_admin_required_dialog():
    # Show a native Windows error dialog when not running as admin
    from utils.dialogs import show_taskdialog_error
    show_taskdialog_error(
        None,
        "Administrator Required",
        "Cheese Injector",
        "This application requires administrator privileges to run.\n\n"
        "Please restart the program as Administrator."
    )