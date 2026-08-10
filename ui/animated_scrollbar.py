from PyQt5.QtWidgets import QScrollBar, QStyle, QStyleOptionSlider
from PyQt5.QtCore import Qt, QVariantAnimation, QEasingCurve, QPropertyAnimation
from PyQt5.QtGui import QColor


class AnimatedScrollBar(QScrollBar):
    def __init__(self, orientation=Qt.Vertical, parent=None):
        super().__init__(orientation, parent)
        self._anim = QVariantAnimation(self)
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.InOutQuad)
        self._anim.valueChanged.connect(self._update_style)
        
        self._progress = 0.0
        self._base_bg = QColor(148, 163, 184, 60)
        self._hover_bg = QColor(6, 182, 212, 100)

        self._scroll_anim = None
        self._dragging = False
        self._drag_start_pos = None
        self._drag_start_val = 0
        
        self.setSingleStep(10)
        self.setPageStep(50)
        self._update_style(0.0)

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
        color_str = f"rgba({bg.red()}, {bg.green()}, {bg.blue()}, {bg.alpha()})"
        
        # Vertical needs margin-top to avoid covering the header
        if self.orientation() == Qt.Vertical:
            margin_str = "margin: 40px 0px 0px 0px;"
            dim_str = "width: 8px;"
        else:
            margin_str = "margin: 0px 0px 0px 0px;"
            dim_str = "height: 8px;"

        self.setStyleSheet(f"""
            QScrollBar:vertical, QScrollBar:horizontal {{
                border: none;
                background: transparent;
                {margin_str}
            }}
            QScrollBar:vertical {{ width: 8px; }}
            QScrollBar:horizontal {{ height: 8px; }}
            
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
                background: {color_str};
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{ min-height: 30px; }}
            QScrollBar::handle:horizontal {{ min-width: 30px; }}
            
            QScrollBar::add-line, QScrollBar::sub-line {{
                border: none;
                background: none;
                height: 0px;
                width: 0px;
            }}
            QScrollBar::add-page, QScrollBar::sub-page {{
                background: none;
            }}
        """)

    def wheelEvent(self, event):
        if self._dragging:
            return
            
        delta = event.angleDelta().y()
        if self.orientation() == Qt.Horizontal:
            delta = event.angleDelta().x() if event.angleDelta().x() != 0 else delta
            
        step = self.singleStep() * 3
        target_value = self.value() - (delta / 120) * step
        target_value = max(self.minimum(), min(self.maximum(), target_value))
        
        if self._scroll_anim:
            self._scroll_anim.stop()
            
        self._scroll_anim = QPropertyAnimation(self, b"value")
        self._scroll_anim.setDuration(250)
        self._scroll_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._scroll_anim.setStartValue(self.value())
        self._scroll_anim.setEndValue(target_value)
        self._scroll_anim.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            opt = QStyleOptionSlider()
            self.initStyleOption(opt)
            control = self.style().hitTestComplexControl(QStyle.CC_ScrollBar, opt, event.pos(), self)
            
            if control == QStyle.SC_ScrollBarSlider:
                self._dragging = True
                self._drag_start_pos = event.pos()
                self._drag_start_val = self.value()
                if self._scroll_anim:
                    self._scroll_anim.stop()
                event.accept()
            else:
                # Click on track: jump by page step smoothly
                if self.orientation() == Qt.Vertical:
                    if event.pos().y() < self.rect().center().y():
                        target = self.value() - self.pageStep()
                    else:
                        target = self.value() + self.pageStep()
                else:
                    if event.pos().x() < self.rect().center().x():
                        target = self.value() - self.pageStep()
                    else:
                        target = self.value() + self.pageStep()
                
                target = max(self.minimum(), min(self.maximum(), target))
                if self._scroll_anim:
                    self._scroll_anim.stop()
                self._scroll_anim = QPropertyAnimation(self, b"value")
                self._scroll_anim.setDuration(150)
                self._scroll_anim.setEasingCurve(QEasingCurve.OutCubic)
                self._scroll_anim.setStartValue(self.value())
                self._scroll_anim.setEndValue(target)
                self._scroll_anim.start()
                event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging:
            opt = QStyleOptionSlider()
            self.initStyleOption(opt)
            groove_rect = self.style().subControlRect(QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarGroove, self)
            slider_rect = self.style().subControlRect(QStyle.CC_ScrollBar, opt, QStyle.SC_ScrollBarSlider, self)
            
            if self.orientation() == Qt.Vertical:
                slider_len = slider_rect.height()
                groove_len = groove_rect.height()
                delta = event.pos().y() - self._drag_start_pos.y()
            else:
                slider_len = slider_rect.width()
                groove_len = groove_rect.width()
                delta = event.pos().x() - self._drag_start_pos.x()

            max_val = self.maximum() - self.minimum()
            if groove_len - slider_len > 0:
                new_val = self._drag_start_val + (delta * max_val) / (groove_len - slider_len)
            else:
                new_val = self._drag_start_val

            new_val = max(self.minimum(), min(self.maximum(), new_val))
            self.setValue(int(new_val))
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._dragging:
            self._dragging = False
            event.accept()
        else:
            super().mouseReleaseEvent(event)