from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer, QSize
from PyQt5.QtGui import QColor
from ui.animated_button import AnimatedIconButton

class ToastNotification(QFrame):
    def __init__(self, title, message, toast_type="info", duration=3000, qt_parent=None, manager=None):
        super().__init__(qt_parent)
        self.setObjectName("toast")
        self.setFixedWidth(300)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.duration = duration
        self.parent_manager = manager
        color_map = {
            "success": "#06B6D4",
            "error": "#EF4444",
            "warning": "#F59E0B",
            "info": "#64748B"
        }
        accent_color = color_map.get(toast_type, "#64748B")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(6)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)
        self.title_label = QLabel(title)
        self.title_label.setObjectName("toastTitle")
        self.title_label.setStyleSheet(f"color: {accent_color}; font-weight: 600;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        self.close_btn = AnimatedIconButton("✕")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.set_theme(
            base_bg=QColor(255, 255, 255, 0),
            hover_bg=QColor(239, 68, 68, 180),
            base_text=QColor(148, 163, 184, 255),
            hover_text=QColor(255, 255, 255, 255),
            radius=4
        )
        self.close_btn.clicked.connect(self.hide_anim)
        header_layout.addWidget(self.close_btn)
        main_layout.addLayout(header_layout)
        self.msg_label = QLabel(message)
        self.msg_label.setObjectName("toastMessage")
        self.msg_label.setWordWrap(True)
        self.msg_label.setStyleSheet("color: #334155;")
        main_layout.addWidget(self.msg_label)
        progress_container = QFrame()
        progress_container.setFixedHeight(3)
        progress_container.setStyleSheet("background-color: #E2E8F0; border-radius: 1px;")
        self.progress_chunk = QFrame(progress_container)
        self.progress_chunk.setStyleSheet(f"background-color: {accent_color}; border-radius: 1px; border: none;")
        self.progress_chunk.move(0, 0)
        self.progress_chunk.resize(0, 3)
        main_layout.addWidget(progress_container)
        self.adjustSize()
        self.anim_pos = QPropertyAnimation(self, b"pos")
        self.anim_pos.setDuration(300)
        self.anim_pos.setEasingCurve(QEasingCurve.OutCubic)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.anim_opacity = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim_opacity.setDuration(300)
        self.anim_opacity.setEasingCurve(QEasingCurve.OutCubic)
        self.anim_progress = QPropertyAnimation(self.progress_chunk, b"size")
        self.anim_progress.setDuration(duration)
        self.anim_progress.setStartValue(QSize(0, 3))
        self.anim_progress.setEndValue(QSize(268, 3))
        self.anim_progress.setEasingCurve(QEasingCurve.Linear)
        self.anim_out_timer = QTimer(self)
        self.anim_out_timer.setSingleShot(True)
        self.anim_out_timer.timeout.connect(self.hide_anim)

    def start_anim(self, start_pos, end_pos):
        self.move(start_pos)
        self.progress_chunk.resize(0, 3)
        self.show()
        self.raise_()
        self.anim_pos.setStartValue(start_pos)
        self.anim_pos.setEndValue(end_pos)
        self.anim_pos.start()
        self.anim_opacity.setStartValue(0.0)
        self.anim_opacity.setEndValue(1.0)
        self.anim_opacity.start()
        self.anim_progress.start()
        self.anim_out_timer.start(self.duration)

    def hide_anim(self):
        try:
            self.anim_out_timer.disconnect()
        except:
            pass
        self.anim_pos.stop()
        self.anim_opacity.stop()
        self.anim_progress.stop()
        current_pos = self.pos()
        end_pos = QPoint(current_pos.x(), current_pos.y() - 50)
        self.anim_pos.setDuration(300)
        self.anim_pos.setEasingCurve(QEasingCurve.InCubic)
        self.anim_pos.setStartValue(current_pos)
        self.anim_pos.setEndValue(end_pos)
        try:
            self.anim_pos.finished.disconnect()
        except:
            pass
        self.anim_pos.finished.connect(self.delete_self)
        self.anim_pos.start()
        self.anim_opacity.setDuration(300)
        self.anim_opacity.setEasingCurve(QEasingCurve.InCubic)
        self.anim_opacity.setStartValue(1.0)
        self.anim_opacity.setEndValue(0.0)
        self.anim_opacity.start()

    def delete_self(self):
        if self.parent_manager:
            self.parent_manager.remove_toast(self)
        self.deleteLater()

class ToastManager:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.active_toasts = []

    def show_toast(self, title, message, toast_type="info", duration=3000):
        if len(message) > 50:
            duration = 5000
        toast = ToastNotification(title, message, toast_type, duration, self.parent_window, self)
        parent_rect = self.parent_window.rect()
        toast_w = toast.width()
        toast_h = toast.height()
        margin = 20
        y_offset = margin
        for t in self.active_toasts:
            y_offset += t.height() + 10
        end_pos = QPoint(parent_rect.width() - toast_w - margin, y_offset)
        start_pos = QPoint(parent_rect.width() - toast_w - margin, -toast_h - 20)
        self.active_toasts.append(toast)
        toast.start_anim(start_pos, end_pos)

    def remove_toast(self, toast):
        if toast in self.active_toasts:
            self.active_toasts.remove(toast)
        margin = 20
        y_offset = margin
        for t in self.active_toasts:
            current_x = t.pos().x()
            target_y = y_offset
            if t.pos().y() != target_y:
                t.anim_pos.stop()
                t.anim_pos.setDuration(200)
                t.anim_pos.setEasingCurve(QEasingCurve.OutCubic)
                t.anim_pos.setStartValue(t.pos())
                t.anim_pos.setEndValue(QPoint(current_x, target_y))
                t.anim_pos.start()
            y_offset += t.height() + 10
