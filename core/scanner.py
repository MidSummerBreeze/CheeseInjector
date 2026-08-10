import psutil
from PyQt5.QtCore import QThread, pyqtSignal
from utils.window_utils import get_window_title_for_pid

JAVA_PROCESS_NAMES = {"java.exe", "javaw.exe"}

class ScannerThread(QThread):
    finished_scan = pyqtSignal(list)
    status_update = pyqtSignal(str, str)

    def run(self):
        self.status_update.emit("scanning", "Scanning for Java processes...")
        processes = []
        try:
            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    name = proc.info["name"]
                    if name and name.lower() in JAVA_PROCESS_NAMES:
                        pid = proc.info["pid"]
                        title = get_window_title_for_pid(pid)
                        processes.append({
                            "pid": pid,
                            "name": name,
                            "title": title if title else "No Window",
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            processes.sort(key=lambda x: x["pid"])
            self.status_update.emit("success", f"Scan complete — {len(processes)} process(es) found")
            self.finished_scan.emit(processes)
        except Exception as e:
            self.status_update.emit("error", f"Scan error: {str(e)}")
            self.finished_scan.emit([])
