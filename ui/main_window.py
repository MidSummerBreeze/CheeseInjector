import threading
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QPoint, QEvent
from core.scanner import ScannerThread
from core.injector import inject_shellcode
from utils.admin import is_admin
from utils.acrylic import enable_acrylic
from ui.styles import MAIN_STYLESHEET
from ui.sidebar import Sidebar
from ui.content_header import ContentHeader
from ui.process_table import ProcessTable
from ui.toast import ToastManager

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
        self.animation_open = None
        self.animation_close = None
        self.anim_minimize = None
        self.anim_restore = None
        self.pos_anim = None
        self._setup_ui()
        is_win11 = sys.getwindowsversion().build >= 22000
        current_style = MAIN_STYLESHEET
        if not is_win11:
            current_style = current_style.replace("border-radius: 12px;", "border-radius: 0px;")
            current_style = current_style.replace("border-top-left-radius: 12px;", "border-top-left-radius: 0px;")
            current_style = current_style.replace("border-bottom-left-radius: 12px;", "border-bottom-left-radius: 0px;")
            current_style = current_style.replace("border-top-right-radius: 12px;", "border-top-right-radius: 0px;")
            current_style = current_style.replace("border-bottom-right-radius: 12px;", "border-bottom-right-radius: 0px;")
        self.setStyleSheet(current_style)
        self.toast_manager = ToastManager(self)
        self.injection_result.connect(self._on_injection_result)
        self.setWindowOpacity(0)
        self.show()
        hwnd = int(self.winId())
        enable_acrylic(hwnd)
        self._animate_open()

    def _setup_ui(self):
        central = QWidget()
        central.setObjectName("rootFrame")
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.sidebar = Sidebar()
        self.sidebar.scan_requested.connect(self.scan_processes)
        self.sidebar.inject_requested.connect(self.inject)
        main_layout.addWidget(self.sidebar)
        content_area = QWidget()
        content_area.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        self.header = ContentHeader()
        self.header.close_requested.connect(self._start_exit_animation)
        self.header.minimize_requested.connect(self.showMinimized)
        content_layout.addWidget(self.header)
        self.process_table = ProcessTable()
        self.process_table.process_selected.connect(self._on_process_selected)
        self.process_table.process_double_clicked.connect(self.inject)
        content_layout.addWidget(self.process_table, 1)
        main_layout.addWidget(content_area, 1)
        self.setFixedSize(860, 560)
        self.process_table.clear()

    def scan_processes(self):
        if self.is_scanning: return
        self.is_scanning = True
        self.sidebar.scan_btn.setEnabled(False)
        self.sidebar.inject_btn.setEnabled(False)
        self.selected_pid = None
        self.process_table.show_loading()
        self.toast_manager.show_toast("Scanning", "Looking for Minecraft processes...", "info")
        self.scanner_thread = ScannerThread()
        self.scanner_thread.finished_scan.connect(self._on_scan_finished)
        self.scanner_thread.status_update.connect(self._on_scan_status)
        self.scanner_thread.start()

    def _on_scan_status(self, status_type, message):
        pass

    def _on_scan_finished(self, processes: list):
        self.is_scanning = False
        self.sidebar.scan_btn.setEnabled(True)
        self.process_table.set_processes(processes)
        if processes:
            self.toast_manager.show_toast("Success", f"Found {len(processes)} process(es)", "success")
        else:
            self.toast_manager.show_toast("Warning", "No Java processes found", "warning")

    def inject(self):
        if self.is_injecting or not self.selected_pid: return
        if not is_admin():
            self.toast_manager.show_toast("Error", "Administrator privileges required", "error")
            return
        pid = self.selected_pid
        self.is_injecting = True
        self.sidebar.inject_btn.setEnabled(False)
        self.sidebar.scan_btn.setEnabled(False)
        self.toast_manager.show_toast("Injecting", f"Targeting PID {pid}...", "info")
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
            self.toast_manager.show_toast("Success", "Injection successful", "success")
        else:
            self.toast_manager.show_toast("Error", f"Injection failed: {message}", "error")

    def _on_process_selected(self, proc: dict):
        self.selected_pid = proc["pid"]
        self.sidebar.inject_btn.setEnabled(True)
        self.toast_manager.show_toast("Selected", f"PID {proc['pid']} - {proc['title']}", "info", 2000)

    def _animate_open(self):
        current_pos = self.pos()
        start_pos = QPoint(current_pos.x(), current_pos.y() + 20)
        self.move(start_pos)
        self.animation_open = QPropertyAnimation(self, b"windowOpacity")
        self.animation_open.setDuration(350)
        self.animation_open.setStartValue(0.0)
        self.animation_open.setEndValue(1.0)
        self.animation_open.setEasingCurve(QEasingCurve.OutCubic)
        self.animation_open.start()
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(350)
        self.pos_anim.setStartValue(start_pos)
        self.pos_anim.setEndValue(current_pos)
        self.pos_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.pos_anim.start()

    def showMinimized(self):
        self.anim_minimize = QPropertyAnimation(self, b"windowOpacity")
        self.anim_minimize.setDuration(150)
        self.anim_minimize.setStartValue(1.0)
        self.anim_minimize.setEndValue(0.0)
        self.anim_minimize.setEasingCurve(QEasingCurve.InCubic)
        self.anim_minimize.finished.connect(lambda: super(InjectorWindow, self).showMinimized())
        self.anim_minimize.start()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() == Qt.WindowNoState and event.oldState() & Qt.WindowMinimized:
                self.setWindowOpacity(0.0)
                self.anim_restore = QPropertyAnimation(self, b"windowOpacity")
                self.anim_restore.setDuration(250)
                self.anim_restore.setStartValue(0.0)
                self.anim_restore.setEndValue(1.0)
                self.anim_restore.setEasingCurve(QEasingCurve.OutCubic)
                self.anim_restore.start()
        super().changeEvent(event)

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
