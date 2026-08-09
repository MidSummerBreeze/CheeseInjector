from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QVariantAnimation, QEasingCurve
from PyQt5.QtGui import QColor


class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._anim = QVariantAnimation(self)
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.InOutQuad)
        self._anim.valueChanged.connect(self._update_style)
        
        self._progress = 0.0
        
        # Default theme (will be overwritten)
        self._base_bg = QColor("#FFFFFF")
        self._hover_bg = QColor("#F8FAFC")
        self._base_border = QColor("#E2E8F0")
        self._hover_border = QColor("#06B6D4")
        self._base_text = QColor("#0F172A")
        self._hover_text = QColor("#0891B2")

        self._update_style(0.0)

    def set_theme(self, base_bg, hover_bg, base_border, hover_border, base_text, hover_text):
        self._base_bg = base_bg
        self._hover_bg = hover_bg
        self._base_border = base_border
        self._hover_border = hover_border
        self._base_text = base_text
        self._hover_text = hover_text
        self._update_style(self._progress)

    def _interpolate_color(self, c1: QColor, c2: QColor, p: float) -> QColor:
        r = int(c1.red() + (c2.red() - c1.red()) * p)
        g = int(c1.green() + (c2.green() - c1.green()) * p)
        b = int(c1.blue() + (c2.blue() - c1.blue()) * p)
        return QColor(r, g, b)

    def enterEvent(self, event):
        self._anim.stop()
        self._anim.setStartValue(self._progress)
        self._anim.setEndValue(1.0)
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._anim.stop()
        self._anim.setStartValue(self._progress)
        self._anim.setEndValue(0.0)
        self._anim.start()
        super().leaveEvent(event)

    def _update_style(self, p: float):
        self._progress = p
        bg = self._interpolate_color(self._base_bg, self._hover_bg, p)
        border = self._interpolate_color(self._base_border, self._hover_border, p)
        text = self._interpolate_color(self._base_text, self._hover_text, p)
        
        # Apply local stylesheet to override global, forcing animation and centering text
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg.name()};
                color: {text.name()};
                border: 1px solid {border.name()};
                border-radius: 8px;
                padding: 10px 16px;
                font-size: 12px;
                font-weight: 600;
                text-align: center;
            }}
            QPushButton:disabled {{
                background-color: #F8FAFC;
                color: #CBD5E1;
                border: 1px solid #F1F5F9;
            }}
        """)