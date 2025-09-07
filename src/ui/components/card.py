import os
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QFont


class ProductCard(QFrame):
    """Reusable Product Card Component"""

    # Signals for handling clicks
    card_clicked = Signal(dict)         # Emits product data when card is clicked
    add_to_cart_clicked = Signal(dict)  # Emits when add to cart is clicked

    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.setup_ui()
        self.setup_styling()

    def setup_ui(self): 
        """Create the card UI"""
        self.setFixedSize(310, 484)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Product Image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(150, 150)
        self.load_image()
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addSpacing(10)

        # Title
        self.title_label = QLabel(self.product_data.get("name", "No Name"))
        self.title_label.setObjectName("title_label")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.subtitle_label = QLabel(f"Category: {self.product_data.get('category', 'uncategorized')}")
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setObjectName("subtitle_label")
        layout.addWidget(self.subtitle_label)


        # Price
        price = self.product_data.get("selling_price", 0)
        self.price_label = QLabel(f"PKR {price:.2f}")
        self.price_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.price_label)

        # Brand (optional)
        brand = self.product_data.get("brand", "")

        self.brand_label = QLabel(brand)
        self.brand_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.brand_label)

    #set stock styling based on quantity


        #stock
        stock = self.product_data.get("stock", 0)
        self.stock_label = QLabel(f"Stock: {stock}")
        self.stock_label.setAlignment(Qt.AlignCenter)
        self.stock_label.setStyleSheet("color: #28a745; font-weight: bold; font-size:16px;")  # Green for in stock
        if stock == 0:
            self.stock_label.setStyleSheet("color: #d32f2f; font-weight: bold; font-size:16px;")  # Red for out of stock
        
        layout.addWidget(self.stock_label)

                # Buttons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        self.view_btn = QPushButton("View")
        self.view_btn.clicked.connect(self.on_view_clicked)
        button_layout.addWidget(self.view_btn)

        # Check product variant status (now at index 10 in the updated query)
        variant_status = self.product_data.get("status") # variant_status
        deactivated_reason = self.product_data.get("deactivated_reason")  # deactivated_reason

        if variant_status == 'active':
            # Show normal Add to Cart button
            self.cart_btn = QPushButton("Add to Cart")
            self.cart_btn.clicked.connect(self.on_cart_clicked)
            button_layout.addWidget(self.cart_btn)
            if stock == 0:
                self.cart_btn.setEnabled(False)
                self.cart_btn.setText("Out of Stock")
                self.cart_btn.setStyleSheet("background-color: #d32f2f;")  # Red background for out of stock
           
        else:
            # Show red DEACTIVATED label
            reason_text = deactivated_reason if deactivated_reason else "Product discontinued"
            self.deactivated_label = QLabel("DEACTIVATED")
            self.deactivated_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    background-color: #d32f2f;
                    font-weight: bold;
                    font-size: 11px;
                    padding: 8px;
                    border-radius: 4px;
                    text-align: center;
                }
            """)
            self.deactivated_label.setAlignment(Qt.AlignCenter)
            self.deactivated_label.setToolTip(reason_text)  # Show reason on hover
            button_layout.addWidget(self.deactivated_label)

        layout.addStretch()
        layout.addLayout(button_layout)

    def load_image(self):
        """Load product image or show placeholder"""
        image_path = self.product_data.get("image", "")

        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(
                150,
                150,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setStyleSheet("""
            
                    border: 2px solid #dee2e6;
                    color: #6c757d;
                    border-radius: 8px;


            """)
        else:
            self.image_label.setPixmap(QPixmap())
            self.image_label.setText("No Image")
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.setStyleSheet("""
                    background-color: #f8f9fa;
                    border: 2px dashed #dee2e6;
                    color: #6c757d;
                    border-radius: 8px;
                    font-size: 12px;


              
            """)

    def setup_styling(self):
        """Apply card styling"""
        self.setStyleSheet("""
            ProductCard {
                background-color: #110e1b;
                color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                margin: 12px;
                padding: 12px;


            }
            ProductCard:hover {
                border: 1px solid #007bff;
            }

            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            #subtitle_label
            {
                color: #6c757d;
                font-size: 14px;
                           

            }
            #title_label
            {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
            }
           
        """)

        # Special styling
        self.price_label.setStyleSheet("color: #28a745; font-weight: bold; font-size: 16px;")
        if hasattr(self, "brand_label"):
            self.brand_label.setStyleSheet("color: #6c757d; font-size: 18px;")

    # --- Signal emitters ---
    def on_view_clicked(self):
        self.card_clicked.emit(self.product_data)

    def on_cart_clicked(self):
        self.add_to_cart_clicked.emit(self.product_data)

    # def update_product_data(self, new_data):
    #     """Update card with new product data"""
    #     self.product_data = new_data
    #     self.title_label.setText(new_data.get("name", "No Name"))
    #     self.price_label.setText(f"${new_data.get('price', 0):.2f}")
    #     if hasattr(self, "brand_label"):
    #         self.brand_label.setText(new_data.get("brand", ""))
    #     self.load_image()
