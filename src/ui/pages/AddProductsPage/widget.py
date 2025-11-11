from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QGroupBox, QLabel,
    QLineEdit, QPushButton, QWidget, QSpinBox, QDoubleSpinBox, QFileDialog, QMessageBox,QHBoxLayout, QSpacerItem, QSizePolicy
)
from .productsimport import ProductImporter
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from .ProductsFormPage_ui import Ui_MainWindow
from ....database.database_manager import DatabaseManager
import os
import shutil


class AddProductsPage(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Container layout for all categories
        self.categories_layout = self.verticalLayout_4

        self.removegeneralimgBtn.hide()
        self.removegeneralimgBtn.setCursor(QCursor(Qt.PointingHandCursor))

        # Connect general buttons
        self.addCategoryBtn.clicked.connect(self.add_category)
        self.img_btn.clicked.connect(self.upload_image)
        self.removegeneralimgBtn.clicked.connect(self.remove_image)

        # Keep track if general fields are hidden
        self.general_hidden = False
        self.general_remove_img_btn_hidden = True

        self.saveproductbtn.clicked.connect(self.handle_save_product)

        # ADD THIS LINE - Setup import button at bottom
        self.setup_import_button()
    def setup_import_button(self):
        """Add import button at the bottom"""
        from PySide6.QtGui import QCursor
        from PySide6.QtCore import Qt

        # Create import button
        self.import_json_btn = QPushButton("Import Products (JSON)")
        self.import_json_btn.setObjectName("import_btn")
        self.import_json_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.import_json_btn.setStyleSheet("""
            #import_btn {
                background-color: #28a745;
                border: 2px solid #1e7e34;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-weight: bold;
                margin: 10px;
            }
            #import_btn:hover {
                background-color: #218838;
            }
        """)
        self.import_json_btn.clicked.connect(self.import_products)

        # Add to layout - right after saveproductbtn
        index = self.verticalLayout_2.indexOf(self.saveproductbtn)
        self.verticalLayout_2.insertWidget(index + 1, self.import_json_btn, 0, Qt.AlignHCenter)

    def import_products(self):
        """Import products from JSON file"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select JSON File",
            "",
            "JSON Files (*.json)"
        )

        if not file_name:
            return

        # Create importer
        from .productsimport import ProductImporter
        importer = ProductImporter(DatabaseManager())

        # Import
        success, imported, failed, errors = importer.import_from_json(file_name)

        # Show results
        if success:
            msg = f"Import Complete!\n\nImported: {imported}\nFailed: {failed}"
            if errors and len(errors) > 0:
                msg += f"\n\nFirst few errors:\n" + "\n".join(errors[:5])
            QMessageBox.information(self, "Import Complete", msg)
            self.clear_form()  # Clear form after successful import
        else:
            QMessageBox.critical(self, "Import Failed", "\n".join(errors))
    def add_category(self):
        """Add a new category section dynamically"""
        # Hide general fields (stock & price) only once
        if not self.general_hidden:
            self.general_info.hide()
            self.label_6.hide()
            self.img_btn.hide()
            self.image_path_label.hide()
            self.removegeneralimgBtn.hide()
            self.general_hidden = True

        group = QGroupBox("New Category")
        group.setObjectName("dynamic_category")
        layout = QVBoxLayout(group)

        # Name
        name = QLineEdit()
        layout.addWidget(QLabel("Name:"))
        name.setMaximumWidth(500)
        layout.addWidget(name)

        # Stock field
        stock_label = QLabel("Stock:")
        stock_input = QSpinBox()
        stock_input.setRange(0, 1000000)
        stock_input.setMaximumWidth(500)
        layout.addWidget(stock_label)
        layout.addWidget(stock_input)

        # Purchase Price field
        price_label = QLabel("Purchase Price:")
        price_input = QDoubleSpinBox()
        price_input.setObjectName("cat_purchase_price")
        price_input.setRange(0, 9999999.000000)
        price_input.setMaximumWidth(500)
        layout.addWidget(price_label)
        layout.addWidget(price_input)

        # Selling Price field
        selling_price_label = QLabel("Selling Price:")
        selling_price_input = QDoubleSpinBox()
        selling_price_input.setObjectName("cat_selling_price")
        selling_price_input.setRange(0, 9999999.000000)
        selling_price_input.setMaximumWidth(500)
        layout.addWidget(selling_price_label)
        layout.addWidget(selling_price_input)

        # Categories image button
        categories_img = QPushButton("Upload Image")
        categories_img.setObjectName("categories_img_btn")
        categories_img.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(categories_img, alignment=Qt.AlignCenter)

        # Per-category image label
        categories_img_path_label = QLabel("No Image Uploaded")
        categories_img_path_label.setObjectName("categories_img_path_label")
        layout.addWidget(categories_img_path_label, alignment=Qt.AlignCenter)

        # Categories image remove button
        remove_categories_img_btn = QPushButton("Remove Image")
        remove_categories_img_btn.setObjectName("remove_categories_img_btn")
        remove_categories_img_btn.setCursor(QCursor(Qt.PointingHandCursor))
        remove_categories_img_btn.hide()
        layout.addWidget(remove_categories_img_btn, alignment=Qt.AlignCenter)

        # Wire buttons to handlers with group context
        categories_img.clicked.connect(
            lambda: self.upload_cat_image(categories_img_path_label, remove_categories_img_btn)
        )
        remove_categories_img_btn.clicked.connect(
            lambda: self.remove_cat_image(categories_img_path_label, remove_categories_img_btn)
        )

        # Remove category button
        remove_btn = QPushButton("Remove Category")
        remove_btn.setObjectName("remove_category_btn")
        remove_btn.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(remove_btn, alignment=Qt.AlignCenter)

        remove_btn.clicked.connect(lambda: self.remove_category(group))

        # Add this group to the scroll area
        self.categories_layout.addWidget(group)

    def remove_category(self, group: QGroupBox):
        """Remove a category section"""
        group.setParent(None)
        group.deleteLater()

        # If no categories left, show general fields again
        if self.categories_layout.count() == 1:
            self.general_info.show()
            self.label_6.show()
            self.img_btn.show()
            self.image_path_label.show()
            # Show remove button if image was selected
            if self.image_path_label.text() != "No Image Uploaded":
                self.removegeneralimgBtn.show()
            self.general_hidden = False

    def upload_image(self):
        """Upload an image for the general product"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            self.image_path_label.setText(file_name)
            if self.general_remove_img_btn_hidden:
                self.removegeneralimgBtn.show()
                self.general_remove_img_btn_hidden = False

    def remove_image(self):
        """Clear the selected general image"""
        self.image_path_label.setText("No Image Uploaded")
        self.removegeneralimgBtn.hide()
        self.general_remove_img_btn_hidden = True

    def upload_cat_image(self, path_label: QLabel, remove_btn: QPushButton):
        """Upload an image for a specific category"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            path_label.setText(file_name)
            remove_btn.show()

    def remove_cat_image(self, path_label: QLabel, remove_btn: QPushButton):
        """Clear the selected category image"""
        path_label.setText("No Image Uploaded")
        remove_btn.hide()

    def copy_image_to_database(self, source_path):
        """Copy image to persistent images directory and return new path"""
        if not source_path or source_path == "No Image Uploaded":
            return None

        try:
            # Use AppData (Windows) or ~/.local/share (Linux/macOS)
            appdata_dir = os.getenv("APPDATA") or os.path.expanduser("~/.local/share")

            # Make a subfolder for your app images
            images_dir = os.path.join(appdata_dir, "StockManager", "images")
            os.makedirs(images_dir, exist_ok=True)

            # Get filename and create new path
            image_filename = os.path.basename(source_path)
            new_image_path = os.path.join(images_dir, image_filename)

            # Copy the file
            shutil.copy(source_path, new_image_path)

            return new_image_path
        except Exception as e:
            print(f"Error copying image: {e}")
            return None

    def handle_save_product(self):
        """Handle the saving of a product with proper validation - UPDATED"""
        # Basic product info (always required)
        name = self.base_name.text().strip()
        description = self.description.toPlainText().strip()
        brand = self.brand.text().strip()

        if not name:
            QMessageBox.warning(self, "Error", "Product name is required!")
            return

        # Check if categories were added by counting dynamic category widgets
        category_groups = self.get_category_groups()

        if len(category_groups) == 0:
            # No categories added - use general fields
            self.save_uncategorized_product(name, description, brand)
        else:
            # Categories were added - validate and save each category
            self.save_categorized_product(name, description, category_groups, brand)

    def get_category_groups(self):
        """Get all dynamically added category group boxes"""
        category_groups = []

        # Loop through all widgets in categories_layout
        for i in range(self.categories_layout.count()):
            widget = self.categories_layout.itemAt(i).widget()
            if widget and isinstance(widget, QGroupBox) and widget.objectName() == "dynamic_category":
                category_groups.append(widget)

        return category_groups

    def save_uncategorized_product(self, name, description, brand):
        """Save product using general fields (no categories) - UPDATED FOR SPLIT APPROACH"""
        # Get general field values
        original_image_path = self.image_path_label.text()
        purchase_price = self.purchaseprice.value()
        selling_price = self.sellingprice.value()
        stock_quantity = self.stockquantity.value()
    
        # Validate general fields
        if purchase_price <= 0:
            QMessageBox.warning(self, "Error", "Purchase price must be greater than 0")
            return
        if selling_price <= 0:
            QMessageBox.warning(self, "Error", "Selling price must be greater than 0")
            return
        if stock_quantity < 0:
            QMessageBox.warning(self, "Error", "Stock quantity cannot be negative!")
            return
        if selling_price < purchase_price:
            QMessageBox.warning(self, "Error", "Selling price cannot be less than purchase price!")
            return
        # Copy image to database directory
        image_path = self.copy_image_to_database(original_image_path)
    
        # Save to database using split approach
        try:
            db = DatabaseManager()
            
            # Step 1: Save base product
            product_id = db.save_base_product(name, description, brand)
            
            # Step 2: Save as "Uncategorized" variant
            db.save_product_variant(
                product_id=product_id,
                category_name="Uncategorized",
                purchase_price=purchase_price,
                selling_price=selling_price,
                stock_quantity=stock_quantity,
                image_path=image_path
            )
            
            QMessageBox.information(self, "Success", f"Product '{name}' saved successfully!")
            self.clear_form()
    
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save product: {str(e)}")

    def save_categorized_product(self, name, description, category_groups, brand="Local"):
        """Save product with multiple categories using split DB functions"""
        if not category_groups:
            QMessageBox.warning(self, "Error", "No categories found!")
            return
    
        db = DatabaseManager()
    
        try:
            # STEP 1: Save the base product ONCE
            product_id = db.save_base_product(name, description, brand)
            
            # STEP 2: Save each category as a variant of the same product
            for group in category_groups:
                category_data = self.extract_category_data(group)
    
                if not category_data:
                    continue
                
                if not self.validate_category_data(category_data):
                    return
    
                # Copy image to database directory
                image_path = self.copy_image_to_database(category_data['original_image_path'])
    
                # Save this category as a variant of the same product
                db.save_product_variant(
                    product_id=product_id,
                    category_name=category_data['category_name'],
                    purchase_price=category_data['purchase_price'],
                    selling_price=category_data['selling_price'],
                    stock_quantity=category_data['stock_quantity'],
                    image_path=image_path
                )
    
            QMessageBox.information(self, "Success", f"Product '{name}' with categories saved successfully!")
            self.clear_form()
    
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save product: {str(e)}")
            # Note: No need for rollback here since each function commits individually

    def extract_category_data(self, group_widget):
        """Extract data from a category group widget"""
        try:
            layout = group_widget.layout()

            # Initialize variables to store our data
            category_name = ""
            stock_quantity = 0
            purchase_price = 0.0
            selling_price = 0.0
            original_image_path = None

            # Get all widgets from this category group
            widgets = []
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget():
                    widgets.append(item.widget())

            # Find each type of widget using simple loops
            line_edits = []
            for w in widgets:
                if isinstance(w, QLineEdit):
                    line_edits.append(w)

            spin_boxes = []
            for w in widgets:
                if isinstance(w, QSpinBox):
                    spin_boxes.append(w)

            double_spin_boxes = []
            for w in widgets:
                if isinstance(w, QDoubleSpinBox):
                    double_spin_boxes.append(w)

            image_labels = []
            for w in widgets:
                if isinstance(w, QLabel) and w.objectName() == "categories_img_path_label":
                    image_labels.append(w)

            # Extract the actual data
            if len(line_edits) > 0:
                category_name = line_edits[0].text().strip()

            if len(spin_boxes) > 0:
                stock_quantity = spin_boxes[0].value()

            if len(double_spin_boxes) >= 2:
                purchase_price = double_spin_boxes[0].value()
                selling_price = double_spin_boxes[1].value()

            if len(image_labels) > 0:
                img_text = image_labels[0].text()
                if img_text != "No Image Uploaded":
                    original_image_path = img_text

            # Return all extracted data as dictionary
            return {
                'category_name': category_name,
                'stock_quantity': stock_quantity,
                'purchase_price': purchase_price,
                'selling_price': selling_price,
                'original_image_path': original_image_path
            }

        except Exception as e:
            print(f"Error extracting category data: {e}")
            return None

    def validate_category_data(self, data):
        """Validate category data"""
        if not data.get('category_name'):
            QMessageBox.warning(self, "Error", "Category name is required!")
            return False

        if data.get('purchase_price', 0) <= 0:
            QMessageBox.warning(self, "Error", f"Purchase price for category '{data['category_name']}' must be greater than 0!")
            return False

        if data.get('selling_price', 0) <= 0:
            QMessageBox.warning(self, "Error", f"Selling price for category '{data['category_name']}' must be greater than 0!")
            return False

        if data.get('stock_quantity', 0) < 0:
            QMessageBox.warning(self, "Error", f"Stock quantity for category '{data['category_name']}' cannot be negative!")
            return False
        if data.get('selling_price', 0) < data.get('purchase_price', 0):
            QMessageBox.warning(self, "Error", f"Selling price for category '{data['category_name']}' cannot be less than purchase price!")
            return False

        return True

    def clear_form(self):
        """Clear the form after successful save"""
        # Clear basic info
        self.base_name.clear()
        self.description.clear()
        self.brand.clear()

        # Clear general fields
        self.purchaseprice.setValue(0.0)
        self.sellingprice.setValue(0.0)
        self.stockquantity.setValue(0)

        # Reset image
        self.image_path_label.setText("No Image Uploaded")
        self.removegeneralimgBtn.hide()
        self.general_remove_img_btn_hidden = True

        # Remove all dynamic categories
        while True:
            category_groups = self.get_category_groups()
            if not category_groups:
                break
            self.remove_category(category_groups[0])

        # Show general fields again
        if self.general_hidden:
            self.general_info.show()
            self.label_6.show()
            self.img_btn.show()
            self.image_path_label.show()
            self.general_hidden = False