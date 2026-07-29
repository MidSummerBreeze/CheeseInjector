import sys
import os
import ctypes
import psutil
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QLabel, QFrame, QMessageBox, QGraphicsOpacityEffect)
from PyQt5.QtCore import Qt, QTimer, QPoint, pyqtSignal, QThread, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    sys.exit()

PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT_RESERVE = 0x3000
PAGE_EXECUTE_READWRITE = 0x40
SHELLCODE = bytearray([0x0F, 0x0B])

class WinAPI:
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    @staticmethod
    def OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId):
        return WinAPI.kernel32.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId)

    @staticmethod
    def VirtualAllocEx(hProcess, lpAddress, dwSize, flAllocationType, flProtect):
        return WinAPI.kernel32.VirtualAllocEx(hProcess, lpAddress, dwSize, flAllocationType, flProtect)

    @staticmethod
    def WriteProcessMemory(hProcess, lpBaseAddress, lpBuffer, nSize):
        lpNumberOfBytesWritten = ctypes.c_size_t(0)
        result = WinAPI.kernel32.WriteProcessMemory(hProcess, lpBaseAddress, lpBuffer, nSize, ctypes.byref(lpNumberOfBytesWritten))
        return result != 0, lpNumberOfBytesWritten.value

    @staticmethod
    def CreateRemoteThread(hProcess, lpStartAddress, lpParameter=0):
        lpThreadId = ctypes.c_ulong(0)
        hThread = WinAPI.kernel32.CreateRemoteThread(hProcess, None, 0, lpStartAddress, lpParameter, 0, ctypes.byref(lpThreadId))
        return hThread, lpThreadId.value

    @staticmethod
    def CloseHandle(hObject):
        return WinAPI.kernel32.CloseHandle(hObject) != 0

    @staticmethod
    def GetLastError():
        return ctypes.get_last_error()

def get_window_title_for_pid(pid: int) -> str:
    from ctypes import wintypes, WINFUNCTYPE, byref, c_ulong
    HWND = wintypes.HWND
    LPARAM = wintypes.LPARAM
    BOOL = wintypes.BOOL
    WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, LPARAM)
    titles = []
    def enum_callback(hwnd, lParam):
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

def inject_into_process(pid: int) -> tuple:
    if not psutil.pid_exists(pid):
        return False, "Process does not exist", -1

    hProcess = WinAPI.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if hProcess == 0:
        error = WinAPI.GetLastError()
        return False, f"OpenProcess failed (error: {error})", error

    try:
        addr = WinAPI.VirtualAllocEx(hProcess, 0, len(SHELLCODE), MEM_COMMIT_RESERVE, PAGE_EXECUTE_READWRITE)
        if addr == 0:
            error = WinAPI.GetLastError()
            return False, f"VirtualAllocEx failed (error: {error})", error

        success, bytes_written = WinAPI.WriteProcessMemory(hProcess, addr, bytes(SHELLCODE), len(SHELLCODE))
        if not success or bytes_written != len(SHELLCODE):
            error = WinAPI.GetLastError()
            return False, f"WriteProcessMemory failed (error: {error})", error

        hThread, thread_id = WinAPI.CreateRemoteThread(hProcess, addr)
        if hThread == 0:
            error = WinAPI.GetLastError()
            return False, f"CreateRemoteThread failed (error: {error})", error

        WinAPI.CloseHandle(hThread)
        return True, f"Remote thread created (ID: {thread_id})", 0

    finally:
        WinAPI.CloseHandle(hProcess)

class ScannerThread(QThread):
    finished = pyqtSignal(list)
    status_update = pyqtSignal(str, str)
    def run(self):
        self.status_update.emit('scanning', 'Scanning for Java processes...')
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    name = proc.info['name'].lower()
                    if name in ('java.exe', 'javaw.exe'):
                        pid = proc.info['pid']
                        title = get_window_title_for_pid(pid)
                        processes.append({
                            'pid': pid,
                            'name': proc.info['name'],
                            'title': title if title else 'No Window'
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            processes.sort(key=lambda x: x['pid'])
            self.status_update.emit('success', f'Scan complete — {len(processes)} process(es) found')
            self.finished.emit(processes)
        except Exception as e:
            self.status_update.emit('error', f'Scan error: {str(e)}')
            self.finished.emit([])

class InjectorWindow(QMainWindow):
    injection_result = pyqtSignal(bool, str, int)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.dragging = False
        self.drag_pos = QPoint()
        self.processes = []
        self.selected_pid = None
        self.is_scanning = False
        self.is_injecting = False
        self.animation_open = None
        self.animation_close = None
        self.is_closing = False

        font = QFont("Segoe UI", 9)
        QApplication.setFont(font)

        self.setup_ui()
        self.apply_styles()
        self.update_status('idle', 'Ready — Click "Scan Processes" to target Minecraft for cheat injection')

        self.injection_result.connect(self.on_injection_result)

        self.setWindowOpacity(0)
        self.show()
        self.animate_window_open()

    def setup_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.window_frame = QFrame()
        self.window_frame.setObjectName("windowFrame")
        frame_layout = QVBoxLayout(self.window_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)
        main_layout.addWidget(self.window_frame)

        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(44)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(16, 0, 12, 0)
        title_bar_layout.setSpacing(8)

        title_label = QLabel("Cheese Injector")
        title_label.setObjectName("titleLabel")
        title_bar_layout.addWidget(title_label)

        subtitle_label = QLabel("— Cheat Client")
        subtitle_label.setObjectName("subtitleLabel")
        title_bar_layout.addWidget(subtitle_label)
        title_bar_layout.addStretch()

        self.min_btn = QPushButton("—")
        self.min_btn.setObjectName("minBtn")
        self.min_btn.setFixedSize(28, 28)
        self.min_btn.setCursor(Qt.PointingHandCursor)
        self.min_btn.clicked.connect(self.minimize_with_animation)
        title_bar_layout.addWidget(self.min_btn)

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setFixedSize(28, 28)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.clicked.connect(self.start_exit_animation)
        title_bar_layout.addWidget(self.close_btn)

        frame_layout.addWidget(title_bar)

        content = QWidget()
        content.setObjectName("contentArea")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 16, 20, 20)
        content_layout.setSpacing(14)

        action_row = QHBoxLayout()
        action_row.setSpacing(8)

        self.scan_btn = QPushButton("Scan Processes")
        self.scan_btn.setObjectName("scanBtn")
        self.scan_btn.setCursor(Qt.PointingHandCursor)
        self.scan_btn.clicked.connect(self.scan_processes)
        self.setup_button_animation(self.scan_btn)
        action_row.addWidget(self.scan_btn)

        self.inject_btn = QPushButton("Inject")
        self.inject_btn.setObjectName("injectBtn")
        self.inject_btn.setCursor(Qt.PointingHandCursor)
        self.inject_btn.setEnabled(False)
        self.inject_btn.clicked.connect(self.inject)
        self.setup_button_animation(self.inject_btn)
        action_row.addWidget(self.inject_btn)

        action_row.addStretch()
        content_layout.addLayout(action_row)

        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)

        self.table = QTableWidget()
        self.table.setObjectName("processTable")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Process", "Window Title"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.setSortingEnabled(False)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.itemClicked.connect(self.on_table_item_clicked)

        table_font = QFont("JetBrains Mono", 10)
        table_font.setStyleHint(QFont.Monospace)
        self.table.setFont(table_font)

        table_layout.addWidget(self.table)
        content_layout.addWidget(table_frame)

        hint_label = QLabel("Click a process row to select target, then inject cheat code.")
        hint_label.setObjectName("hintLabel")
        content_layout.addWidget(hint_label)

        status_bar = QWidget()
        status_bar.setObjectName("statusBar")
        status_bar.setFixedHeight(34)
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(12, 0, 12, 0)
        status_layout.setSpacing(10)

        self.status_dot = QLabel()
        self.status_dot.setObjectName("statusDot")
        self.status_dot.setFixedSize(8, 8)
        status_layout.addWidget(self.status_dot)

        self.status_text = QLabel("Ready — Click \"Scan Processes\" to target Minecraft for cheat injection")
        self.status_text.setObjectName("statusText")
        status_layout.addWidget(self.status_text)
        status_layout.addStretch()
        content_layout.addWidget(status_bar)

        frame_layout.addWidget(content)

        self.setFixedSize(620, 520)
        self.clear_table()

        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.pulse_status_dot)
        self.pulse_state = False

    def setup_button_animation(self, button):
        effect = QGraphicsOpacityEffect()
        button.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(150)
        anim.setEasingCurve(QEasingCurve.OutQuad)

        def on_pressed():
            anim.stop()
            anim.setStartValue(1.0)
            anim.setEndValue(0.6)
            anim.start()

        def on_released():
            anim.stop()
            anim.setStartValue(0.6)
            anim.setEndValue(1.0)
            anim.start()

        button.pressed.connect(on_pressed)
        button.released.connect(on_released)

    def minimize_with_animation(self):
        self.min_anim = QPropertyAnimation(self, b"windowOpacity")
        self.min_anim.setDuration(300)
        self.min_anim.setStartValue(1.0)
        self.min_anim.setEndValue(0.0)
        self.min_anim.setEasingCurve(QEasingCurve.InCubic)
        self.min_anim.finished.connect(self._finish_minimize)
        self.min_anim.start()

    def _finish_minimize(self):
        self.showMinimized()
        self.setWindowOpacity(1.0)

    def clear_table(self):
        self.table.clearContents()
        self.table.setRowCount(0)

    def apply_styles(self):
        style = """
        #windowFrame {
            background-color: #ffffff;
            border-radius: 14px;
            border: 1px solid #e8eaef;
        }
        #centralWidget {
            background-color: transparent;
        }
        #titleBar {
            background-color: #fafbfc;
            border-top-left-radius: 14px;
            border-top-right-radius: 14px;
            border-bottom: 1px solid #e8eaef;
        }
        #titleLabel {
            color: #1a1d23;
            font-size: 13px;
            font-weight: 600;
        }
        #subtitleLabel {
            color: #9aa0b0;
            font-size: 11px;
            font-weight: 400;
        }
        #minBtn, #closeBtn {
            background: transparent;
            border: none;
            border-radius: 4px;
            font-size: 18px;
            font-weight: 300;
            color: #9aa0b0;
            padding: 0;
            margin: 0;
        }
        #minBtn:hover, #closeBtn:hover {
            background: #f0f0f0;
            color: #1a1d23;
        }
        #minBtn:pressed, #closeBtn:pressed {
            background: #e0e0e0;
        }
        #contentArea {
            background-color: #ffffff;
            border-bottom-left-radius: 14px;
            border-bottom-right-radius: 14px;
        }
        #scanBtn, #injectBtn {
            border-radius: 6px;
            padding: 7px 18px;
            font-size: 12.5px;
            font-weight: 500;
            border: 1px solid transparent;
        }
        #scanBtn {
            background-color: #ffffff;
            color: #1a1d23;
            border-color: #e8eaef;
        }
        #scanBtn:hover {
            background-color: #fafbfc;
            border-color: #d5d8de;
        }
        #scanBtn:pressed {
            background-color: #f3f4f6;
            padding: 5px 16px;
        }
        #scanBtn:disabled {
            opacity: 0.45;
        }

        #injectBtn {
            background-color: #4f6ef6;
            color: #ffffff;
            border-color: #4f6ef6;
        }
        #injectBtn:hover {
            background-color: #3d5de0;
            border-color: #3d5de0;
        }
        #injectBtn:pressed {
            background-color: #3451cc;
            border-color: #3451cc;
            padding: 5px 16px;
        }
        #injectBtn:disabled {
            background-color: #4f6ef6;
            opacity: 0.45;
        }

        #tableFrame {
            border: 1px solid #e8eaef;
            border-radius: 10px;
            background-color: #ffffff;
        }
        #processTable {
            border: none;
            background-color: #ffffff;
            gridline-color: transparent;
            font-family: 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace;
            font-size: 12px;
        }
        QTableWidget::item {
            border: none;
            padding: 8px 12px;
        }
        QTableWidget::item:selected {
            background-color: #eef2fb;
        }
        QTableWidget::item:selected:first {
            border-left: 3px solid #4f6ef6;
        }
        QTableWidget::item:hover {
            background-color: #f5f7fa;
        }
        QTableWidget QHeaderView::section {
            background-color: #f9fafb;
            color: #4a5060;
            font-size: 11px;
            font-weight: 600;
            font-family: 'Segoe UI', 'Inter', sans-serif;
            padding: 8px 12px;
            border: none;
            border-bottom: 1px solid #e8eaef;
            letter-spacing: 0.02em;
        }
        QTableWidget QTableCornerButton::section {
            background-color: #f9fafb;
            border: none;
        }
        #statusBar {
            background-color: #fafbfc;
            border: 1px solid #f0f2f5;
            border-radius: 6px;
        }
        #statusDot {
            border-radius: 4px;
        }
        #statusDot.idle {
            background-color: #c8cdd6;
        }
        #statusDot.scanning {
            background-color: #4f6ef6;
        }
        #statusDot.success {
            background-color: #30a46c;
        }
        #statusDot.error {
            background-color: #e5484d;
        }
        #statusDot.warning {
            background-color: #e9a23b;
        }
        #statusText {
            font-size: 12px;
            color: #5b616e;
            font-family: 'Segoe UI', sans-serif;
        }
        #hintLabel {
            font-size: 11px;
            color: #9aa0b0;
            margin-top: -6px;
            font-family: 'Segoe UI', sans-serif;
        }
        """
        self.setStyleSheet(style)

    def update_status(self, status_type: str, message: str):
        self.status_dot.setProperty("class", status_type)
        self.status_dot.style().polish(self.status_dot)
        self.status_text.setText(message)

        if status_type == 'scanning':
            self.pulse_state = False
            self.pulse_timer.start(500)
            self.status_dot.setStyleSheet("background-color: #4f6ef6; border-radius: 4px;")
        else:
            self.pulse_timer.stop()
            color_map = {
                'idle': '#c8cdd6',
                'success': '#30a46c',
                'error': '#e5484d',
                'warning': '#e9a23b'
            }
            self.status_dot.setStyleSheet(f"background-color: {color_map.get(status_type, '#c8cdd6')}; border-radius: 4px;")

    def pulse_status_dot(self):
        self.pulse_state = not self.pulse_state
        if self.pulse_state:
            self.status_dot.setStyleSheet("background-color: #7a8ef6; border-radius: 4px;")
        else:
            self.status_dot.setStyleSheet("background-color: #4f6ef6; border-radius: 4px;")

    def animate_window_open(self):
        if self.animation_open and self.animation_open.state() == QPropertyAnimation.Running:
            return
        self.animation_open = QPropertyAnimation(self, b"windowOpacity")
        self.animation_open.setDuration(300)
        self.animation_open.setStartValue(0.0)
        self.animation_open.setEndValue(1.0)
        self.animation_open.setEasingCurve(QEasingCurve.OutCubic)
        self.animation_open.start()

    def start_exit_animation(self):
        if self.is_closing:
            return
        self.is_closing = True
        self.animation_close = QPropertyAnimation(self, b"windowOpacity")
        self.animation_close.setDuration(250)
        self.animation_close.setStartValue(1.0)
        self.animation_close.setEndValue(0.0)
        self.animation_close.setEasingCurve(QEasingCurve.InCubic)
        self.animation_close.finished.connect(self.quit_application)
        self.animation_close.start()

    def update_table(self, processes: list):
        self.processes = processes
        self.table.clearContents()
        if not processes:
            self.clear_table()
            return
        self.table.setRowCount(len(processes))
        for i, proc in enumerate(processes):
            name_item = QTableWidgetItem(proc['name'])
            name_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, name_item)

            title_item = QTableWidgetItem(proc['title'])
            title_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, title_item)
        self.table.resizeColumnToContents(0)

    def on_table_item_clicked(self, item):
        row = item.row()
        if row < 0 or row >= len(self.processes):
            return
        proc = self.processes[row]
        self.selected_pid = proc['pid']
        self.inject_btn.setEnabled(True)
        self.update_status('idle', f"PID {proc['pid']} selected — {proc['title']}")

    def scan_processes(self):
        if self.is_scanning:
            return
        self.is_scanning = True
        self.scan_btn.setEnabled(False)
        self.inject_btn.setEnabled(False)
        self.table.clearSelection()
        self.selected_pid = None

        self.table.clearContents()
        self.table.setRowCount(1)
        item = QTableWidgetItem("Scanning for Java processes...")
        item.setTextAlignment(Qt.AlignCenter)
        item.setForeground(QColor(154, 160, 176))
        self.table.setItem(0, 1, item)
        for col in range(2):
            if col != 1:
                self.table.setItem(0, col, QTableWidgetItem(""))

        self.update_status('scanning', 'Scanning for Minecraft processes...')
        self.scanner_thread = ScannerThread()
        self.scanner_thread.finished.connect(self.on_scan_finished)
        self.scanner_thread.status_update.connect(self.update_status)
        self.scanner_thread.start()

    def on_scan_finished(self, processes: list):
        self.is_scanning = False
        self.scan_btn.setEnabled(True)
        self.update_table(processes)
        if processes:
            self.update_status('success', f'Scan complete — {len(processes)} process(es) found')
        else:
            self.update_status('warning', 'No Java processes found — launch Minecraft and try again')

    def inject(self):
        if self.is_injecting or not self.selected_pid:
            return
        if not is_admin():
            QMessageBox.warning(self, "Administrator Required",
                                "Injection requires administrator privileges.\n\nPlease restart the application as Administrator.")
            return

        pid = self.selected_pid
        self.is_injecting = True
        self.inject_btn.setEnabled(False)
        self.scan_btn.setEnabled(False)
        self.update_status('scanning', f'Injecting into PID {pid}...')

        threading.Thread(target=self._do_injection, args=(pid,), daemon=True).start()

    def _do_injection(self, pid):
        try:
            success, message, error_code = inject_into_process(pid)
            self.injection_result.emit(success, message, error_code)
        except Exception as e:
            self.injection_result.emit(False, f"Exception: {str(e)}", -1)

    def on_injection_result(self, success: bool, message: str, error_code: int):
        self.is_injecting = False
        self.inject_btn.setEnabled(True)
        self.scan_btn.setEnabled(True)
        if success:
            self.update_status('success', 'Injection successful')
        else:
            self.update_status('error', f'Injection failed — {message}')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def closeEvent(self, event):
        self.quit_application()

    def quit_application(self):
        QApplication.quit()

def main():
    if not is_admin():
        run_as_admin()
        return
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Cheese Injector")
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    window = InjectorWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()