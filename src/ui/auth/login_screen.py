from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QHBoxLayout, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap

class LoginScreen(QWidget):
    login_successful = Signal()
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Setup login screen UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Login container
        login_container = QFrame()
        login_container.setFixedSize(400, 450)
        login_container.setStyleSheet("""
            QFrame {
                background-color: #2d2d30;
                border-radius: 15px;
                border: 2px solid #3e3e42;
            }
        """)
        
        container_layout = QVBoxLayout(login_container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)
        
        # Company name
        company_name = self.db_manager.get_company_name()
        company_label = QLabel(company_name if company_name else "Stock Management")
        company_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #60a5fa;
            margin-bottom: 10px;
        """)
        company_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(company_label)
        
        # Subtitle
        subtitle = QLabel("Enter your password to continue")
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #9ca3af;
            margin-bottom: 20px;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(subtitle)
        
        # Password input
        password_label = QLabel("Password:")
        password_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 20px;
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
        self.password_input.returnPressed.connect(self.attempt_login)
        container_layout.addWidget(self.password_input)
        
        # Show/Hide password checkbox
        show_password_layout = QHBoxLayout()
        self.show_password_btn = QPushButton("Show Password")
        self.show_password_btn.setCheckable(True)
        self.show_password_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #60a5fa;
                border: none;
                text-align: left;
                padding: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #3b82f6;
                text-decoration: underline;
            }
        """)
        self.show_password_btn.toggled.connect(self.toggle_password_visibility)
        show_password_layout.addWidget(self.show_password_btn)
        show_password_layout.addStretch()
        container_layout.addLayout(show_password_layout)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #60a5fa;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #3b82f6;
            }
            QPushButton:pressed {
                background-color: #2563eb;
            }
        """)
        self.login_button.clicked.connect(self.attempt_login)
        container_layout.addWidget(self.login_button)
        
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
        
        main_layout.addWidget(login_container)
        
        # Focus on password input
        self.password_input.setFocus()
        
    def toggle_password_visibility(self, checked):
        """Toggle password visibility"""
        if checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_btn.setText("Hide Password")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_password_btn.setText("Show Password")
    
    def attempt_login(self):
        """Attempt to login with entered password"""
        password = self.password_input.text().strip()
        
        if not password:
            self.show_error("Please enter a password")
            return
        
        if self.db_manager.verify_password(password):
            self.error_label.hide()
            self.login_successful.emit()
        else:
            self.show_error("Incorrect password. Please try again.")
            self.password_input.clear()
            self.password_input.setFocus()
    
    def show_error(self, message):
        """Show error message"""
        self.error_label.setText(message)
        self.error_label.show()
        
    def clear_form(self):
        """Clear the form"""
        self.password_input.clear()
        self.error_label.hide()
        self.password_input.setFocus()