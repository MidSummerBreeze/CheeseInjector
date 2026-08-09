from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import QTimer


STATUS_COLORS = {
    "idle": "#94A3B8",
    "scanning": "#06B6D4",
    "success": "#10B981",
    "error": "#EF4444",
    "warning": "#F59E0B",
}


class StatusBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statusCard")
        self.setFixedHeight(60)

        self._pulse_state = False
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._pulse_dot)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        self.status_dot = QLabel()
        self.status_dot.setFixedSize(10, 10)
        self.status_dot.setStyleSheet("background-color: #94A3B8; border-radius: 5px;")
        layout.addWidget(self.status_dot)

        self.status_text = QLabel("Idle — waiting for action")
        self.status_text.setObjectName("statusText")
        layout.addWidget(self.status_text)

        layout.addStretch()

    def set_status(self, status_type: str, message: str):
        self.status_text.setText(message)

        if status_type == "scanning":
            self._pulse_state = False
            self._pulse_timer.start(500)
            self.status_dot.setStyleSheet("background-color: #06B6D4; border-radius: 5px;")
        else:
            self._pulse_timer.stop()
            color = STATUS_COLORS.get(status_type, STATUS_COLORS["idle"])
            self.status_dot.setStyleSheet(f"background-color: {color}; border-radius: 5px;")

    def _pulse_dot(self):
        self._pulse_state = not self._pulse_state
        color = "#67E8F9" if self._pulse_state else "#06B6D4"
        self.status_dot.setStyleSheet(f"background-color: {color}; border-radius: 5px;")