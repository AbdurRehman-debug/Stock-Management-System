from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QFrame, QHBoxLayout)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from ...database.database_manager import DatabaseManager
class PasswordSettingsPage(QWidget):
    password_changed = Signal()
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup password settings UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QScrollArea {
                border: none;
                background-color: #1e1e1e;
            }
            QScrollBar:vertical {
                background-color: #2d2d30;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #60a5fa;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #3b82f6;
            }
        """)
        
        # Create scroll area
        from PySide6.QtWidgets import QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create content widget
        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d30;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel("Password Settings")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #60a5fa;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        title.setAlignment(Qt.AlignCenter)
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Change your application password")
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #9ca3af;
            margin-top: 5px;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header_frame)
        
        # Change Password Form
        form_frame = QFrame()
        form_frame.setMaximumWidth(600)
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d30;
                border-radius: 12px;
                padding: 30px;
            }
        """)
        
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
        # Current Password
        current_label = QLabel("Current Password:")
        current_label.setMinimumHeight(25)
        current_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #ffffff;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        
        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.current_password_input.setPlaceholderText("Enter your current password")
        self.current_password_input.setStyleSheet(self.input_style())
        
        form_layout.addWidget(current_label)
        form_layout.addWidget(self.current_password_input)
        
        # New Password
        new_label = QLabel("New Password:")
        new_label.setMinimumHeight(25)
        new_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 10px;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setPlaceholderText("Enter your new password")
        self.new_password_input.setStyleSheet(self.input_style())
        
        form_layout.addWidget(new_label)
        form_layout.addWidget(self.new_password_input)
        
        # Confirm New Password
        confirm_label = QLabel("Confirm New Password:")
        confirm_label.setMinimumHeight(25)
        confirm_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 10px;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Confirm your new password")
        self.confirm_password_input.setStyleSheet(self.input_style())
        self.confirm_password_input.returnPressed.connect(self.change_password)
        
        form_layout.addWidget(confirm_label)
        form_layout.addWidget(self.confirm_password_input)
        
        # Show/Hide password buttons
        show_password_layout = QHBoxLayout()
        
        self.show_current_btn = QPushButton("Show Current")
        self.show_current_btn.setCheckable(True)
        self.show_current_btn.setStyleSheet(self.toggle_button_style())
        self.show_current_btn.toggled.connect(self.toggle_current_password)
        
        self.show_new_btn = QPushButton("Show New")
        self.show_new_btn.setCheckable(True)
        self.show_new_btn.setStyleSheet(self.toggle_button_style())
        self.show_new_btn.toggled.connect(self.toggle_new_password)
        
        show_password_layout.addWidget(self.show_current_btn)
        show_password_layout.addWidget(self.show_new_btn)
        show_password_layout.addStretch()
        
        form_layout.addLayout(show_password_layout)
        
        # Password requirements
        requirements = QLabel("- Minimum 4 characters\n- New password must be different from current")
        requirements.setMinimumHeight(50)
        requirements.setStyleSheet("""
            color: #9ca3af;
            font-size: 12px;
            padding: 10px;
            background-color: #1e1e1e;
            border-radius: 6px;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        form_layout.addWidget(requirements)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.change_button = QPushButton("Change Password")
        self.change_button.setMinimumHeight(40)
        self.change_button.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #047857;
            }
        """)
        self.change_button.clicked.connect(self.change_password)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.setMinimumHeight(40)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
            QPushButton:pressed {
                background-color: #374151;
            }
        """)
        self.clear_button.clicked.connect(self.clear_form)
        
        button_layout.addStretch()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.change_button)
        
        form_layout.addLayout(button_layout)
        
        # Error/Success label
        self.message_label = QLabel("")
        self.message_label.setMinimumHeight(50)
        self.message_label.setStyleSheet("""
            font-size: 13px;
            padding: 10px;
            border-radius: 6px;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        self.message_label.hide()
        
        form_layout.addWidget(self.message_label)
        
        # Center the form
        form_container = QHBoxLayout()
        form_container.addStretch()
        form_container.addWidget(form_frame)
        form_container.addStretch()
        
        main_layout.addLayout(form_container)
        content_widget.setMinimumHeight(1200)
        
        # Set content widget to scroll area
        scroll_area.setWidget(content_widget)
        
        # Set scroll area as main layout
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll_area)
        
    def input_style(self):
        """Input field style"""
        return """
            QLineEdit {
                background-color: #1e1e1e;
                border: 2px solid #3e3e42;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                color: #ffffff;
                min-height: 40px;
            }
            QLineEdit:focus {
                border-color: #60a5fa;
            }
        """
    
    def toggle_button_style(self):
        """Toggle button style"""
        return """
            QPushButton {
                background-color: transparent;
                color: #60a5fa;
                border: none;
                text-align: left;
                padding: 5px 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #3b82f6;
            }
            QPushButton:checked {
                color: #10b981;
            }
        """
    
    def toggle_current_password(self, checked):
        """Toggle current password visibility"""
        if checked:
            self.current_password_input.setEchoMode(QLineEdit.Normal)
            self.show_current_btn.setText("Hide Current")
        else:
            self.current_password_input.setEchoMode(QLineEdit.Password)
            self.show_current_btn.setText("Show Current")
    
    def toggle_new_password(self, checked):
        """Toggle new password visibility"""
        if checked:
            self.new_password_input.setEchoMode(QLineEdit.Normal)
            self.confirm_password_input.setEchoMode(QLineEdit.Normal)
            self.show_new_btn.setText("Hide New")
        else:
            self.new_password_input.setEchoMode(QLineEdit.Password)
            self.confirm_password_input.setEchoMode(QLineEdit.Password)
            self.show_new_btn.setText("Show New")
    
    def change_password(self):
        """Change the password"""
        current_password = self.current_password_input.text().strip()
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        
        # Validation
        if not current_password:
            self.show_error("Please enter your current password")
            return
        
        if not new_password:
            self.show_error("Please enter a new password")
            return
        
        if len(new_password) < 4:
            self.show_error("New password must be at least 4 characters long")
            return
        
        if new_password != confirm_password:
            self.show_error("New passwords do not match")
            return
        
        if current_password == new_password:
            self.show_error("New password must be different from current password")
            return
        
        # Attempt to change password
        success, message = self.db_manager.change_password(current_password, new_password)
        
        if success:
            self.show_success(message)
            self.clear_form()
            self.password_changed.emit()
            
            # Show confirmation dialog
            QMessageBox.information(
                self,
                "Success",
                "Password changed successfully!\n\nPlease remember your new password."
            )
        else:
            self.show_error(message)
    
    def clear_form(self):
        """Clear all input fields"""
        self.current_password_input.clear()
        self.new_password_input.clear()
        self.confirm_password_input.clear()
        self.message_label.hide()
        self.show_current_btn.setChecked(False)
        self.show_new_btn.setChecked(False)
        self.current_password_input.setFocus()
    
    def show_error(self, message):
        """Show error message"""
        self.message_label.setText(f"Error: {message}")
        self.message_label.setStyleSheet("""
            font-size: 13px;
            padding: 10px;
            border-radius: 6px;
            background-color: #7f1d1d;
            color: #fca5a5;
            min-height: 50px;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        self.message_label.show()
    
    def show_success(self, message):
        """Show success message"""
        self.message_label.setText(f"Success: {message}")
        self.message_label.setStyleSheet("""
            font-size: 13px;
            padding: 10px;
            border-radius: 6px;
            background-color: #064e3b;
            color: #6ee7b7;
            min-height: 50px;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        self.message_label.show()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # For testing - you'll need to import DatabaseManager
    # from database.database_manager import DatabaseManager
    # db = DatabaseManager()
    # window = PasswordSettingsPage(db)
    # window.show()
    
    sys.exit(app.exec())