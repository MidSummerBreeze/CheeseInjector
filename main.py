import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.admin import is_admin, show_admin_required_dialog
from ui.main_window import InjectorWindow


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Cheese Injector")
    app.setFont(QFont("Segoe UI", 9))
    if not is_admin():
        show_admin_required_dialog()
        sys.exit(1)
    window = InjectorWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
