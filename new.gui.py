from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QPushButton, QLabel, QHBoxLayout,
    QVBoxLayout, QStackedWidget, QSizePolicy, QGridLayout, QSpacerItem
)
from PyQt6.QtCore import Qt
import sys

# Colors for light and dark mode
LIGHT_GREEN = "#a8d5a2"
DARK_GREEN = "#3a5f41"
BUTTON_HOVER_DARKEN = "#2f4f2d"

class WelcomePage(QWidget):
    """Welcome page with two main buttons"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setSpacing(50)

        self.adjust_btn = QPushButton("Adjust NanoLab Settings")
        self.view_data_btn = QPushButton("View Collected Data")

        for btn in (self.adjust_btn, self.view_data_btn):
            btn.setFixedHeight(70)
            btn.setStyleSheet(self.button_style())
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(self.adjust_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.view_data_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

    def button_style(self):
        return f"""
            QPushButton {{
                background-color: {LIGHT_GREEN};
                border: none;
                border-radius: 10px;
                font-size: 20px;
                font-weight: bold;
                color: black;
                min-width: 300px;
            }}
            QPushButton:hover {{
                background-color: {BUTTON_HOVER_DARKEN};
                color: white;
            }}
        """

class AdjustNanoLabSettingsPage(QWidget):
    """Adjust NanoLab Settings page with multiple placeholder buttons"""
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(100, 50, 100, 50)
        main_layout.setSpacing(20)

        title = QLabel("Adjust NanoLab Settings")
        title.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {DARK_GREEN};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Button names as requested
        button_names = [
            "Data Results",
            "Water Pump Settings",
            "LED Settings",
            "Fan Settings",
            "Camera Settings",
            "Atmospheric Sensor",
        ]

        # Grid layout 3x2 for buttons
        grid = QGridLayout()
        grid.setSpacing(20)

        positions = [(i, j) for i in range(2) for j in range(3)]  # 2 rows x 3 cols

        for position, name in zip(positions, button_names):
            btn = QPushButton(name)
            btn.setFixedHeight(80)
            btn.setMinimumWidth(180)
            btn.setStyleSheet(self.button_style())
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            grid.addWidget(btn, *position, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(grid)
        main_layout.addStretch()

        # Bottom right button layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        sent_button = QPushButton("Sent to your NanoLab")
        sent_button.setFixedHeight(40)
        sent_button.setStyleSheet(self.button_style())
        sent_button.setCursor(Qt.CursorShape.PointingHandCursor)
        bottom_layout.addWidget(sent_button)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def button_style(self):
        return f"""
            QPushButton {{
                background-color: {LIGHT_GREEN};
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                color: black;
                padding-left: 15px;
                padding-right: 15px;
            }}
            QPushButton:hover {{
                background-color: {BUTTON_HOVER_DARKEN};
                color: white;
            }}
        """

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NanoLab Control Panel")
        self.resize(1000, 700)  # Initial window size

        # Central widget is a stacked widget for pages
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create pages
        self.welcome_page = WelcomePage()
        self.adjust_page = AdjustNanoLabSettingsPage()

        # Add pages to stack
        self.stack.addWidget(self.welcome_page)      # index 0
        self.stack.addWidget(self.adjust_page)       # index 1

        # Navigation history stack and pointer
        self.history = []
        self.history_index = -1

        # Top navigation bar with back/forward buttons centered
        top_bar_widget = QWidget()
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(0, 10, 0, 10)
        top_bar_layout.setSpacing(40)

        self.back_button = QPushButton("← Back")
        self.back_button.setFixedSize(140, 50)
        self.back_button.setStyleSheet(self.button_style())
        self.back_button.setEnabled(False)  # Disabled initially
        self.back_button.clicked.connect(self.go_back)

        self.forward_button = QPushButton("Forward →")
        self.forward_button.setFixedSize(140, 50)
        self.forward_button.setStyleSheet(self.button_style())
        self.forward_button.setEnabled(False)
        self.forward_button.clicked.connect(self.go_forward)

        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.back_button)
        top_bar_layout.addWidget(self.forward_button)
        top_bar_layout.addStretch()

        top_bar_widget.setLayout(top_bar_layout)

        # Create main layout with top bar and stacked widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_bar_widget)
        main_layout.addWidget(self.stack)

        # A container widget for main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connect buttons on welcome page to navigate
        self.welcome_page.adjust_btn.clicked.connect(lambda: self.navigate_to(1))
        # For demo, view_data_btn just shows a message box
        self.welcome_page.view_data_btn.clicked.connect(self.show_data_message)

        # Start with welcome page, update history
        self.navigate_to(0)

    def button_style(self):
        return f"""
            QPushButton {{
                background-color: {LIGHT_GREEN};
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 18px;
                color: black;
            }}
            QPushButton:hover {{
                background-color: {BUTTON_HOVER_DARKEN};
                color: white;
            }}
        """

    def navigate_to(self, index):
        # If going forward from somewhere in history, trim forward history first
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index+1]

        self.history.append(index)
        self.history_index += 1
        self.stack.setCurrentIndex(index)
        self.update_nav_buttons()

    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.stack.setCurrentIndex(self.history[self.history_index])
            self.update_nav_buttons()

    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.stack.setCurrentIndex(self.history[self.history_index])
            self.update_nav_buttons()

    def update_nav_buttons(self):
        self.back_button.setEnabled(self.history_index > 0)
        self.forward_button.setEnabled(self.history_index < len(self.history) - 1)

    def show_data_message(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "View Data", "This feature is not implemented yet.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
