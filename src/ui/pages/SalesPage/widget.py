from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFrame, QScrollArea, QHBoxLayout, QMessageBox, QComboBox,QGroupBox
from PySide6.QtCore import Qt, QTimer, Signal
from ....ui.components.cartitem import CartItemWidget
from .SalesPage_ui import Ui_MainWindow
from ....database.database_manager import DatabaseManager


class SalesPage(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Access the vertical layout from the UI
        self.page_layout = self.verticalLayout  

        # Create CartManager widget
        self.cart_manager = CartManager(self)

        # Add CartManager widget to SalesPage's vertical layout
        self.page_layout.addWidget(self.cart_manager)
        
    def showEvent(self, event):
        """Called whenever this page becomes visible"""
        super().showEvent(event)
        # Refresh cart when page is shown
        if hasattr(self, 'cart_manager'):
            self.cart_manager.refresh_cart()


class CartManager(QWidget):
    """Main cart management widget with real-time updates"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = DatabaseManager()
        self.setup_ui()
        self.setup_auto_refresh()
        self.refresh_cart()
        
    def setup_auto_refresh(self):
        """Setup automatic refresh timer"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.check_for_updates)
        self.refresh_timer.start(2000)  # Check every 2 seconds
        self.last_cart_count = 0
        
    def check_for_updates(self):
        """Check if cart has been updated from other pages"""
        cart_items = self.db_manager.get_cart_items()
        current_count = len(cart_items) if cart_items else 0
        
        # If cart count changed, refresh the display
        if current_count != self.last_cart_count:
            self.refresh_cart()
            self.last_cart_count = current_count
        
    def setup_ui(self):
        """Setup the main cart UI with improved centering"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header section with better alignment
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
                padding: 10px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title - centered
        title = QLabel("Shopping Cart")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: white;
                padding: 15px;
                
            }
        """)

        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title, 1)  # Give it stretch

        # Clear cart button - aligned right
        self.clear_btn = QPushButton("Clear Cart")
        self.clear_btn.setFixedSize(120, 40)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_cart)
        header_layout.addWidget(self.clear_btn, 0, Qt.AlignRight)
        
        main_layout.addWidget(header_frame)
        
        # Scroll area for cart items with better styling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 2px solid #bdc3c7;
                border-radius: 12px;
                background-color: #ecf0f1;
                padding: 5px;
            }
            QScrollBar:vertical {
                background-color: #d5dbdb;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #85929e;
                border-radius: 6px;
                min-height: 400px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #5d6d7e;
            }
        """)
        
        # Cart items container with centering
        self.cart_container = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_container)
        self.cart_layout.setContentsMargins(15, 15, 15, 15)
        self.cart_layout.setSpacing(10)
        self.cart_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # Center horizontally
        
        scroll_area.setWidget(self.cart_container)
        main_layout.addWidget(scroll_area, 1)  # Takes most space
        
        # Cart summary section with better styling
        self.setup_summary_section()
        main_layout.addWidget(self.summary_frame)
        
    def setup_summary_section(self):
        """Setup cart summary section with centered layout"""
        self.summary_frame = QFrame()
        self.summary_frame.setFrameShape(QFrame.StyledPanel)
        self.summary_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 12px;
                padding: 20px;
                margin: 10px;
            }
            QLabel {
                color: white;
                font-size: 15px;
            }
            QPushButton {
                background-color: #27ae60;
                color: white;
                border-radius: 8px;
                padding: 15px 30px;
                font-weight: bold;
                font-size: 16px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:disabled {
                background-color: #7f8c8d;
            }
        """)
        
        summary_layout = QVBoxLayout(self.summary_frame)
        summary_layout.setSpacing(15)
        
        # Summary info - centered
        summary_info_layout = QHBoxLayout()
        summary_info_layout.setContentsMargins(10, 0, 10, 0)
        
        self.total_items_label = QLabel("Items: 0")
        self.total_items_label.setStyleSheet("font-weight: bold; color: #ecf0f1; font-size: 16px;")
        self.total_items_label.setAlignment(Qt.AlignLeft)
        summary_info_layout.addWidget(self.total_items_label)
        
        summary_info_layout.addStretch()  # Push total to right
        
        self.total_amount_label = QLabel("Total: PKR 0.00")
        self.total_amount_label.setStyleSheet("font-weight: bold; color: #f39c12; font-size: 20px;")
        self.total_amount_label.setAlignment(Qt.AlignRight)
        summary_info_layout.addWidget(self.total_amount_label)
        
        summary_layout.addLayout(summary_info_layout)
        
        # Checkout button - centered
        checkout_container = QHBoxLayout()
        checkout_container.addStretch()
        
        self.checkout_btn = QPushButton("Proceed to Checkout")
        self.checkout_btn.setEnabled(False)
        self.checkout_btn.setFixedSize(250, 50)
        self.checkout_btn.clicked.connect(self.proceed_to_checkout)
        checkout_container.addWidget(self.checkout_btn)
        
        checkout_container.addStretch()
        summary_layout.addLayout(checkout_container)
      
        
    def refresh_cart(self):
        """Refresh cart display from database with improved empty state"""
        # Clear existing items
        for i in reversed(range(self.cart_layout.count())):
            child = self.cart_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Get cart items from database
        cart_items = self.db_manager.get_cart_items()
        
        if not cart_items:
            # Show centered empty cart message
            empty_container = QWidget()
            empty_layout = QVBoxLayout(empty_container)
            empty_layout.setAlignment(Qt.AlignCenter)
            
            empty_label = QLabel("🛒")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("""
                font-size: 48px;
                color: #bdc3c7;
                padding: 20px;
            """)
            empty_layout.addWidget(empty_label)
            
            message_label = QLabel("Your cart is empty")
            message_label.setAlignment(Qt.AlignCenter)
            message_label.setStyleSheet("""
                color: #7f8c8d;
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
            """)
            empty_layout.addWidget(message_label)
            
            sub_message = QLabel("Add some products to get started!")
            sub_message.setAlignment(Qt.AlignCenter)
            sub_message.setStyleSheet("""
                color: #95a5a6;
                font-size: 14px;
                padding: 5px;
            """)
            empty_layout.addWidget(sub_message)
            
            self.cart_layout.addWidget(empty_container)
        else:
            # Add cart items with maximum width for better centering
            for item_data in cart_items:
                cart_item = CartItemWidget(item_data)
                cart_item.setMaximumWidth(1000)  # Prevent items from being too wide
                cart_item.quantity_changed.connect(self.update_item_quantity)
                cart_item.remove_item.connect(self.remove_item)
                self.cart_layout.addWidget(cart_item, 0, Qt.AlignHCenter)
        
        self.update_summary()
        
    def update_item_quantity(self, item_id, new_quantity):
        """Update item quantity in database"""
        success, message = self.db_manager.update_cart_item_quantity(item_id, new_quantity)
        if not success:
            QMessageBox.warning(self, "Update Failed", message)
            self.refresh_cart()  # Refresh to show correct quantities
        else:
            self.update_summary()
            
    def remove_item(self, item_id):
        """Remove item from cart with improved dialog"""
        reply = QMessageBox.question(
            self, "Remove Item", 
            "Are you sure you want to remove this item from your cart?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.db_manager.remove_from_cart(item_id)
            if success:
                self.refresh_cart()
                # Update the cart count for auto-refresh
                cart_items = self.db_manager.get_cart_items()
                self.last_cart_count = len(cart_items) if cart_items else 0
            else:
                QMessageBox.warning(self, "Remove Failed", message)
                
    def clear_cart(self):
        """Clear entire cart with improved confirmation"""
        cart_items = self.db_manager.get_cart_items()
        if not cart_items:
            QMessageBox.information(self, "Cart Empty", "Your cart is already empty!")
            return
            
        reply = QMessageBox.question(
            self, "Clear Cart", 
            f"Are you sure you want to remove all {len(cart_items)} items from your cart?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.db_manager.clear_cart()
            if success:
                self.refresh_cart()
                self.last_cart_count = 0
                QMessageBox.information(self, "Success", "Cart cleared successfully!")
            else:
                QMessageBox.warning(self, "Clear Failed", message)
                
    def update_summary(self):
        """Update cart summary information with better formatting"""
        cart_items = self.db_manager.get_cart_items()
        
        if not cart_items:
            self.total_items_label.setText("Items: 0")
            self.total_amount_label.setText("Total: PKR 0.00")
            self.checkout_btn.setEnabled(False)
        else:
            total_items = sum(item[1] for item in cart_items)  # Sum quantities
            total_amount = sum(item[3] for item in cart_items)  # Sum line_totals
            
            # Format with proper pluralization
            item_text = "Item" if total_items == 1 else "Items"
            self.total_items_label.setText(f"{item_text}: {total_items}")
            self.total_amount_label.setText(f"Total: PKR {total_amount:,.2f}")
            self.checkout_btn.setEnabled(True)
            
    def proceed_to_checkout(self):
        """Enhanced checkout with payment tracking"""
        cart_items = self.db_manager.get_cart_items()
        print(f"Proceeding to checkout with cart items: {cart_items}")
        if not cart_items:
            QMessageBox.warning(self, "Empty Cart", "Please add items to your cart before checkout.")
            return

        total_amount = sum(item[3] for item in cart_items)

        # Open enhanced checkout dialog
        from .checkout_dialog import CheckoutDialog  # Add this import at top of file
        dialog = CheckoutDialog(cart_items, total_amount, self)
        dialog.checkout_completed.connect(self.handle_checkout_completion)
        dialog.exec()

    def handle_checkout_completion(self, sale_data):
        """Handle completed checkout - ADD THIS NEW METHOD"""
        success, message = self.db_manager.complete_sale_enhanced(sale_data)
        print(f"Checkout completed: success={success}, message={message}, sale_data={sale_data}")

        if success:
            balance = sale_data['balance_due']
            if balance > 0:
                msg = f"Sale completed! Customer owes PKR {balance:,.2f} due on {sale_data['due_date']}"
            else:
                msg = "Sale completed successfully! Payment received in full."

            QMessageBox.information(self, "Sale Completed", msg)

            # Clear cart
            self.db_manager.clear_cart()
            self.refresh_cart()
            self.last_cart_count = 0
        else:
            QMessageBox.warning(self, "Sale Failed", message)

    def add_product_to_cart(self, variant_id, quantity=1):
        """Add product to cart with immediate refresh"""
        success, message = self.db_manager.add_to_cart(variant_id, quantity)
        print(f"Adding to cart: variant_id={variant_id}, quantity={quantity}, success={success}, message={message}")
        
        if success:
            # Immediate refresh
            self.refresh_cart()
            # Update counter for auto-refresh
            cart_items = self.db_manager.get_cart_items()
            self.last_cart_count = len(cart_items) if cart_items else 0
            
            # Show success message
            QMessageBox.information(self, "Added to Cart", f"{message}")
        else:
            QMessageBox.warning(self, "Add to Cart Failed", message)
            
    def force_refresh(self):
        """Force refresh cart - can be called from other pages"""
        self.refresh_cart()
        cart_items = self.db_manager.get_cart_items()
        self.last_cart_count = len(cart_items) if cart_items else 0
    