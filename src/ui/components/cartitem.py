from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSpinBox, QFrame, QScrollArea, 
                             QMessageBox, QGridLayout, QSizePolicy)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QFont
import os

class CartItemWidget(QFrame):
    """Individual cart item widget that integrates with database"""
    quantity_changed = Signal(int, int)  # item_id, new_quantity
    remove_item = Signal(int)  # item_id
    
    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        
        # Extract data from database result
        (self.item_id, self.quantity, self.unit_price, self.line_total, 
         self.line_profit, self.product_name, self.category_name, 
         self.image_path, self.variant_id, self.stock_quantity) = item_data
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the cart item UI"""
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border: 2px solid #34495e;
                border-radius: 12px;
                padding: 12px;
                margin: 6px;
            }
            QFrame:hover {
                border-color: #3498db;
            }
            QLabel {
                color: white;
                font-size: 13px;
            }
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QSpinBox {
                background-color: #34495e;
                color: white;
                border: 1px solid #5d6d7e;
                border-radius: 4px;
                padding: 4px;
                font-size: 12px;
            }
        """)
        
        # Main horizontal layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        
        # Product image
        self.image_label = QLabel()
        self.image_label.setFixedSize(80, 80)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 1px solid #5d6d7e;
                border-radius: 8px;
                background-color: #34495e;
            }
        """)
        self.load_product_image()
        main_layout.addWidget(self.image_label)
        
        # Product info section
        info_layout = QVBoxLayout()
        
        # Product name
        name_font = QFont()
        name_font.setBold(True)
        name_font.setPointSize(14)
        
        self.name_label = QLabel(self.product_name)
        self.name_label.setFont(name_font)
        self.name_label.setStyleSheet("color: #ecf0f1; font-weight: bold;")
        info_layout.addWidget(self.name_label)
        
        # Category
        self.category_label = QLabel(f"Category: {self.category_name}")
        self.category_label.setStyleSheet("color: #bdc3c7; font-size: 11px;")
        info_layout.addWidget(self.category_label)
        
        # Stock info
        stock_color = "#27ae60" if self.stock_quantity > 5 else "#f39c12" if self.stock_quantity > 0 else "#e74c3c"
        self.stock_label = QLabel(f"Stock: {self.stock_quantity}")
        self.stock_label.setStyleSheet(f"color: {stock_color}; font-size: 11px; font-weight: bold;")
        info_layout.addWidget(self.stock_label)
        
        main_layout.addLayout(info_layout, 2)  # Give more space to info
        
        # Price and quantity section
        price_qty_layout = QVBoxLayout()
        
        # Unit price
        self.price_label = QLabel(f"PKR {self.unit_price:.2f}")
        self.price_label.setStyleSheet("color: #f39c12; font-weight: bold; font-size: 13px;")
        price_qty_layout.addWidget(self.price_label, alignment=Qt.AlignCenter)
        
        # Quantity controls
        qty_layout = QHBoxLayout()
        qty_label = QLabel("Qty:")
        qty_label.setStyleSheet("color: #bdc3c7; font-size: 11px;")
        qty_layout.addWidget(qty_label)
        
        self.qty_spinbox = QSpinBox()
        self.qty_spinbox.setMinimum(1)
        self.qty_spinbox.setMaximum(self.stock_quantity)
        self.qty_spinbox.setValue(self.quantity)
        self.qty_spinbox.setFixedWidth(70)
        qty_layout.addWidget(self.qty_spinbox)
        
        price_qty_layout.addLayout(qty_layout)
        
        # Line total
        self.total_label = QLabel(f"Total: PKR {self.line_total:.2f}")
        self.total_label.setStyleSheet("color: #27ae60; font-weight: bold; font-size: 14px;")
        price_qty_layout.addWidget(self.total_label, alignment=Qt.AlignCenter)
        
        main_layout.addLayout(price_qty_layout, 1)
        
        # Remove button
        self.remove_btn = QPushButton("Remove")
        self.remove_btn.setFixedSize(80, 35)
        main_layout.addWidget(self.remove_btn, alignment=Qt.AlignCenter)
        
    def load_product_image(self):
        """Load product image or show placeholder"""
        if self.image_path and os.path.exists(self.image_path):
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(78, 78, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setAlignment(Qt.AlignCenter)
                return
        
        # Placeholder image
        self.image_label.setText("No\nImage")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet(self.image_label.styleSheet() + "color: #7f8c8d;")
        
    def setup_connections(self):
        """Setup signal connections"""
        self.qty_spinbox.valueChanged.connect(self.on_quantity_changed)
        self.remove_btn.clicked.connect(self.on_remove_clicked)
        
    def on_quantity_changed(self, new_quantity):
        """Handle quantity change"""
        # Update total display
        new_total = new_quantity * self.unit_price
        self.total_label.setText(f"Total: PKR {new_total:.2f}")
        
        # Emit signal for database update
        self.quantity_changed.emit(self.item_id, new_quantity)
        
    def on_remove_clicked(self):
        """Handle remove button click"""
        self.remove_item.emit(self.item_id)


# class CartManager(QWidget):
#     """Main cart management widget"""
    
#     def __init__(self, db_manager, parent=None):
#         super().__init__(parent)
#         self.db_manager = db_manager
#         self.setup_ui()
#         self.refresh_cart()
        
#     def setup_ui(self):
#         """Setup the main cart UI"""
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(10, 10, 10, 10)
        
#         # Header
#         header_layout = QHBoxLayout()
        
#         title = QLabel("Shopping Cart")
#         title.setStyleSheet("""
#             font-size: 24px;
#             font-weight: bold;
#             color: #2c3e50;
#             padding: 10px;
#         """)
#         header_layout.addWidget(title)
        
#         # Clear cart button
#         self.clear_btn = QPushButton("Clear Cart")
#         self.clear_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #95a5a6;
#                 color: white;
#                 border-radius: 6px;
#                 padding: 8px 16px;
#                 font-weight: bold;
#             }
#             QPushButton:hover {
#                 background-color: #7f8c8d;
#             }
#         """)
#         self.clear_btn.clicked.connect(self.clear_cart)
#         header_layout.addWidget(self.clear_btn)
        
#         layout.addLayout(header_layout)
        
#         # Scroll area for cart items
#         scroll_area = QScrollArea()
#         scroll_area.setWidgetResizable(True)
#         scroll_area.setStyleSheet("""
#             QScrollArea {
#                 border: none;
#                 background-color: #ecf0f1;
#             }
#         """)
        
#         # Cart items container
#         self.cart_container = QWidget()
#         self.cart_layout = QVBoxLayout(self.cart_container)
#         self.cart_layout.setAlignment(Qt.AlignTop)
        
#         scroll_area.setWidget(self.cart_container)
#         layout.addWidget(scroll_area, 1)  # Takes most space
        
#         # Cart summary section
#         self.setup_summary_section()
#         layout.addWidget(self.summary_frame)
        
#     def setup_summary_section(self):
#         """Setup cart summary section"""
#         self.summary_frame = QFrame()
#         self.summary_frame.setFrameShape(QFrame.StyledPanel)
#         self.summary_frame.setStyleSheet("""
#             QFrame {
#                 background-color: #34495e;
#                 border-radius: 8px;
#                 padding: 15px;
#             }
#             QLabel {
#                 color: white;
#                 font-size: 14px;
#             }
#             QPushButton {
#                 background-color: #27ae60;
#                 color: white;
#                 border-radius: 6px;
#                 padding: 12px 24px;
#                 font-weight: bold;
#                 font-size: 16px;
#             }
#             QPushButton:hover {
#                 background-color: #2ecc71;
#             }
#             QPushButton:disabled {
#                 background-color: #7f8c8d;
#             }
#         """)
        
#         summary_layout = QVBoxLayout(self.summary_frame)
        
#         # Summary info
#         summary_info_layout = QHBoxLayout()
        
#         self.total_items_label = QLabel("Items: 0")
#         self.total_items_label.setStyleSheet("font-weight: bold; color: #ecf0f1;")
#         summary_info_layout.addWidget(self.total_items_label)
        
#         summary_info_layout.addStretch()
        
#         self.total_amount_label = QLabel("Total: PKR 0.00")
#         self.total_amount_label.setStyleSheet("font-weight: bold; color: #f39c12; font-size: 18px;")
#         summary_info_layout.addWidget(self.total_amount_label)
        
#         summary_layout.addLayout(summary_info_layout)
        
#         # Checkout button
#         self.checkout_btn = QPushButton("Proceed to Checkout")
#         self.checkout_btn.setEnabled(False)
#         self.checkout_btn.clicked.connect(self.proceed_to_checkout)
#         summary_layout.addWidget(self.checkout_btn)
        
#     def refresh_cart(self):
#         """Refresh cart display from database"""
#         # Clear existing items
#         for i in reversed(range(self.cart_layout.count())):
#             child = self.cart_layout.itemAt(i).widget()
#             if child:
#                 child.setParent(None)
        
#         # Get cart items from database
#         cart_items = self.db_manager.get_cart_items()
        
#         if not cart_items:
#             # Show empty cart message
#             empty_label = QLabel("Your cart is empty")
#             empty_label.setAlignment(Qt.AlignCenter)
#             empty_label.setStyleSheet("""
#                 color: #7f8c8d;
#                 font-size: 18px;
#                 padding: 50px;
#             """)
#             self.cart_layout.addWidget(empty_label)
#         else:
#             # Add cart items
#             for item_data in cart_items:
#                 cart_item = CartItemWidget(item_data)
#                 cart_item.quantity_changed.connect(self.update_item_quantity)
#                 cart_item.remove_item.connect(self.remove_item)
#                 self.cart_layout.addWidget(cart_item)
        
#         self.update_summary()
        
#     def update_item_quantity(self, item_id, new_quantity):
#         """Update item quantity in database"""
#         success, message = self.db_manager.update_cart_item_quantity(item_id, new_quantity)
#         if not success:
#             QMessageBox.warning(self, "Update Failed", message)
#             self.refresh_cart()  # Refresh to show correct quantities
#         else:
#             self.update_summary()
            
#     def remove_item(self, item_id):
#         """Remove item from cart"""
#         reply = QMessageBox.question(
#             self, "Remove Item", 
#             "Are you sure you want to remove this item from cart?",
#             QMessageBox.Yes | QMessageBox.No,
#             QMessageBox.No
#         )
        
#         if reply == QMessageBox.Yes:
#             success, message = self.db_manager.remove_from_cart(item_id)
#             if success:
#                 self.refresh_cart()
#             else:
#                 QMessageBox.warning(self, "Remove Failed", message)
                
#     def clear_cart(self):
#         """Clear entire cart"""
#         if self.cart_layout.count() == 0:
#             return
            
#         reply = QMessageBox.question(
#             self, "Clear Cart", 
#             "Are you sure you want to clear the entire cart?",
#             QMessageBox.Yes | QMessageBox.No,
#             QMessageBox.No
#         )
        
#         if reply == QMessageBox.Yes:
#             success, message = self.db_manager.clear_cart()
#             if success:
#                 self.refresh_cart()
#             else:
#                 QMessageBox.warning(self, "Clear Failed", message)
                
#     def update_summary(self):
#         """Update cart summary information"""
#         cart_items = self.db_manager.get_cart_items()
        
#         if not cart_items:
#             self.total_items_label.setText("Items: 0")
#             self.total_amount_label.setText("Total: PKR 0.00")
#             self.checkout_btn.setEnabled(False)
#         else:
#             total_items = sum(item[1] for item in cart_items)  # Sum quantities
#             total_amount = sum(item[3] for item in cart_items)  # Sum line_totals
            
#             self.total_items_label.setText(f"Items: {total_items}")
#             self.total_amount_label.setText(f"Total: PKR {total_amount:.2f}")
#             self.checkout_btn.setEnabled(True)
            
#     def proceed_to_checkout(self):
#         """Handle checkout button click"""
#         # This would open a checkout dialog or page
#         # For now, just show a message
#         QMessageBox.information(
#             self, "Checkout", 
#             "Checkout functionality to be implemented.\nThis will open customer details and payment processing."
#         )

#     def add_product_to_cart(self, variant_id, quantity=1):
#         """Add product to cart (called from product display)"""
#         success, message = self.db_manager.add_to_cart(variant_id, quantity)
        
#         if success:
#             self.refresh_cart()
#             QMessageBox.information(self, "Success", message)
#         else:
#             QMessageBox.warning(self, "Add to Cart Failed", message)


# # Example usage and integration
# class ProductCard(QFrame):
#     """Example product card with 'Add to Cart' functionality"""
    
#     def __init__(self, product_data, cart_manager, parent=None):
#         super().__init__(parent)
#         self.cart_manager = cart_manager
        
#         # Extract product data
#         (self.product_id, self.product_name, self.product_description, 
#          self.product_brand, self.category_name, self.purchase_price, 
#          self.selling_price, self.stock_quantity, self.image_path, 
#          self.variant_id) = product_data
         
#         self.setup_ui()
        
#     def setup_ui(self):
#         """Setup product card UI"""
#         layout = QVBoxLayout(self)
        
#         # Product image
#         image_label = QLabel()
#         image_label.setFixedSize(150, 150)
#         image_label.setStyleSheet("border: 1px solid #ccc; border-radius: 8px;")
        
#         if self.image_path and os.path.exists(self.image_path):
#             pixmap = QPixmap(self.image_path)
#             if not pixmap.isNull():
#                 scaled_pixmap = pixmap.scaled(148, 148, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#                 image_label.setPixmap(scaled_pixmap)
#                 image_label.setAlignment(Qt.AlignCenter)
#         else:
#             image_label.setText("No Image")
#             image_label.setAlignment(Qt.AlignCenter)
            
#         layout.addWidget(image_label)
        
#         # Product name
#         name_label = QLabel(self.product_name)
#         name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
#         layout.addWidget(name_label)
        
#         # Category
#         category_label = QLabel(f"Category: {self.category_name}")
#         category_label.setStyleSheet("color: gray; font-size: 12px;")
#         layout.addWidget(category_label)
        
#         # Price
#         price_label = QLabel(f"PKR {self.selling_price}")
#         price_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")
#         layout.addWidget(price_label)
        
#         # Add to Cart button
#         add_to_cart_btn = QPushButton("Add to Cart")
#         add_to_cart_btn.clicked.connect(self.add_to_cart)
#         layout.addWidget(add_to_cart_btn)
        
#     def add_to_cart(self):
#         """Add this product to cart"""
#         self.cart_manager.add_product_to_cart(self.variant_id, 1)