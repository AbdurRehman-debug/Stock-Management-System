from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QComboBox, QTextEdit, 
                             QDateEdit, QGroupBox, QFormLayout, QMessageBox,
                             QCheckBox, QSpinBox, QDoubleSpinBox, QFrame,
                             QScrollArea, QWidget)
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QFont
import datetime

class CheckoutDialog(QDialog):
    """Enhanced checkout dialog with payment tracking - SPACIOUS VERSION"""
    
    checkout_completed = Signal(dict)
    
    def __init__(self, cart_items, total_amount, parent=None):
        super().__init__(parent)
        self.cart_items = cart_items
        print(self.cart_items)
        self.total_amount = total_amount
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the checkout dialog UI with improved spacing and scroll area"""
        self.setWindowTitle("Checkout")
        self.resize(900, 900)  # Allow resizing, better with scroll area

        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                color: white;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #34495e;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 20px;
                background-color: #34495e;
            }
            QGroupBox::title {
                color: #3498db;
                padding: 0 15px;
                font-size: 16px;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
                padding: 2px;
            }
            QLineEdit, QComboBox, QTextEdit, QDateEdit, QDoubleSpinBox {
                background-color: #2c3e50;
                border: 2px solid #7f8c8d;
                border-radius: 8px;
                padding: 12px 15px;
                color: white;
                font-size: 14px;
                min-height: 15px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QDoubleSpinBox:focus {
                border: 3px solid #3498db;
                background-color: #34495e;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #7f8c8d;
                background-color: #7f8c8d;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 25px;
                font-weight: bold;
                font-size: 15px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton#cancel_btn {
                background-color: #e74c3c;
            }
            QPushButton#cancel_btn:hover {
                background-color: #c0392b;
            }
        """)

        # Create main layout for the dialog
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)  # No spacing here, spacing inside scroll area content

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background-color: transparent; }")

        # Create a container widget for all content inside scroll area
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(20)  # Spacing between sections

        # Add all sections to container layout
        self.setup_order_summary(container_layout)
        self.setup_customer_info(container_layout)
        self.setup_payment_details(container_layout)
        self.setup_notes_section(container_layout)
        self.setup_action_buttons(container_layout)

        # Set container as the scroll area's widget
        scroll_area.setWidget(container)

        # Add scroll area to the main layout
        main_layout.addWidget(scroll_area)
        
    def setup_order_summary(self, parent_layout):
        """Setup order summary section with better spacing"""
        summary_group = QGroupBox("📱 Order Summary")
        summary_layout = QVBoxLayout(summary_group)
        summary_layout.setSpacing(15)
        summary_layout.setContentsMargins(20, 25, 20, 20)
        summary_group.setMinimumHeight(200)
        
        # Total items and amount with better formatting
        items_count = sum(item[1] for item in self.cart_items)
        
        # Items count
        items_label = QLabel(f"Total Items: {items_count}")
        items_label.setStyleSheet("font-size: 16px; color: #ecf0f1; padding: 8px;")
        summary_layout.addWidget(items_label)
        
        # Total amount - make it prominent
        total_label = QLabel(f"Total Amount: PKR {self.total_amount:,.2f}")
        total_label.setStyleSheet("""
            font-size: 22px; 
            font-weight: bold; 
            color: #f39c12; 
            padding: 10px; 
            border: 2px solid #f39c12; 
            border-radius: 8px;
            background-color: rgba(243, 156, 18, 0.1);
        """)
        total_label.setAlignment(Qt.AlignCenter)
        summary_layout.addWidget(total_label)
        
        parent_layout.addWidget(summary_group)
        
    def setup_customer_info(self, parent_layout):
        """Setup customer information section with bigger inputs"""
        customer_group = QGroupBox("👤 Customer Information")
        customer_layout = QFormLayout(customer_group)
        customer_layout.setSpacing(15)  # More space between rows
        customer_layout.setContentsMargins(10, 10, 10, 10)
        
        # Customer name (bigger input)
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name (required for partial payments and credit sales)")
        self.customer_name.setMinimumHeight(20)  # Bigger input
        customer_layout.addRow("Customer Name:", self.customer_name)
        
        # Phone number (bigger input)
        self.customer_phone = QLineEdit()
        self.customer_phone.setPlaceholderText("03XX-XXXXXXX")
        self.customer_phone.setMinimumHeight(20)
        customer_layout.addRow("Phone Number:", self.customer_phone)
        
        # Customer type (bigger dropdown)
        self.customer_type = QComboBox()
        self.customer_type.setMinimumHeight(20)
        self.customer_type.addItems([
            "Walk-in Customer", 
            "Regular Customer", 
            "Shop Owner/Retailer",
            "Wholesale Buyer"
        ])
        customer_layout.addRow("Customer Type:", self.customer_type)
        
        parent_layout.addWidget(customer_group)
        
    def setup_payment_details(self, parent_layout):
        """Setup payment details section with bigger inputs"""
        payment_group = QGroupBox("💰 Payment Details")
        payment_layout = QFormLayout(payment_group)
        payment_layout.setSpacing(15)
        payment_layout.setContentsMargins(20, 20, 20, 20)
        payment_group.setMinimumHeight(400)
        
        # Amount paid (much bigger input)
        self.amount_paid = QDoubleSpinBox()
        self.amount_paid.setRange(0, 999999.99)
        self.amount_paid.setDecimals(2)
        self.amount_paid.setValue(self.total_amount)
        self.amount_paid.setSuffix(" PKR")
        self.amount_paid.setMinimumHeight(30)  # Much bigger
        self.amount_paid.setStyleSheet("""
            QDoubleSpinBox {
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
            }
        """)
        payment_layout.addRow("Amount Paid:", self.amount_paid)
        
        # Balance due (prominent display)
        self.balance_label = QLabel("PKR 0.00")
        self.balance_label.setStyleSheet("""
            font-weight: bold; 
            color: #e74c3c; 
            font-size: 14px;
            padding: 10px;
            border: 1px solid #e74c3c;
            border-radius: 6px;
            background-color: rgba(231, 76, 60, 0.1);
        """)
        self.balance_label.setMinimumHeight(10)
        self.balance_label.setAlignment(Qt.AlignCenter)
        payment_layout.addRow("Balance Due:", self.balance_label)
        
        # Payment method (bigger dropdown)
        self.payment_method = QComboBox()
        self.payment_method.setMinimumHeight(20)
        self.payment_method.addItems([
            "Cash", 
            "Bank Transfer", 
            "Mobile Banking (JazzCash/EasyPaisa)",
            "Credit Card",
            "Cheque"
        ])
        payment_layout.addRow("Payment Method:", self.payment_method)
        
        # Payment status (prominent display)
        self.payment_status = QLabel("Paid in Full")
        self.payment_status.setStyleSheet("""
            font-weight: bold; 
            color: #27ae60; 
            font-size: 14px;
            padding: 10px;
            border: 1px solid #27ae60;
            border-radius: 6px;
            background-color: rgba(39, 174, 96, 0.1);
        """)
        self.payment_status.setMinimumHeight(10)
        self.payment_status.setAlignment(Qt.AlignCenter)
        payment_layout.addRow("Payment Status:", self.payment_status)
        
        # Due date (bigger date picker)
        self.due_date = QDateEdit()
        self.due_date.setDate(QDate.currentDate().addDays(30))
        self.due_date.setMinimumHeight(20)
        self.due_date.setEnabled(False)
        self.due_date.setDisplayFormat("dd-MM-yyyy")
        payment_layout.addRow("Due Date:", self.due_date)
        
        parent_layout.addWidget(payment_group)
        
    def setup_notes_section(self, parent_layout):
        """Setup notes section with bigger text area"""
        notes_group = QGroupBox("📝 Additional Notes")
        notes_layout = QVBoxLayout(notes_group)
        notes_layout.setSpacing(10)
        notes_layout.setContentsMargins(20, 25, 20, 20)
        notes_group.setMinimumHeight(300)
        
        self.notes = QTextEdit()
        self.notes.setMinimumHeight(120)  # Much bigger text area
        self.notes.setPlaceholderText("Any special instructions, payment agreements, or notes about this sale...")
        self.notes.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                padding: 15px;
                line-height: 1.4;
            }
        """)
        notes_layout.addWidget(self.notes)
        
        parent_layout.addWidget(notes_group)
        
    def setup_action_buttons(self, parent_layout):
        """Setup action buttons with better spacing"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(20, 20, 20, 0)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancel_btn")
        cancel_btn.setFixedSize(150, 50)  # Bigger buttons
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        button_layout.addStretch()
        
        # Complete sale button
        complete_btn = QPushButton("Complete Sale")
        complete_btn.setFixedSize(200, 50)  # Even bigger
        complete_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
                
            }
        """)
        complete_btn.clicked.connect(self.complete_sale)
        button_layout.addWidget(complete_btn)
        
        parent_layout.addLayout(button_layout)
        
    def setup_connections(self):
        """Setup signal connections"""
        self.amount_paid.valueChanged.connect(self.update_payment_status)
        self.customer_name.textChanged.connect(self.validate_form)
        
    def update_payment_status(self):
        """Update payment status based on amount paid with better visual feedback"""
        paid = self.amount_paid.value()
        balance = self.total_amount - paid
        
        # Update balance label
        self.balance_label.setText(f"PKR {balance:,.2f}")
        
        # Update payment status and styling with better colors
        if balance <= 0:
            status = "Paid in Full"
            color = "#27ae60"
            bg_color = "rgba(39, 174, 96, 0.1)"
            border_color = "#27ae60"
            self.due_date.setEnabled(False)
            if balance < 0:
                status = f"Overpaid (Change: PKR {abs(balance):,.2f})"
                color = "#f39c12"
                bg_color = "rgba(243, 156, 18, 0.1)"
                border_color = "#f39c12"
        elif paid == 0:
            status = "Payment Pending"
            color = "#e74c3c"
            bg_color = "rgba(231, 76, 60, 0.1)"
            border_color = "#e74c3c"
            self.due_date.setEnabled(True)
        else:
            status = "Partial Payment"
            color = "#f39c12"
            bg_color = "rgba(243, 156, 18, 0.1)"
            border_color = "#f39c12"
            self.due_date.setEnabled(True)
            
        self.payment_status.setText(status)
        self.payment_status.setStyleSheet(f"""
            font-weight: bold; 
            color: {color}; 
            font-size: 16px;
            padding: 10px;
            border: 1px solid {border_color};
            border-radius: 6px;
            background-color: {bg_color};
        """)
        
        # Update balance label color
        if balance <= 0:
            balance_color = "#27ae60"
            balance_bg = "rgba(39, 174, 96, 0.1)"
            balance_border = "#27ae60"
        else:
            balance_color = "#e74c3c"
            balance_bg = "rgba(231, 76, 60, 0.1)"
            balance_border = "#e74c3c"
            
        self.balance_label.setStyleSheet(f"""
            font-weight: bold; 
            color: {balance_color}; 
            font-size: 18px;
            padding: 10px;
            border: 1px solid {balance_border};
            border-radius: 6px;
            background-color: {balance_bg};
        """)
        
    def validate_form(self):
        """Validate form for credit sales with better visual feedback"""
        paid = self.amount_paid.value()
        if paid < self.total_amount and not self.customer_name.text().strip():
            self.customer_name.setStyleSheet("""
                QLineEdit {
                    background-color: #2c3e50;
                    border: 3px solid #e74c3c;
                    border-radius: 8px;
                    padding: 12px 15px;
                    color: white;
                    font-size: 14px;
                }
            """)
        else:
            self.customer_name.setStyleSheet("")
            
    def complete_sale(self):
        """Complete the sale with enhanced validation and confirmation"""
        paid = self.amount_paid.value()
        customer_name = self.customer_name.text().strip()
        
        # Validation
        if paid < self.total_amount and not customer_name:
            QMessageBox.warning(self, "Validation Error", 
                              "Customer name is required for partial payments or credit sales!\n\nPlease enter the customer's name before proceeding.")
            self.customer_name.setFocus()
            return
            
        if paid < 0:
            QMessageBox.warning(self, "Validation Error", 
                              "Amount paid cannot be negative!")
            self.amount_paid.setFocus()
            return
            
        # Enhanced confirmation for partial payments
        balance = self.total_amount - paid
        if balance > 0:
            reply = QMessageBox.question(
                self, "Confirm Partial Payment",
                f"""Please confirm the partial payment details:
                
👤 Customer: {customer_name}
💰 Total Amount: PKR {self.total_amount:,.2f}
💵 Amount Paid: PKR {paid:,.2f}
⚠️  Balance Due: PKR {balance:,.2f}
📅 Due Date: {self.due_date.date().toString('dd-MM-yyyy')}
💳 Payment Method: {self.payment_method.currentText()}

Are you sure you want to proceed with this partial payment?""",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
                
        # Prepare sale data
        sale_data = {
            'cart_items': self.cart_items,
            'total_amount': self.total_amount,
            'amount_paid': paid,
            'balance_due': balance,
            'customer_name': customer_name,
            'customer_phone': self.customer_phone.text().strip(),
            'customer_type': self.customer_type.currentText(),
            'payment_method': self.payment_method.currentText(),
            'payment_status': self.payment_status.text(),
            'due_date': self.due_date.date().toPython() if balance > 0 else None,
            'notes': self.notes.toPlainText().strip(),
            'sale_date': datetime.datetime.now()
        }
        print("Sale Data:", sale_data)
        
        # Emit signal and close
        self.checkout_completed.emit(sale_data)
        self.accept()
