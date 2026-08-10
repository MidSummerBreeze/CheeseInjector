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
        self._base_bg = QColor(255, 255, 255, 200)
        self._hover_bg = QColor(248, 250, 252, 220)
        self._base_border = QColor(226, 232, 240, 200)
        self._hover_border = QColor(6, 182, 212, 255)
        self._base_text = QColor(15, 23, 42, 255)
        self._hover_text = QColor(8, 145, 178, 255)
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
        a = int(c1.alpha() + (c2.alpha() - c1.alpha()) * p)
        return QColor(r, g, b, a)

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
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba({bg.red()}, {bg.green()}, {bg.blue()}, {bg.alpha()});
                color: rgba({text.red()}, {text.green()}, {text.blue()}, {text.alpha()});
                border: 1px solid rgba({border.red()}, {border.green()}, {border.blue()}, {border.alpha()});
                border-radius: 8px;
                padding: 10px 16px;
                font-size: 12px;
                font-weight: 600;
                text-align: center;
            }}
            QPushButton:disabled {{
                background-color: rgba(248, 250, 252, 100);
                color: rgba(203, 213, 225, 200);
                border: 1px solid rgba(241, 245, 249, 150);
            }}
        """)

class AnimatedIconButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._anim = QVariantAnimation(self)
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.InOutQuad)
        self._anim.valueChanged.connect(self._update_style)
        self._progress = 0.0
        self._base_bg = QColor(255, 255, 255, 0)
        self._hover_bg = QColor(239, 68, 68, 180)
        self._base_text = QColor(148, 163, 184)
        self._hover_text = QColor(255, 255, 255, 255)
        self._border_radius = 6
        self._update_style(0.0)

    def set_theme(self, base_bg, hover_bg, base_text, hover_text, radius=6):
        self._base_bg = base_bg
        self._hover_bg = hover_bg
        self._base_text = base_text
        self._hover_text = hover_text
        self._border_radius = radius
        self._update_style(self._progress)

    def _interpolate_color(self, c1: QColor, c2: QColor, p: float) -> QColor:
        r = int(c1.red() + (c2.red() - c1.red()) * p)
        g = int(c1.green() + (c2.green() - c1.green()) * p)
        b = int(c1.blue() + (c2.blue() - c1.blue()) * p)
        a = int(c1.alpha() + (c2.alpha() - c1.alpha()) * p)
        return QColor(r, g, b, a)

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
        text = self._interpolate_color(self._base_text, self._hover_text, p)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba({bg.red()}, {bg.green()}, {bg.blue()}, {bg.alpha()});
                color: rgba({text.red()}, {text.green()}, {text.blue()}, {text.alpha()});
                border: none;
                border-radius: {self._border_radius}px;
                font-size: 13px;
                padding: 0px;
            }}
        """)
