from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel, 
                             QPushButton, QFrame, QScrollArea, QHBoxLayout, 
                             QMessageBox, QLineEdit, QComboBox, QGridLayout, 
                             QProgressBar, QDialog, QFormLayout, QDoubleSpinBox,
                             QDialogButtonBox, QTextEdit)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont
from ....database.database_manager import DatabaseManager
import datetime


class PaymentDialog(QDialog):
    """Dialog for processing partial payments"""
    
    def __init__(self, customer_data, parent=None):
        super().__init__(parent)
        self.customer_data = customer_data
        self.db_manager = DatabaseManager()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup payment dialog UI"""
        self.setWindowTitle("Process Payment")
        self.setFixedSize(400, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QLineEdit, QDoubleSpinBox, QTextEdit, QComboBox {
                background-color: #34495e;
                border: 2px solid #7f8c8d;
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus, QDoubleSpinBox:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Customer info header
        header_label = QLabel(f"Payment for: {self.customer_data.get('name', 'Unknown Customer')}")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db;")
        layout.addWidget(header_label)
        
        # Outstanding balance info
        balance_due = self.customer_data.get('balance_due', 0)
        balance_label = QLabel(f"Outstanding Balance: PKR {balance_due:,.2f}")
        balance_label.setStyleSheet("font-size: 16px; color: #e74c3c; font-weight: bold;")
        layout.addWidget(balance_label)
        
        # Payment form
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # Payment amount
        self.payment_amount = QDoubleSpinBox()
        self.payment_amount.setRange(0.01, balance_due)
        self.payment_amount.setDecimals(2)
        self.payment_amount.setValue(balance_due)  # Default to full payment
        self.payment_amount.setSuffix(" PKR")
        form_layout.addRow("Payment Amount:", self.payment_amount)
        
        # Payment method
        self.payment_method = QComboBox()
        self.payment_method.addItems(["Cash", "Bank Transfer", "Card", "Check", "Mobile Payment"])
        form_layout.addRow("Payment Method:", self.payment_method)
        
        # Notes
        self.payment_notes = QTextEdit()
        self.payment_notes.setMaximumHeight(80)
        self.payment_notes.setPlaceholderText("Optional payment notes...")
        form_layout.addRow("Notes:", self.payment_notes)
        
        layout.addLayout(form_layout)
        
        # Quick payment buttons
        quick_payment_layout = QHBoxLayout()
        quick_payment_layout.addWidget(QLabel("Quick amounts:"))
        
        # Add quick payment buttons for common amounts
        half_amount = balance_due / 2
        quarter_amount = balance_due / 4
        
        for amount, label in [(quarter_amount, "25%"), (half_amount, "50%"), (balance_due, "Full")]:
            btn = QPushButton(f"{label}")
            btn.clicked.connect(lambda checked, amt=amount: self.payment_amount.setValue(amt))
            btn.setStyleSheet("font-size: 12px; padding: 5px 10px;")
            quick_payment_layout.addWidget(btn)
        
        layout.addLayout(quick_payment_layout)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.process_payment)
        button_box.rejected.connect(self.reject)
        button_box.setStyleSheet("""
            QDialogButtonBox QPushButton {
                min-width: 80px;
                padding: 8px 16px;
            }
        """)
        layout.addWidget(button_box)
        
    def process_payment(self):
        """Process the payment and update database"""
        try:
            payment_amount = self.payment_amount.value()
            payment_method = self.payment_method.currentText()
            notes = self.payment_notes.toPlainText().strip()
            
            if payment_amount <= 0:
                QMessageBox.warning(self, "Invalid Amount", "Payment amount must be greater than 0")
                return
            
            balance_due = self.customer_data.get('balance_due', 0)
            if payment_amount > balance_due:
                QMessageBox.warning(self, "Invalid Amount", 
                                  f"Payment amount cannot exceed outstanding balance of PKR {balance_due:,.2f}")
                return
            
            # Get the sale ID for this customer's outstanding balance
            sale_id = self.customer_data.get('sale_id')
            if not sale_id:
                QMessageBox.critical(self, "Error", "Could not find associated sale record")
                return
            
            # Process payment in database
            success, message = self.db_manager.process_partial_payment(
                sale_id=sale_id,
                payment_amount=payment_amount,
                payment_method=payment_method.lower().replace(' ', '_'),
                notes=notes
            )
            
            if success:
                QMessageBox.information(self, "Payment Processed", 
                                      f"Payment of PKR {payment_amount:,.2f} has been processed successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Payment Failed", f"Failed to process payment: {message}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while processing payment: {str(e)}")