from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor
from ui.animated_button import AnimatedButton

class Sidebar(QWidget):
    scan_requested = pyqtSignal()
    inject_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(220)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(16)
        name_label = QLabel("Cheese Injector")
        name_label.setObjectName("appName")
        layout.addWidget(name_label)
        desc_label = QLabel("Minecraft Hack Client")
        desc_label.setObjectName("appDesc")
        layout.addWidget(desc_label)
        layout.addSpacing(24)
        self.scan_btn = AnimatedButton("Scan Processes")
        self.scan_btn.setObjectName("scanBtn")
        self.scan_btn.setCursor(Qt.PointingHandCursor)
        self.scan_btn.set_theme(
            base_bg=QColor(6, 182, 212, 255), hover_bg=QColor(8, 145, 178, 255),
            base_border=QColor(6, 182, 212, 255), hover_border=QColor(8, 145, 178, 255),
            base_text=QColor(255, 255, 255, 255), hover_text=QColor(255, 255, 255, 255)
        )
        self.scan_btn.clicked.connect(self.scan_requested.emit)
        layout.addWidget(self.scan_btn)
        self.inject_btn = AnimatedButton("Inject")
        self.inject_btn.setObjectName("injectBtn")
        self.inject_btn.setCursor(Qt.PointingHandCursor)
        self.inject_btn.setEnabled(False)
        self.inject_btn.set_theme(
            base_bg=QColor(255, 255, 255, 200), hover_bg=QColor(248, 250, 252, 220),
            base_border=QColor(226, 232, 240, 200), hover_border=QColor(6, 182, 212, 255),
            base_text=QColor(15, 23, 42, 255), hover_text=QColor(8, 145, 178, 255)
        )
        self.inject_btn.clicked.connect(self.inject_requested.emit)
        layout.addWidget(self.inject_btn)
        layout.addStretch()
