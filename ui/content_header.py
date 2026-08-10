from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QColor
from ui.animated_button import AnimatedIconButton

class ContentHeader(QWidget):
    close_requested = pyqtSignal()
    minimize_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("contentHeader")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(56)
        self._dragging = False
        self._drag_pos = QPoint()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 16, 0)
        layout.setSpacing(10)
        title = QLabel("Process Explorer")
        title.setObjectName("headerTitle")
        layout.addWidget(title)
        layout.addStretch()
        self.min_btn = AnimatedIconButton("─")
        self.min_btn.setFixedSize(32, 32)
        self.min_btn.setCursor(Qt.PointingHandCursor)
        self.min_btn.set_theme(
            base_bg=QColor(255, 255, 255, 0),
            hover_bg=QColor(241, 245, 249, 220),
            base_text=QColor(71, 85, 105, 255),
            hover_text=QColor(15, 23, 42, 255),
            radius=6
        )
        self.min_btn.clicked.connect(self.minimize_requested.emit)
        layout.addWidget(self.min_btn)
        self.close_btn = AnimatedIconButton("✕")
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.set_theme(
            base_bg=QColor(255, 255, 255, 0),
            hover_bg=QColor(239, 68, 68, 180),
            base_text=QColor(71, 85, 105, 255),
            hover_text=QColor(255, 255, 255, 255),
            radius=6
        )
        self.close_btn.clicked.connect(self.close_requested.emit)
        layout.addWidget(self.close_btn)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_pos = event.globalPos() - self.window().frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._dragging and event.buttons() & Qt.LeftButton:
            self.window().move(event.globalPos() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = False
