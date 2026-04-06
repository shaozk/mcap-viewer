from mcap import __version__
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.mcap_version_label = QLabel(f"mcap version: {__version__}")
        self.layout.addWidget(self.mcap_version_label)
        self.setLayout(self.layout)
