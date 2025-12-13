from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QComboBox, QTextEdit, 
                             QDateEdit, QGroupBox, QFormLayout, QMessageBox,
                             QCheckBox, QSpinBox, QDoubleSpinBox, QFrame,
                             QScrollArea, QWidget)
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QFont
import datetime

class CheckoutDialog(QDialog):
    """Enhanced checkout dialog with payment tracking and discount - SPACIOUS VERSION"""
    
    checkout_completed = Signal(dict)
    
    def __init__(self, cart_items, total_amount, parent=None):
        super().__init__(parent)
        self.cart_items = cart_items
        print(self.cart_items)
        self.original_total = total_amount  # Store original total
        self.total_amount = total_amount
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the checkout dialog UI with improved spacing and scroll area"""
        self.setWindowTitle("Checkout")
        self.resize(900, 900)

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
            QCheckBox {
                color: #ecf0f1;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #7f8c8d;
                border-radius: 4px;
                background-color: #2c3e50;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border: 2px solid #3498db;
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
        main_layout.setSpacing(0)

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background-color: transparent; }")

        # Create a container widget for all content inside scroll area
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(20)

        # Add all sections to container layout
        self.setup_order_summary(container_layout)
        self.setup_discount_section(container_layout)
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
        summary_layout.setSpacing(12)
        summary_layout.setContentsMargins(20, 25, 20, 20)
        summary_group.setFixedHeight(300)  # Fixed height to prevent stretching
        
        # Total items
        items_count = sum(item[1] for item in self.cart_items)
        items_label = QLabel(f"Total Items: {items_count}")
        items_label.setStyleSheet("font-size: 16px; color: #ecf0f1; padding: 5px;")
        summary_layout.addWidget(items_label)
        
        # Original amount label
        self.original_amount_label = QLabel(f"Original Amount: PKR {self.original_total:,.2f}")
        self.original_amount_label.setStyleSheet("""
            font-size: 15px; 
            color: #95a5a6; 
            padding: 5px;
        """)
        self.original_amount_label.hide()  # Hidden by default
        summary_layout.addWidget(self.original_amount_label)
        
        # Discount label
        self.discount_amount_label = QLabel("Discount: PKR 0.00")
        self.discount_amount_label.setStyleSheet("""
            font-size: 15px; 
            color: #e67e22; 
            padding: 5px;
        """)
        self.discount_amount_label.hide()  # Hidden by default
        summary_layout.addWidget(self.discount_amount_label)
        
        # Total amount - make it prominent
        self.total_label = QLabel(f"Total Amount: PKR {self.total_amount:,.2f}")
        self.total_label.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #f39c12; 
            padding: 8px; 
            border: 2px solid #f39c12; 
            border-radius: 8px;
            background-color: rgba(243, 156, 18, 0.1);
        """)
        self.total_label.setAlignment(Qt.AlignCenter)
        summary_layout.addWidget(self.total_label)
        
        # Add stretch to push content to top
        summary_layout.addStretch()
        
        parent_layout.addWidget(summary_group)
    
    def setup_discount_section(self, parent_layout):
        """Setup discount section"""
        discount_group = QGroupBox("💰 Discount")
        discount_layout = QFormLayout(discount_group)
        discount_layout.setSpacing(15)
        discount_layout.setContentsMargins(20, 25, 20, 20)
        discount_group.setMinimumHeight(250)
        
        # Discount checkbox
        self.discount_checkbox = QCheckBox("Apply Discount")
        self.discount_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 16px;
                font-weight: bold;
                color: #3498db;
                padding: 8px;
            }
        """)
        discount_layout.addRow("", self.discount_checkbox)
        
        # Discount input
        self.discount_input = QDoubleSpinBox()
        self.discount_input.setRange(0, 999999.99)
        self.discount_input.setDecimals(2)
        self.discount_input.setValue(0)
        self.discount_input.setSuffix(" PKR")
        self.discount_input.setMinimumHeight(30)
        self.discount_input.setEnabled(False)
        self.discount_input.setStyleSheet("""
            QDoubleSpinBox {
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
            }
            QDoubleSpinBox:disabled {
                background-color: #1a252f;
                color: #7f8c8d;
                border: 2px solid #34495e;
            }
        """)
        discount_layout.addRow("Discount Amount:", self.discount_input)
        
        parent_layout.addWidget(discount_group)
        
    def setup_customer_info(self, parent_layout):
        """Setup customer information section with bigger inputs"""
        customer_group = QGroupBox("👤 Customer Information")
        customer_layout = QFormLayout(customer_group)
        customer_layout.setSpacing(15)
        customer_layout.setContentsMargins(10, 10, 10, 10)
        
        # Sale Date (Manual Entry)
        self.sale_date = QDateEdit()
        self.sale_date.setDate(QDate.currentDate())  # Default to today
        self.sale_date.setMinimumHeight(20)
        self.sale_date.setDisplayFormat("dd-MM-yyyy")
        self.sale_date.setCalendarPopup(True)  # Show calendar popup
        self.sale_date.setStyleSheet("""
            QDateEdit {
                font-size: 15px;
                font-weight: bold;
            }
        """)
        customer_layout.addRow("📅 Sale Date:", self.sale_date)
        
        # Customer name
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name (required for partial payments and credit sales)")
        self.customer_name.setMinimumHeight(20)
        customer_layout.addRow("Customer Name:", self.customer_name)
        
        # Phone number
        self.customer_phone = QLineEdit()
        self.customer_phone.setPlaceholderText("03XX-XXXXXXX")
        self.customer_phone.setMinimumHeight(20)
        customer_layout.addRow("Phone Number:", self.customer_phone)
        
        # Customer type
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
        self.payment_group = QGroupBox("💰 Payment Details")
        payment_layout = QFormLayout(self.payment_group)
        payment_layout.setSpacing(15)
        payment_layout.setContentsMargins(20, 20, 20, 20)
        self.payment_group.setMinimumHeight(400)
        
        # Amount paid
        self.amount_paid = QDoubleSpinBox()
        self.amount_paid.setRange(0, 999999.99)
        self.amount_paid.setDecimals(2)
        self.amount_paid.setValue(self.total_amount)
        self.amount_paid.setSuffix(" PKR")
        self.amount_paid.setMinimumHeight(30)
        self.amount_paid.setStyleSheet("""
            QDoubleSpinBox {
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
            }
        """)
        payment_layout.addRow("Amount Paid:", self.amount_paid)
        
        # Balance due
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
        
        # Payment method
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
        
        # Payment status
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
        
        # Due date
        self.due_date = QDateEdit()
        self.due_date.setDate(QDate.currentDate().addDays(30))
        self.due_date.setMinimumHeight(20)
        self.due_date.setEnabled(False)
        self.due_date.setDisplayFormat("dd-MM-yyyy")
        payment_layout.addRow("Due Date:", self.due_date)
        
        parent_layout.addWidget(self.payment_group)
        
    def setup_notes_section(self, parent_layout):
        """Setup notes section with bigger text area"""
        notes_group = QGroupBox("📝 Additional Notes")
        notes_layout = QVBoxLayout(notes_group)
        notes_layout.setSpacing(10)
        notes_layout.setContentsMargins(20, 25, 20, 20)
        notes_group.setMinimumHeight(300)
        
        self.notes = QTextEdit()
        self.notes.setMinimumHeight(120)
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
        cancel_btn.setFixedSize(150, 50)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        button_layout.addStretch()
        
        # Complete sale button
        complete_btn = QPushButton("Complete Sale")
        complete_btn.setFixedSize(200, 50)
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
        self.discount_checkbox.stateChanged.connect(self.toggle_discount)
        self.discount_input.valueChanged.connect(self.apply_discount)
        
    def toggle_discount(self, state):
        """Toggle discount section and payment details visibility"""
        # State is an integer: 0 = unchecked, 2 = checked
        is_discount = (state == 2)
        
        print(f"Discount checkbox state: {state}, is_discount: {is_discount}")  # Debug
        
        # Enable/disable discount input
        self.discount_input.setEnabled(is_discount)
        self.discount_input.setReadOnly(not is_discount)
        
        # Show/hide payment details section
        self.payment_group.setVisible(not is_discount)
        
        if is_discount:
            # Reset discount input and focus on it
            self.discount_input.setValue(0)
            self.discount_input.setFocus()
            # Show discount info in summary
            self.original_amount_label.show()
            self.discount_amount_label.show()
        else:
            # Hide discount info
            self.original_amount_label.hide()
            self.discount_amount_label.hide()
            # Reset total to original
            self.total_amount = self.original_total
            self.update_total_display()
            self.amount_paid.setValue(self.total_amount)
    
    def apply_discount(self):
        """Apply discount to total amount"""
        discount = self.discount_input.value()
        
        # Validate discount
        if discount > self.original_total:
            QMessageBox.warning(self, "Invalid Discount", 
                              f"Discount cannot exceed the original amount of PKR {self.original_total:,.2f}")
            self.discount_input.setValue(self.original_total)
            return
        
        # Calculate new total
        self.total_amount = self.original_total - discount
        
        # Update displays
        self.discount_amount_label.setText(f"Discount: PKR {discount:,.2f}")
        self.update_total_display()
        
        # Update amount paid to match new total
        if not self.discount_checkbox.isChecked():
            self.amount_paid.setValue(self.total_amount)
    
    def update_total_display(self):
        """Update the total amount display"""
        self.total_label.setText(f"Total Amount: PKR {self.total_amount:,.2f}")
        
    def update_payment_status(self):
        """Update payment status based on amount paid"""
        paid = self.amount_paid.value()
        balance = self.total_amount - paid
        
        # Update balance label
        self.balance_label.setText(f"PKR {balance:,.2f}")
        
        # Update payment status and styling
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
        """Validate form for credit sales"""
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
        """Complete the sale with enhanced validation"""
        is_discount = self.discount_checkbox.isChecked()
        customer_name = self.customer_name.text().strip()
        
        # Get the manually entered sale date
        sale_date_qdate = self.sale_date.date()
        sale_date = datetime.datetime(
            sale_date_qdate.year(),
            sale_date_qdate.month(),
            sale_date_qdate.day(),
            datetime.datetime.now().hour,
            datetime.datetime.now().minute,
            datetime.datetime.now().second
        )
        
        # For discount sales
        if is_discount:
            discount = self.discount_input.value()
            
            if discount <= 0:
                QMessageBox.warning(self, "Validation Error", 
                                  "Please enter a discount amount greater than 0!")
                self.discount_input.setFocus()
                return
            
            # Confirm discount sale
            reply = QMessageBox.question(
                self, "Confirm Discount Sale",
                f"""Please confirm the discount sale:
                
📅 Sale Date: {sale_date_qdate.toString('dd-MM-yyyy')}
👤 Customer: {customer_name or 'Walk-in Customer'}
💰 Original Amount: PKR {self.original_total:,.2f}
🎟️ Discount: PKR {discount:,.2f}
💵 Final Amount: PKR {self.total_amount:,.2f}

Are you sure you want to proceed with this discount?""",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
            
            # Prepare discount sale data
            sale_data = {
                'cart_items': self.cart_items,
                'total_amount': self.total_amount,
                'amount_paid': self.total_amount,  # Full payment with discount
                'balance_due': 0,
                'customer_name': customer_name or 'guest',
                'customer_phone': self.customer_phone.text().strip(),
                'customer_type': self.customer_type.currentText(),
                'payment_method': 'cash',
                'payment_status': 'Paid in Full',
                'due_date': None,
                'notes': self.notes.toPlainText().strip(),
                'sale_date': sale_date,  # Use manual date
                'discount_amount': discount
            }
        else:
            # Regular payment validation
            paid = self.amount_paid.value()
            
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
            
            balance = self.total_amount - paid
            
            # Confirmation for partial payments
            if balance > 0:
                reply = QMessageBox.question(
                    self, "Confirm Partial Payment",
                    f"""Please confirm the partial payment details:
                    
📅 Sale Date: {sale_date_qdate.toString('dd-MM-yyyy')}
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
            
            # Prepare regular sale data
            sale_data = {
                'cart_items': self.cart_items,
                'total_amount': self.total_amount,
                'amount_paid': paid,
                'balance_due': balance,
                'customer_name': customer_name or 'guest',
                'customer_phone': self.customer_phone.text().strip(),
                'customer_type': self.customer_type.currentText(),
                'payment_method': self.payment_method.currentText(),
                'payment_status': self.payment_status.text(),
                'due_date': self.due_date.date().toPython() if balance > 0 else None,
                'notes': self.notes.toPlainText().strip(),
                'sale_date': sale_date,  # Use manual date
                'discount_amount': 0
            }
        
        print("Sale Data:", sale_data)
        
        # Emit signal and close
        self.checkout_completed.emit(sale_data)
        self.accept()