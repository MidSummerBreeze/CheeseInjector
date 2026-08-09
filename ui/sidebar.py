from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor
from ui.status_bar import StatusBar
from ui.animated_button import AnimatedButton


class Sidebar(QWidget):
    scan_requested = pyqtSignal()
    inject_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        # Required for QSS background-color to work on a QWidget
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.setFixedWidth(220)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(16)

        # App Branding
        name_label = QLabel("Cheese Injector")
        name_label.setObjectName("appName")
        layout.addWidget(name_label)

        desc_label = QLabel("Minecraft Hack Client")
        desc_label.setObjectName("appDesc")
        layout.addWidget(desc_label)

        layout.addSpacing(24)

        # Action Buttons
        self.scan_btn = AnimatedButton("Scan Processes")
        self.scan_btn.setObjectName("scanBtn")
        self.scan_btn.setCursor(Qt.PointingHandCursor)
        self.scan_btn.set_theme(
            base_bg=QColor("#06B6D4"), hover_bg=QColor("#0891B2"),
            base_border=QColor("#06B6D4"), hover_border=QColor("#0891B2"),
            base_text=QColor("#FFFFFF"), hover_text=QColor("#FFFFFF")
        )
        self.scan_btn.clicked.connect(self.scan_requested.emit)
        layout.addWidget(self.scan_btn)

        self.inject_btn = AnimatedButton("Inject")
        self.inject_btn.setObjectName("injectBtn")
        self.inject_btn.setCursor(Qt.PointingHandCursor)
        self.inject_btn.setEnabled(False)
        self.inject_btn.set_theme(
            base_bg=QColor("#FFFFFF"), hover_bg=QColor("#F8FAFC"),
            base_border=QColor("#E2E8F0"), hover_border=QColor("#06B6D4"),
            base_text=QColor("#0F172A"), hover_text=QColor("#0891B2")
        )
        self.inject_btn.clicked.connect(self.inject_requested.emit)
        layout.addWidget(self.inject_btn)

        layout.addStretch()

        # Status Card
        self.status_card = StatusBar()
        layout.addWidget(self.status_card)