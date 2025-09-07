from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QGroupBox, QFormLayout, QPushButton, QLineEdit, QFrame, QFileDialog,QMessageBox,
    QDoubleSpinBox, QSpinBox
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
import os
from ...database.database_manager import DatabaseManager
class ProductDetailPage(QWidget):
    def __init__(self, product_data):
        self.db = DatabaseManager()
        super().__init__()
        self.product_data = product_data
        self.edit_mode = False  # Track edit state

        # Set dark theme styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # --- HEADER (image + name/brand/category) ---
        self.build_header()

        # --- DESCRIPTION ---
        self.build_description_section()

        # --- DETAILS ---
        self.build_details_section()

        # --- EDIT BUTTON ---
        self.build_action_buttons()

        self.main_layout.addStretch()
    def showEvent(self, event):
        """When the widget is shown, always refresh product data from DB"""
        super().showEvent(event)

        variant_id = self.product_data.get("variant_id")
        if not variant_id:
            return

        # Fetch fresh data from DB
        updated_data = self.db.get_variant_by_id(variant_id)
        if updated_data:
            self.product_data.update(updated_data)
            self.refresh_ui()

    def refresh_ui(self):
        """Update the UI elements with latest product data"""
        # Header
        self.name_label.setText(self.product_data.get("name", "Unnamed Product"))
        self.brand_label.setText(f"Brand: {self.product_data.get('brand', 'N/A')}")
        self.category_label.setText(f"Category: {self.product_data.get('category', 'N/A')}")
        self.update_image_display()

        # Description
        self.desc.setPlainText(self.product_data.get("description", "No description"))

        # Details
        self.purchase_price.setValue(float(self.product_data.get("purchase_price", 0)))
        self.selling_price.setValue(float(self.product_data.get("selling_price", 0)))
        self.stock.setValue(int(self.product_data.get("stock", 0)))
        self.variant_id.setText(str(self.product_data.get("variant_id", "N/A")))
        self.status.setText(self.product_data.get("status", "N/A"))
        
        # Action buttons
        if self.product_data.get("status") == 'active':
            self.activate_btn.hide()
            self.delete_btn.show()
            self.edit_button.show()
            self.add_button.show()
        elif self.product_data.get("status") == 'deleted':
            self.activate_btn.hide()
            self.delete_btn.hide()
            self.edit_button.hide()
            self.add_button.hide()
        else:
            self.activate_btn.show()
            self.delete_btn.hide()
            self.edit_button.hide()
            self.add_button.hide()

    def build_header(self):
        header_layout = QHBoxLayout()
        header_layout.setSpacing(30)

        # Image
        self.image_label = QLabel()
        self.image_label.setFixedSize(250, 180)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #2d2d30;
                border: 2px solid #3e3e42;
                border-radius: 8px;
            }
        """)
        
        image_path = self.product_data.get("image", "")
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(
                250, 180,
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
        else:
            self.image_label.setText("No Image")
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.setStyleSheet("""
                QLabel {
                    background-color: #2d2d30;
                    border: 2px dashed #3e3e42;
                    border-radius: 8px;
                    color: #9ca3af;
                    font-size: 14px;
                }
            """)

        header_layout.addWidget(self.image_label)

        # Name/brand/category
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)
        
        self.name_label = QLabel(self.product_data.get("name", "Unnamed Product"))
        self.name_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 10px;
        """)
        info_layout.addWidget(self.name_label)

        brand = self.product_data.get("brand", "N/A")
        self.brand_label = QLabel(f"Brand: {brand}")
        self.brand_label.setStyleSheet("""
            font-size: 14px;
            color: #9ca3af;
            padding: 2px 0;
        """)
        
        category = self.product_data.get("category", "N/A")
        self.category_label = QLabel(f"Category: {category}")
        self.category_label.setStyleSheet("""
            font-size: 14px;
            color: #9ca3af;
            padding: 2px 0;
        """)

        info_layout.addWidget(self.brand_label)
        info_layout.addWidget(self.category_label)
        info_layout.addStretch()

        header_layout.addLayout(info_layout, 1)
        self.main_layout.addLayout(header_layout)

    def build_description_section(self):
        self.desc_box = QGroupBox("Description")
        self.desc_box.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #3e3e42;
                border-radius: 8px;
                margin-top: 15px;
                background-color: #2d2d30;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: #1e1e1e;
                color: #60a5fa;
            }
        """)
        
        desc_layout = QVBoxLayout()
        desc_layout.setContentsMargins(15, 15, 15, 15)
        
        self.desc = QTextEdit(self.product_data.get("description", "No description"))
        self.desc.setReadOnly(True)
        self.desc.setMinimumHeight(100)
        self.desc.setMaximumHeight(120)
        self.desc.setStyleSheet("""
            QTextEdit {
                border: 1px solid #3e3e42;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                background-color: #1e1e1e;
                color: #ffffff;
                selection-background-color: #60a5fa;
            }
            QTextEdit:focus {
                border-color: #60a5fa;
            }
        """)
        
        desc_layout.addWidget(self.desc)
        self.desc_box.setLayout(desc_layout)
        self.main_layout.addWidget(self.desc_box)

    def build_details_section(self):
        self.details_box = QGroupBox("Product Details")
        self.details_box.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #3e3e42;
                border-radius: 8px;
                margin-top: 15px;
                background-color: #2d2d30;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: #1e1e1e;
                color: #60a5fa;
            }
        """)

        details_container = QVBoxLayout()
        details_container.setContentsMargins(15, 15, 15, 15)
        
        self.details_layout = QFormLayout()
        self.details_layout.setLabelAlignment(Qt.AlignLeft)
        self.details_layout.setVerticalSpacing(12)
        self.details_layout.setHorizontalSpacing(15)

        # Create input fields
        self.purchase_price = QDoubleSpinBox()
        self.purchase_price.setValue(float(self.product_data.get("purchase_price", 0)))
        self.selling_price = QDoubleSpinBox()
        self.selling_price.setValue(float(self.product_data.get("selling_price", 0)))
        self.stock = QSpinBox()
        self.stock.setValue(int(self.product_data.get("stock", 0)))
        self.variant_id = QLineEdit(str(self.product_data.get("variant_id", "N/A")))
        self.status = QLineEdit(self.product_data.get("status", "N/A"))

        # Read-only styling
        readonly_style = """
            QLineEdit {
                background: transparent;
                border: none;
                font-size: 13px;
                color: #ffffff;
                padding: 5px;
            }
        """

        # Edit styling
        self.edit_style = """
            QLineEdit {
                background: #1e1e1e;
                border: 2px solid #3e3e42;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #60a5fa;
            }
        """

        for field in [self.purchase_price, self.selling_price, self.stock, self.variant_id, self.status]:
            field.setReadOnly(True)
            field.setStyleSheet(readonly_style)

        # Create labels
        labels = [
            ("Purchase Price:", self.purchase_price),
            ("Selling Price:", self.selling_price),
            ("Stock:", self.stock),
            ("Variant ID:", self.variant_id),
            ("Status:", self.status)
        ]

        for label_text, field in labels:
            label = QLabel(label_text)
            label.setStyleSheet("""
                font-weight: 600;
                font-size: 13px;
                color: #9ca3af;
                min-width: 100px;
                padding: 8px;
            """)
            self.details_layout.addRow(label, field)

        details_container.addLayout(self.details_layout)
        self.details_box.setLayout(details_container)
        self.main_layout.addWidget(self.details_box)

    def build_action_buttons(self):
        self.button_layout = QHBoxLayout()

        # Edit/Save button
        self.edit_button = QPushButton("Edit")
        self.edit_button.setStyleSheet(self.blue_button_style())
        self.edit_button.clicked.connect(self.toggle_edit_mode)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setStyleSheet(self.red_button_style())
        self.delete_btn.clicked.connect(lambda: self.handle_delete_variant(self.product_data.get("variant_id")))

        self.activate_btn = QPushButton("Activate")
        self.activate_btn.setStyleSheet(self.green_button_style())
        self.activate_btn.clicked.connect(self.handle_activate_variant)

        self.add_button = QPushButton("Add to cart")
        self.add_button.setStyleSheet(self.green_button_style())
        self.add_button.clicked.connect(lambda: self.handle_add_variant(self.product_data.get("variant_id")))


        if self.product_data.get("status") == 'active':
            self.activate_btn.hide()
            self.delete_btn.show()
            self.edit_button.show()
            self.add_button.show()
        elif self.product_data.get("status") == 'deleted':
            self.activate_btn.hide()
            self.delete_btn.hide()
            self.edit_button.hide()
            self.add_button.hide()
        else:
            self.activate_btn.show()
            self.delete_btn.hide()
            self.edit_button.hide()
            self.add_button.hide()
        
        # Upload Image button (hidden initially)
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.setStyleSheet(self.gray_button_style())
        self.upload_button.clicked.connect(self.upload_image)
        self.upload_button.hide()

        # Remove Image button (hidden initially)
        self.remove_button = QPushButton("Remove Image")
        self.remove_button.setStyleSheet(self.red_button_style())
        self.remove_button.clicked.connect(self.remove_image)
        self.remove_button.hide()

        self.button_layout.addStretch()
        self.button_layout.addWidget(self.upload_button)
        self.button_layout.addWidget(self.remove_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_btn)
        self.button_layout.addWidget(self.activate_btn)
        self.button_layout.addWidget(self.add_button)
        self.main_layout.addLayout(self.button_layout)

    def toggle_edit_mode(self):
        """Switch between view and edit mode"""
        self.edit_mode = not self.edit_mode
        readonly_style = """
            QLineEdit {
                background: transparent;
                border: none;
                font-size: 13px;
                color: #ffffff;
                padding: 5px;
            }
        """

        if self.edit_mode:
            # Switch Edit → Save
            self.edit_button.setText("Save")
            self.edit_button.setStyleSheet(self.green_button_style())
            self.add_button.hide()
            self.delete_btn.hide()

            # Show image buttons
            self.upload_button.show()
            if self.product_data.get("image"):
                self.remove_button.show()

            self.desc.setReadOnly(False)
            self.desc.setStyleSheet(self.desc_edit_style())
            for field in [self.purchase_price, self.selling_price, self.stock]:
                field.setReadOnly(False)
                field.setStyleSheet(self.edit_style)

        else:
            # Switch Save → Edit
            self.edit_button.setText("Edit")
            self.edit_button.setStyleSheet(self.blue_button_style())
            self.add_button.show()
            self.delete_btn.show()

            # Hide image buttons
            self.upload_button.hide()
            self.remove_button.hide()

            self.desc.setReadOnly(True)
            self.desc.setStyleSheet(self.desc_readonly_style())
            for field in [self.purchase_price, self.selling_price, self.stock]:
                field.setReadOnly(True)
                field.setStyleSheet(readonly_style)

            # Save back to product_data
            self.product_data["description"] = self.desc.toPlainText()
            self.product_data["purchase_price"] = self.purchase_price.value()
            self.product_data["selling_price"] = self.selling_price.value()
            self.product_data["stock"] = self.stock.value()
            #  save to the database
            self.db.save_edited_products(self.product_data["description"], self.product_data["purchase_price"], self.product_data["selling_price"], self.product_data["stock"], self.product_data["image"], self.product_data["variant_id"])

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
        self, "Select Product Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
    )
        if file_path:
            self.product_data["image"] = file_path
            self.update_image_display()
            self.remove_button.show()

    def remove_image(self):
        self.product_data["image"] = ""
        self.update_image_display()
        self.remove_button.hide()

    def update_image_display(self):
        """Refresh image in header"""
        image_path = self.product_data.get("image", "")
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(
                250, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.image_label.setPixmap(pixmap)
            self.image_label.setText("")

        else:
            self.image_label.clear()
            self.image_label.setText("No Image")

# --- Button style helpers ---
    def blue_button_style(self):
        return """
            QPushButton {
                background-color: #60a5fa;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #3b82f6; }
            QPushButton:pressed { background-color: #2563eb; }
        """

    def green_button_style(self):
        return """
            QPushButton {
                background-color: #10b981;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #059669; }
            QPushButton:pressed { background-color: #047857; }
        """

    def gray_button_style(self):
        return """
        QPushButton {
            background-color: #4b5563;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 10px 16px;
            font-size: 12px;
        }
        QPushButton:hover { background-color: #374151; }
        QPushButton:pressed { background-color: #1f2937; }
        """

    def red_button_style(self):
        return """
            QPushButton {
                background-color: #ef4444;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #dc2626; }
            QPushButton:pressed { background-color: #b91c1c; }
        """

# --- Description styles ---
    def desc_readonly_style(self):
        return """
            QTextEdit {
                border: 1px solid #3e3e42;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                background-color: #1e1e1e;
                color: #ffffff;
                selection-background-color: #60a5fa;
            }
        """

    def desc_edit_style(self):
        return """
            QTextEdit {
                border: 2px solid #60a5fa;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                background-color: #1e1e1e;
                color: #ffffff;
                selection-background-color: #60a5fa;
            }
        """
    def handle_delete_variant(self, variant_id: int):
        """Ask user before deleting a variant and maybe the base product"""
        # Confirm deletion of variant
        confirm_variant = QMessageBox.question(
            self,
            "Delete Variant?",
            "Are you sure you want to delete this variant?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm_variant != QMessageBox.Yes:
            return  # user cancelled

        result, message = self.db.delete_variant(variant_id)
        
        if result:
            # Success, update data and UI
            self.product_data["status"] = "deleted"
            self.refresh_ui()
            QMessageBox.information(self, "Variant Deleted", f"{message}")
            # Optionally navigate away if the variant is deleted
            main_window = self.window()
            main_window.stacked_widget.setCurrentIndex(1)
        else:

            # Failed or special case (like your example: linked to sales)
            QMessageBox.critical(self, "Error", f"Failed to delete variant: {message}")
            if message == "This product is linked to completed sales and can only be deactivated. It has been marked as inactive.":
                # The database marked it as inactive, so we update the UI accordingly
                self.product_data["status"] = "deactivated"
                self.refresh_ui()

        # No navigation here, user stays on the page to see the change.
        # If you need to navigate away, you would do it here.
        # For example:
        # main_window = self.window()
        # main_window.stacked_widget.setCurrentIndex(1)
        # But this would prevent the user from seeing the immediate UI change.

    def handle_activate_variant(self):
       self.db.reactivate_variant(self.product_data.get("variant_id"))
       # Update the product data and refresh the UI
       self.product_data["status"] = "active"
       self.refresh_ui()

    def handle_add_variant(self, variant_id: int):
        from ..pages.SalesPage.widget import CartManager
        cart_manager = CartManager(self)
        try:
            cart_manager.add_product_to_cart(variant_id)
        except Exception as e:
            print(f"Error adding to cart: {e}")   