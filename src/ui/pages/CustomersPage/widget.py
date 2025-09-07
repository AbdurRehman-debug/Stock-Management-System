from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel, 
                             QPushButton, QFrame, QScrollArea, QHBoxLayout, 
                             QMessageBox, QLineEdit, QComboBox, QGridLayout,QDialog,
                             QProgressBar)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont
from ....database.database_manager import DatabaseManager
from .outstanding_payments import PaymentDialog
import datetime


class CustomersPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.setup_ui()
        self.load_customers()
        self.setup_auto_refresh()
        
    def setup_ui(self):
        """Setup the main customers page UI"""
        self.setWindowTitle("Customers Management")
        
        # Set main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header section
        self.setup_header(layout)
        
        # Search and filter section
        self.setup_search_filter(layout)
        
        # Customers scroll area
        self.setup_customers_area(layout)
        
        # Summary section
        self.setup_summary_section(layout)
        
    def setup_header(self, parent_layout):
        """Setup header with title"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Title
        title = QLabel("Customer Management")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: white;
            }
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        parent_layout.addWidget(header_frame)
        
    def setup_search_filter(self, parent_layout):
        """Setup search and filter controls"""
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 10px;
                padding: 15px;
            }
            QLineEdit, QComboBox {
                background-color: #34495e;
                border: 2px solid #7f8c8d;
                border-radius: 6px;
                padding: 8px 12px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setSpacing(15)
        
        # Search box
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or phone...")
        self.search_input.textChanged.connect(self.filter_customers)
        
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input, 2)
        
        # Status filter
        status_label = QLabel("Status:")
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All Customers", "Paid in Full", "Partial Payment", "Payment Pending"])
        self.status_filter.currentTextChanged.connect(self.filter_customers)
        
        filter_layout.addWidget(status_label)
        filter_layout.addWidget(self.status_filter, 1)
        
        # Customer type filter
        type_label = QLabel("Type:")
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Types", "Walk-in Customer", "Regular Customer", "Shop Owner", "Wholesale Buyer"])
        self.type_filter.currentTextChanged.connect(self.filter_customers)
        
        filter_layout.addWidget(type_label)
        filter_layout.addWidget(self.type_filter, 1)
        
        parent_layout.addWidget(filter_frame)
        
    def setup_customers_area(self, parent_layout):
        """Setup scrollable area for customer cards"""
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: 2px solid #34495e;
                border-radius: 12px;
                background-color: #ecf0f1;
            }
            QScrollBar:vertical {
                background-color: #d5dbdb;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #85929e;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #5d6d7e;
            }
        """)
        
        # Container widget for customer cards
        self.customers_container = QWidget()
        self.customers_layout = QGridLayout(self.customers_container)
        self.customers_layout.setContentsMargins(20, 20, 20, 20)
        self.customers_layout.setSpacing(50)
        self.customers_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_area.setWidget(self.customers_container)
        parent_layout.addWidget(self.scroll_area, 1)
        
    def setup_summary_section(self, parent_layout):
        """Setup summary statistics at bottom"""
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 12px;
                padding: 15px;
            }
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        summary_layout = QHBoxLayout(summary_frame)
        summary_layout.setSpacing(30)
        
        # Summary labels
        self.total_customers_label = QLabel("Total Customers: 0")
        self.paid_customers_label = QLabel("Paid in Full: 0")
        self.pending_customers_label = QLabel("Payment Pending: 0")
        self.total_outstanding_label = QLabel("Total Outstanding: PKR 0.00")
        
        # Style important numbers
        self.total_outstanding_label.setStyleSheet("color: #e74c3c; font-size: 16px; font-weight: bold;")
        
        summary_layout.addWidget(self.total_customers_label)
        summary_layout.addWidget(self.paid_customers_label)
        summary_layout.addWidget(self.pending_customers_label)
        summary_layout.addStretch()
        summary_layout.addWidget(self.total_outstanding_label)
        
        parent_layout.addWidget(summary_frame)
        
    def setup_auto_refresh(self):
        """Setup automatic refresh timer"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(3000)  # Refresh every 8 seconds

    def refresh_data(self):
        """Refresh data while preserving current filters"""
        self.load_customers()
        # Reapply current filters after loading
        self.filter_customers()

    def load_customers(self):
        """Load all customers from database and create cards"""
        # Clear existing cards
        for i in reversed(range(self.customers_layout.count())):
            child = self.customers_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Get customers data with their payment status
        customers_data = self.db_manager.get_customers_with_payment_status()
        
        if not customers_data:
            self.show_empty_state()
        else:
            # Create customer cards in grid layout
            row = 0
            col = 0
            max_cols = 3  # 3 cards per row
            
            for customer_data in customers_data:
                customer_card = CustomerCard(customer_data, self)
                self.customers_layout.addWidget(customer_card, row, col)
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
        
        self.update_summary_statistics(customers_data)
        
    def show_empty_state(self):
        """Show empty state when no customers"""
        empty_widget = QWidget()
        empty_layout = QVBoxLayout(empty_widget)
        empty_layout.setAlignment(Qt.AlignCenter)
        
        empty_text = QLabel("No customers yet")
        empty_text.setAlignment(Qt.AlignCenter)
        empty_text.setStyleSheet("color: #7f8c8d; font-size: 20px; font-weight: bold;")
        
        empty_subtext = QLabel("Customers will appear here after completing sales")
        empty_subtext.setAlignment(Qt.AlignCenter)
        empty_subtext.setStyleSheet("color: #95a5a6; font-size: 14px;")
        
        empty_layout.addWidget(empty_text)
        empty_layout.addWidget(empty_subtext)
        
        self.customers_layout.addWidget(empty_widget, 0, 0, 1, 3)
        
    def filter_customers(self):
        """Filter customers based on search and filter criteria"""
        search_text = self.search_input.text().lower()
        status_filter = self.status_filter.currentText()
        type_filter = self.type_filter.currentText()
        
        # Hide/show customer cards based on filters
        for i in range(self.customers_layout.count()):
            item = self.customers_layout.itemAt(i)
            if item and isinstance(item.widget(), CustomerCard):
                card = item.widget()
                
                should_show = True
                
                # Search filter
                if search_text:
                    customer_name = card.customer_data.get('name', '').lower()
                    customer_phone = card.customer_data.get('phone', '').lower()
                    if search_text not in customer_name and search_text not in customer_phone:
                        should_show = False
                
                # Status filter
                if status_filter != "All Customers" and should_show:
                    card_status = card.customer_data.get('payment_status')
                    if status_filter == "Paid in Full" and card_status != "paid_full":
                        should_show = False
                    elif status_filter == "Partial Payment" and card_status != "partial":
                        should_show = False
                    elif status_filter == "Payment Pending" and card_status != "pending":
                        should_show = False
                
                # Type filter
                if type_filter != "All Types" and should_show:
                    card_type = card.customer_data.get('customer_type', '').replace('_', ' ').title()
                    if type_filter not in card_type:
                        should_show = False
                
                card.setVisible(should_show)
    
    def update_summary_statistics(self, customers_data):
        """Update summary statistics"""
        if not customers_data:
            self.total_customers_label.setText("Total Customers: 0")
            self.paid_customers_label.setText("Paid in Full: 0")
            self.pending_customers_label.setText("Payment Pending: 0")
            self.total_outstanding_label.setText("Total Outstanding: PKR 0.00")
            return
            
        total_customers = len(set(c['id'] for c in customers_data))  # Unique customers
        paid_customers = len(set(c['id'] for c in customers_data if c['payment_status'] == 'paid_full'))
        pending_customers = len(set(c['id'] for c in customers_data if c['payment_status'] in ['pending', 'partial']))
        total_outstanding = sum(c['balance_due'] for c in customers_data)
        
        self.total_customers_label.setText(f"Total Customers: {total_customers}")
        self.paid_customers_label.setText(f"Paid in Full: {paid_customers}")
        self.pending_customers_label.setText(f"Payment Pending: {pending_customers}")
        self.total_outstanding_label.setText(f"Total Outstanding: PKR {total_outstanding:,.2f}")


class CustomerCard(QFrame):
    """Individual customer card widget"""
    
    def __init__(self, customer_data, parent=None):
        super().__init__(parent)
        self.parent_page = parent
        self.db_manager = DatabaseManager()
        self.customer_data = customer_data
        self.setup_ui()
        
    def setup_ui(self):
        """Setup customer card UI"""
        self.setFixedSize(400, 500)
        self.setFrameShape(QFrame.StyledPanel)
        
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Customer name and type and id
        name_layout = QHBoxLayout()
        id_label = QLabel(f"ID: {self.customer_data.get('id')}")
        id_label.setStyleSheet("font-size: 12px; color: white;")
        name_label = QLabel(self.customer_data.get("name", "guest"))
        name_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        name_layout.addWidget(id_label)
        name_layout.addWidget(name_label)

        # Status indicator
        status_indicator = self.create_status_indicator()
        name_layout.addStretch()
        name_layout.addWidget(status_indicator)

        layout.addLayout(name_layout)
        
        # Phone number
        phone_label = QLabel(f"Phone: {self.customer_data.get('phone') or 'Not provided'}")
        phone_label.setStyleSheet("font-size: 12px; color: white;")
        layout.addWidget(phone_label)
        
        # Customer type
        type_label = QLabel(f"Type: {self.customer_data.get('customer_type', '').replace('_', ' ').title()}")
        type_label.setStyleSheet("font-size: 12px; color: white;")
        layout.addWidget(type_label)
        
        # Payment summary
        total_purchased = QLabel(f"Total Purchased: PKR {self.customer_data.get('total_amount', 0):,.2f}")
        total_purchased.setStyleSheet("font-size: 14px; font-weight: bold; color: #e74c3c;")
        total_paid = QLabel(f"Total Paid: PKR {self.customer_data.get('amount_paid', 0):,.2f}")
        total_paid.setStyleSheet("font-size: 14px; font-weight: bold; color: #27ae60;")

        # Purchased items
        purchased_title = QLabel("Items Purchased:")
        purchased_title.setStyleSheet("font-size: 12px; font-weight: bold; color: white;")
        layout.addWidget(purchased_title)
        purchased_items = self.customer_data.get("items_purchased", [])
        for item in purchased_items:
            item_label = QLabel(f" - {item[0]} (Category: {item[1]}, Price: PKR {item[2]:,.2f}, Quantity: {item[3]})")
            item_label.setStyleSheet("font-size: 12px; color: white;")
            layout.addWidget(item_label)

        layout.addWidget(total_purchased)
        layout.addWidget(total_paid)

        # Sale date
        sale_date = self.customer_data.get('created_at')
        sale_date_label = QLabel(f"First Purchase: {sale_date.split(' ')[0] if sale_date else 'N/A'}")
        sale_date_label.setStyleSheet("font-size: 10px; color: #bdc3c7;")
        layout.addWidget(sale_date_label)

        # Progress bar for payment completion
        total_amount = self.customer_data.get('total_amount', 0)
        amount_paid = self.customer_data.get('amount_paid', 0)
        if total_amount > 0:
            progress = QProgressBar()
            progress.setRange(0, 100)
            progress.setValue(int((amount_paid / total_amount) * 100))
            progress.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #bdc3c7;
                    border-radius: 4px;
                    text-align: center;
                    font-size: 10px;
                    height: 16px;
                }
                QProgressBar::chunk {
                    background-color: #27ae60;
                    border-radius: 3px;
                }
            """)
            layout.addWidget(progress)

        # Due date
        due_date = self.customer_data.get('due_date')
        if due_date:
            try:
                due_date_obj = datetime.datetime.fromisoformat(due_date)
                due_date_text = due_date_obj.strftime("%B %d, %Y")
            except:
                due_date_text = "Unknown"
            due_date_label = QLabel(f"Due Date: {due_date_text}")
        else:
            due_date_label = QLabel("Due Date: N/A")
        due_date_label.setStyleSheet("font-size: 10px; color: #7f8c8d;")
        layout.addWidget(due_date_label)
        
        layout.addStretch()
        
        # Balance due
        balance_due = self.customer_data.get('balance_due', 0)
        balance_due_label = QLabel(f"Balance Due: PKR {balance_due:,.2f}")
        balance_due_label.setStyleSheet("font-size: 12px; color: #e74c3c; font-weight: bold;")
        layout.addWidget(balance_due_label)


        #implenting duncality if balance due is greater than 0
        if balance_due > 0:
            reminder_label = QLabel("⚠️ Payment Pending")
            reminder_label.setStyleSheet("font-size: 12px; color: #e74c3c; font-weight: bold;")
            layout.addWidget(reminder_label)
            #add a button if ther user wants to complete the payment
            pay_button = QPushButton("Complete Payment")
            layout.addWidget(pay_button)
            pay_button.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    
                }
                QPushButton:hover {
                    background-color: #2ecc71;
                }
            """)
            pay_button.clicked.connect(self.open_payment_dialog)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        print_pdf = QPushButton("Print Receipt")
        print_pdf.clicked.connect(self.print_receipt)
        button_layout.addWidget(print_pdf)

        layout.addLayout(button_layout)
        
    def create_status_indicator(self):
        """Create status indicator badge"""
        indicator = QLabel()
        indicator.setFixedSize(20, 20)
        indicator.setAlignment(Qt.AlignCenter)

        payment_status = self.customer_data.get('payment_status')
        due_date = self.customer_data.get('due_date')
        
        if payment_status == 'paid_full':
            indicator.setText("✓")
            indicator.setStyleSheet("background-color: #27ae60; color: white; border-radius: 10px; font-weight: bold;")
        elif payment_status == 'pending':
            indicator.setText("!")
            indicator.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 10px; font-weight: bold;")
        elif payment_status == 'partial':
            indicator.setText("~")
            indicator.setStyleSheet("background-color: #f39c12; color: white; border-radius: 10px; font-weight: bold;")
        else:
            indicator.setText("?")
            indicator.setStyleSheet("background-color: #7f8c8d; color: white; border-radius: 10px; font-weight: bold;")

        return indicator

    def print_receipt(self):
        """Print the receipt for the customer"""
        QMessageBox.information(self, "Print Receipt", 
                              f"Receipt printing for customer {self.customer_data.get('name')} is not implemented yet.")

    def open_payment_dialog(self):
        """Open payment dialog for processing partial payments"""
        dialog = PaymentDialog(self.customer_data, self)
        if dialog.exec() == QDialog.Accepted:
            # Refresh the customers page to show updated data
            if self.parent_page:
                self.parent_page.load_customers()
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = CustomersPage()
    window.show()
    sys.exit(app.exec())