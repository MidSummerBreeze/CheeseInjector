from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QVBoxLayout, QWidget, QAbstractItemView
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from ui.animated_scrollbar import AnimatedScrollBar


class SmoothScrollTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Enable pixel-by-pixel scrolling for a smoother experience
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        
        # Use custom scrollbar to prevent native bugs
        self.setVerticalScrollBar(AnimatedScrollBar(Qt.Vertical, self))
        self.setHorizontalScrollBar(AnimatedScrollBar(Qt.Horizontal, self))

    def wheelEvent(self, event):
        # Directly let the underlying view handle the pixel scroll
        # This eliminates any animation skipping bugs
        super().wheelEvent(event)


class ProcessTable(QWidget):
    process_selected = pyqtSignal(dict)
    process_double_clicked = pyqtSignal(dict)
    COLUMNS = ["PID", "Process", "Window Title"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._processes = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.table = SmoothScrollTable()
        self.table.setObjectName("tableWidget")
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        
        # Disable editing and header interaction
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setSectionsClickable(False)
        self.table.horizontalHeader().setHighlightSections(False)
        
        # Force header to use QSS and become transparent for Acrylic
        self.table.horizontalHeader().setAttribute(Qt.WA_StyledBackground, True)
        self.table.horizontalHeader().setAutoFillBackground(False)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.itemClicked.connect(self._on_item_clicked)
        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)

        self.table.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.table)

        self.empty_label = QLabel('Click "Scan Processes" to begin')
        self.empty_label.setObjectName("emptyLabel")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setVisible(False)
        layout.addWidget(self.empty_label)

    def set_processes(self, processes: list):
        self._processes = processes
        self.table.clearContents()

        if not processes:
            self.table.setRowCount(0)
            self.table.setVisible(False)
            self.empty_label.setVisible(True)
            self.empty_label.setText("No Java processes found")
            return

        self.table.setVisible(True)
        self.empty_label.setVisible(False)
        self.table.setRowCount(len(processes))

        for i, proc in enumerate(processes):
            pid_item = QTableWidgetItem(str(proc["pid"]))
            pid_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, pid_item)

            name_item = QTableWidgetItem(proc["name"])
            name_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, name_item)

            title_item = QTableWidgetItem(proc["title"])
            title_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 2, title_item)

        self.table.resizeColumnToContents(0)
        self.table.resizeColumnToContents(1)

    def show_loading(self):
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setVisible(False)
        self.empty_label.setVisible(True)
        self.empty_label.setText("Scanning...")

    def clear(self):
        self._processes = []
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setVisible(False)
        self.empty_label.setVisible(True)
        self.empty_label.setText('Click "Scan Processes" to begin')

    def _on_item_clicked(self, item):
        if 0 <= item.row() < len(self._processes):
            self.process_selected.emit(self._processes[item.row()])

    def _on_item_double_clicked(self, item):
        if 0 <= item.row() < len(self._processes):
            self.process_double_clicked.emit(self._processes[item.row()])