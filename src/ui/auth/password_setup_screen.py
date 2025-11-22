from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QFrame)
from PySide6.QtCore import Qt, Signal

class PasswordSetupScreen(QWidget):
    password_set = Signal()
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Setup first-time password creation UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Setup container
        setup_container = QFrame()
        setup_container.setFixedSize(450, 550)
        setup_container.setStyleSheet("""
            QFrame {
                background-color: #2d2d30;
                border-radius: 15px;
                border: 2px solid #3e3e42;
            }
        """)
        
        container_layout = QVBoxLayout(setup_container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)
        
        # Welcome message
        welcome_label = QLabel("Setup Password")
        welcome_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #60a5fa;
            margin-bottom: 10px;
        """)
        welcome_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(welcome_label)
        
        # Subtitle
        subtitle = QLabel("Create a password to protect your application")
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #9ca3af;
            margin-bottom: 20px;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        container_layout.addWidget(subtitle)
        
        # Password input
        password_label = QLabel("New Password:")
        password_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 10px;
        """)
        container_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                border: 2px solid #3e3e42;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #60a5fa;
            }
        """)
        container_layout.addWidget(self.password_input)
        
        # Confirm password input
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 10px;
        """)
        container_layout.addWidget(confirm_label)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setPlaceholderText("Confirm your password")
        self.confirm_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                border: 2px solid #3e3e42;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #60a5fa;
            }
        """)
        self.confirm_input.returnPressed.connect(self.create_password)
        container_layout.addWidget(self.confirm_input)
        
        # Password requirements
        requirements = QLabel("- Minimum 4 characters\n- Choose something memorable")
        requirements.setStyleSheet("""
            color: #9ca3af;
            font-size: 12px;
            margin-top: 10px;
        """)
        container_layout.addWidget(requirements)
        
        # Create button
        self.create_button = QPushButton("Create Password")
        self.create_button.setFixedHeight(75)
        self.create_button.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #047857;
            }
        """)
        self.create_button.clicked.connect(self.create_password)
        container_layout.addWidget(self.create_button)
        
        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("""
            color: #ef4444;
            font-size: 13px;
            margin-top: 10px;
        """)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        container_layout.addWidget(self.error_label)
        
        container_layout.addStretch()
        
        main_layout.addWidget(setup_container)
        
        # Focus on password input
        self.password_input.setFocus()
        
    def create_password(self):
        """Create new password"""
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        # Validation
        if not password:
            self.show_error("Please enter a password")
            return
        
        if len(password) < 4:
            self.show_error("Password must be at least 4 characters long")
            return
        
        if password != confirm:
            self.show_error("Passwords do not match")
            return
        
        # Save password
        try:
            self.db_manager.set_password(password)
            QMessageBox.information(
                self,
                "Success",
                "Password created successfully!\n\nPlease remember your password."
            )
            self.password_set.emit()
        except Exception as e:
            self.show_error(f"Error creating password: {str(e)}")
    
    def show_error(self, message):
        """Show error message"""
        self.error_label.setText(message)
        self.error_label.show()