import threading
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QMessageBox, QApplication, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor

from core.scanner import ScannerThread
from core.injector import inject_shellcode
from utils.admin import is_admin
from ui.styles import MAIN_STYLESHEET
from ui.sidebar import Sidebar
from ui.content_header import ContentHeader
from ui.process_table import ProcessTable


class InjectorWindow(QMainWindow):
    injection_result = pyqtSignal(bool, str, int)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.selected_pid = None
        self.is_scanning = False
        self.is_injecting = False
        self.is_closing = False
        self.scanner_thread = None

        self._setup_ui()
        self.setStyleSheet(MAIN_STYLESHEET)

        self.sidebar.status_card.set_status('idle', 'Ready to scan')
        self.injection_result.connect(self._on_injection_result)

        self.setWindowOpacity(0)
        self.show()
        self._animate_open()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(0)

        self.root_frame = QFrame()
        self.root_frame.setObjectName("rootFrame")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 10)
        self.root_frame.setGraphicsEffect(shadow)

        root_layout = QHBoxLayout(self.root_frame)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.scan_requested.connect(self.scan_processes)
        self.sidebar.inject_requested.connect(self.inject)
        root_layout.addWidget(self.sidebar)

        # Content Area
        content_area = QWidget()
        content_area.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Header
        self.header = ContentHeader()
        self.header.close_requested.connect(self._start_exit_animation)
        self.header.minimize_requested.connect(self.showMinimized)
        content_layout.addWidget(self.header)

        # Table
        self.process_table = ProcessTable()
        self.process_table.process_selected.connect(self._on_process_selected)
        self.process_table.process_double_clicked.connect(self.inject)
        content_layout.addWidget(self.process_table, 1)

        root_layout.addWidget(content_area, 1)
        main_layout.addWidget(self.root_frame)

        self.setFixedSize(860, 560)
        self.process_table.clear()

    # --- Scanning ---
    def scan_processes(self):
        if self.is_scanning: return
        self.is_scanning = True
        self.sidebar.scan_btn.setEnabled(False)
        self.sidebar.inject_btn.setEnabled(False)
        self.selected_pid = None

        self.process_table.show_loading()
        self.sidebar.status_card.set_status("scanning", "Scanning...")

        self.scanner_thread = ScannerThread()
        self.scanner_thread.finished_scan.connect(self._on_scan_finished)
        self.scanner_thread.status_update.connect(self.sidebar.status_card.set_status)
        self.scanner_thread.start()

    def _on_scan_finished(self, processes: list):
        self.is_scanning = False
        self.sidebar.scan_btn.setEnabled(True)
        self.process_table.set_processes(processes)

        if processes:
            self.sidebar.status_card.set_status("success", f"Found {len(processes)} process(es)")
        else:
            self.sidebar.status_card.set_status("warning", "No processes found")

    # --- Injection ---
    def inject(self):
        if self.is_injecting or not self.selected_pid: return
        if not is_admin():
            QMessageBox.critical(self, "Admin Required", "Please restart as Administrator.")
            return

        pid = self.selected_pid
        self.is_injecting = True
        self.sidebar.inject_btn.setEnabled(False)
        self.sidebar.scan_btn.setEnabled(False)
        self.sidebar.status_card.set_status("scanning", f"Injecting PID {pid}...")

        threading.Thread(target=self._do_injection, args=(pid,), daemon=True).start()

    def _do_injection(self, pid: int):
        try:
            result = inject_shellcode(pid)
            self.injection_result.emit(result.success, result.message, result.error_code)
        except Exception as e:
            self.injection_result.emit(False, f"Exception: {str(e)}", -1)

    def _on_injection_result(self, success: bool, message: str, error_code: int):
        self.is_injecting = False
        self.sidebar.inject_btn.setEnabled(True)
        self.sidebar.scan_btn.setEnabled(True)
        if success:
            self.sidebar.status_card.set_status("success", "Injection successful")
        else:
            self.sidebar.status_card.set_status("error", f"Failed: {message}")

    def _on_process_selected(self, proc: dict):
        self.selected_pid = proc["pid"]
        self.sidebar.inject_btn.setEnabled(True)
        self.sidebar.status_card.set_status("idle", f"Selected: {proc['title']}")

    # --- Animations ---
    def _animate_open(self):
        self.animation_open = QPropertyAnimation(self, b"windowOpacity")
        self.animation_open.setDuration(300)
        self.animation_open.setStartValue(0.0)
        self.animation_open.setEndValue(1.0)
        self.animation_open.setEasingCurve(QEasingCurve.OutCubic)
        self.animation_open.start()

    def _start_exit_animation(self):
        if self.is_closing: return
        self.is_closing = True
        self.animation_close = QPropertyAnimation(self, b"windowOpacity")
        self.animation_close.setDuration(250)
        self.animation_close.setStartValue(1.0)
        self.animation_close.setEndValue(0.0)
        self.animation_close.setEasingCurve(QEasingCurve.InCubic)
        self.animation_close.finished.connect(QApplication.quit)
        self.animation_close.start()

    def closeEvent(self, event):
        if not self.is_closing:
            event.ignore()
            self._start_exit_animation()