from mcap.reader import make_reader
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMenu,
    QToolBar,
)

from mcap_viewer.ui.aboutwindow import AboutWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mcap-viewer")
        self.setGeometry(100, 100, 800, 600)

        self.menu_bar = self.menuBar()
        self.tool_bar = QToolBar("tool-bar")
        self.addToolBar(self.tool_bar)
        self.about_window = AboutWindow()

        self._set_file_menu()
        self._set_help_menu()

    def _set_menu_bar(self):
        pass

    def _set_tool_bar(self):
        pass

    def _set_file_menu(self):
        # File Menu
        self.file_menu = QMenu("&File", self)
        self.menu_bar.addMenu(self.file_menu)

        # New Window Action
        self.new_window_action = QAction("New Window", self)
        self.new_window_action.triggered.connect(self.open_new_window)
        self.file_menu.addAction(self.new_window_action)

        self.file_menu.addSeparator()

        # Add File Action
        self.add_file_action = QAction("Open File...", self)
        self.add_file_action.triggered.connect(self.open_file)
        self.file_menu.addAction(self.add_file_action)
        self.tool_bar.addAction(self.add_file_action)

        # Recent Files Submenu
        self.recent_menu = QMenu("Open Recent", self)
        self.file_menu.addMenu(self.recent_menu)
        self.update_recent_files_menu()  # populate on startup

        self.file_menu.addSeparator()

        # Exit Action
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)
        self.tool_bar.addAction(self.exit_action)

    def _set_help_menu(self):
        # Help Menu
        self.help_menu = QMenu("&Help", self)
        self.menu_bar.addMenu(self.help_menu)

        # About Action
        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.open_about_window)
        self.help_menu.addAction(self.about_action)
        self.tool_bar.addAction(self.about_action)

    def _open_mcap(self, mcap_path: str):
        with open(mcap_path, "rb") as f:
            reader = make_reader(f)
            summary = reader.get_summary()
            print(summary)
            self.label = QLabel("summary")
            self.setCentralWidget(self.label)

    def open_new_window(self):
        self.new_window = MainWindow()
        self.new_window.show()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "mcap Files (*.mcap);;All Files (*)"
        )
        if file_path:
            self.add_to_recent_files(file_path)
            self._open_mcap(file_path)

    def add_to_recent_files(self, file_path):
        settings = QSettings("mcap_viewer", "recent_files")
        files = settings.value("files", [])
        if file_path in files:
            files.remove(file_path)
        files.insert(0, file_path)
        files = files[:10]  # keep only 10
        settings.setValue("files", files)
        self.update_recent_files_menu()

    def update_recent_files_menu(self):
        self.recent_menu.clear()
        settings = QSettings("mcap_viewer", "recent_files")
        files = settings.value("files", [])
        if not files:
            action = QAction("No Recent Files", self)
            action.setEnabled(False)
            self.recent_menu.addAction(action)
        else:
            for file_path in files:
                action = QAction(file_path, self)
                action.triggered.connect(
                    lambda checked, f=file_path: self.open_recent_file(f)
                )
                self.recent_menu.addAction(action)

    def open_recent_file(self, file_path):
        self.add_to_recent_files(file_path)
        self._open_mcap(file_path)

    def open_about_window(self):
        self.about_window.show()
