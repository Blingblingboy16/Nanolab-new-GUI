from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QPushButton, QLabel, QHBoxLayout,
    QVBoxLayout, QStackedWidget, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt
import sys

# Colors (keep as is)
LIGHT_GREEN = "#a8d5a2"
DARK_GREEN = "#3a5f41"
BUTTON_HOVER_DARKEN = "#2f4f2d"

class TopBar(QWidget):
    """Top bar with back/forward buttons and menu options"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(70)  # Bigger height to fit bigger buttons
        self.setStyleSheet(f"background-color: {DARK_GREEN};")

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(40)

        # Back button - bigger size
        self.back_button = QPushButton("←")
        self.back_button.setFixedSize(60, 50)  # Bigger size
        self.back_button.setStyleSheet(self.button_style())
        self.back_button.setEnabled(False)  # Initially disabled
        layout.addWidget(self.back_button)

        # Forward button - bigger size
        self.forward_button = QPushButton("→")
        self.forward_button.setFixedSize(60, 50)  # Bigger size
        self.forward_button.setStyleSheet(self.button_style())
        self.forward_button.setEnabled(False)  # Initially disabled
        layout.addWidget(self.forward_button)

        # Spacer between arrows and menu
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Menu buttons (About, Updates, Storage, Log) same as before
        self.about_btn = QPushButton("About")
        self.updates_btn = QPushButton("Updates")
        self.storage_btn = QPushButton("Storage")
        self.log_btn = QPushButton("Log")

        for btn in (self.about_btn, self.updates_btn, self.storage_btn, self.log_btn):
            btn.setStyleSheet(self.menu_button_style())
            btn.setFixedHeight(35)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            layout.addWidget(btn)

        self.setLayout(layout)

    def button_style(self):
        return f"""
            QPushButton {{
                background-color: {LIGHT_GREEN};
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 28px;
                color: black;
            }}
            QPushButton:hover {{
                background-color: {BUTTON_HOVER_DARKEN};
                color: white;
            }}
            QPushButton:disabled {{
                background-color: #a0bfa0;
                color: #666666;
            }}
        """

    def menu_button_style(self):
        return f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                color: {LIGHT_GREEN};
            }}
        """

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NanoLab Control Panel")
        self.resize(1000, 700)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.welcome_page = WelcomePage()
        self.adjust_page = AdjustNanoLabSettingsPage()

        self.stack.addWidget(self.welcome_page)  # 0
        self.stack.addWidget(self.adjust_page)   # 1

        self.topbar = TopBar()
        self.setMenuWidget(self.topbar)

        # Navigation history management
        self.history = [0]  # start with welcome page index
        self.current_index = 0

        # Connect buttons
        self.topbar.back_button.clicked.connect(self.go_back)
        self.topbar.forward_button.clicked.connect(self.go_forward)
        self.welcome_page.adjust_btn.clicked.connect(lambda: self.navigate_to(1))
        self.topbar.about_btn.clicked.connect(lambda: self.show_message("About", "This is NanoLab Control Panel."))

        # Initially show welcome page
        self.stack.setCurrentIndex(0)
        self.update_nav_buttons()

    def navigate_to(self, page_index):
        # If we go to a new page, remove "forward" history
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        self.history.append(page_index)
        self.current_index += 1
        self.stack.setCurrentIndex(page_index)
        self.update_nav_buttons()

    def go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            page_index = self.history[self.current_index]
            self.stack.setCurrentIndex(page_index)
            self.update_nav_buttons()

    def go_forward(self):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            page_index = self.history[self.current_index]
            self.stack.setCurrentIndex(page_index)
            self.update_nav_buttons()

    def update_nav_buttons(self):
        # Enable/disable back and forward buttons based on history position
        self.topbar.back_button.setEnabled(self.current_index > 0)
        self.topbar.forward_button.setEnabled(self.current_index < len(self.history) - 1)

    def show_message(self, title, message):
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

# Your existing page classes (WelcomePage, AdjustNanoLabSettingsPage) here
# (unchanged)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
