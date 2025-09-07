import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt, QTimer
from ....ui.components.card import ProductCard  # Your ProductCard component
from .HomePage_ui import Ui_HomePage  # Your compiled UI file
from ....database.database_manager import DatabaseManager

class HomePage(QMainWindow, Ui_HomePage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Store all products data for filtering
        self.all_products = []
        
        # Setup search functionality
        self.setup_search()
        
        # Setup dynamic products area
        self.setup_products_area()

        # Load actual products
        self.load_products_for_display()

    def setup_search(self):
        """Setup search functionality"""
        # Connect search box to filter function
        if hasattr(self, 'searchbox'):
            # Use QTimer to delay search (avoid searching on every keystroke)
            self.search_timer = QTimer()
            self.search_timer.setSingleShot(True)
            self.search_timer.timeout.connect(self.filter_products)
            
            # Connect textChanged to start timer
            self.searchbox.textChanged.connect(self.on_search_text_changed)
            
            # Set placeholder text
            self.searchbox.setPlaceholderText("Search products by name or category...")
        else:
            print("Warning: searchbox widget not found!")

    def on_search_text_changed(self):
        """Called when search text changes - starts timer to delay search"""
        # Stop existing timer
        self.search_timer.stop()
        # Start new timer (300ms delay)
        self.search_timer.start(300)

    def filter_products(self):
        """Filter products based on search text"""
        try:
            search_text = self.searchbox.text().lower().strip()
            
            # Clear current products display
            self.clear_products()
            
            if not search_text:
                # If search is empty, show all products
                self.display_products(self.all_products)
            else:
                # Filter products by name or category
                filtered_products = []
                for product in self.all_products:
                    product_name = product.get('name', '').lower()
                    product_category = product.get('category', '').lower()
                    product_brand = product.get('brand', '').lower()
                    
                    # Check if search text matches name, category, or brand
                    if (search_text in product_name or 
                        search_text in product_category or 
                        search_text in product_brand):
                        filtered_products.append(product)
                
                # Display filtered products
                self.display_products(filtered_products)
                
        except Exception as e:
            print(f"Error filtering products: {e}")

    def display_products(self, products_list):
        """Display a list of products"""
        try:
            if len(products_list) == 0:
                # Show "no results" message
                search_text = getattr(self, 'searchbox', None)
                if search_text and search_text.text().strip():
                    message = f"No products found for '{search_text.text()}'"
                else:
                    message = "No products added yet"
                    
                label = QLabel(message)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        color: #666;
                        font-size: 16px;
                        padding: 20px;
                    }
                """)
                self.products_grid.addWidget(label, 0, 0, 1, 3)
                return

            # Display products
            for product in products_list:
                self.add_product_card(product)
                
        except Exception as e:
            print(f"Error displaying products: {e}")

    def setup_products_area(self):
        """Setup the dynamic products grid area"""
        # Access your scroll area widget directly 
        self.products_container = self.scrollAreaWidgetContents  # Direct access, no self.ui needed!
        
        # Get the EXISTING grid layout instead of creating a new one
        self.products_grid = self.products_container.layout()
        
        # Configure the existing layout
        self.products_grid.setSpacing(10)  # Space between cards
        
        # Keep track of current position
        self.current_row = 0
        self.current_col = 0
    
    def add_product_card(self, product_data):
        """Add a single product card to the grid"""
        # Create the card
        card = ProductCard(product_data)
        card.card_clicked.connect(self.open_product_detail)
        card.add_to_cart_clicked.connect(self.on_add_to_cart)

        # Connect signals to handle clicks
        # card.card_clicked.connect(self.on_product_clicked)
        # card.add_to_cart_clicked.connect(self.on_add_to_cart)
        
        # Add to grid layout
        self.products_grid.addWidget(card, self.current_row, self.current_col)
        
        # Update position for next card
        self.current_col += 1
        if self.current_col >= 3:  # Max 3 per row
            self.current_col = 0
            self.current_row += 1
    
    def on_add_to_cart(self, product_data):
        from ....ui.pages.SalesPage.widget import CartManager
        cart_manager = CartManager(self)
        try:
            cart_manager.add_product_to_cart(product_data.get("variant_id"))
        except Exception as e:
            print(f"Error adding to cart: {e}")    

    def open_product_detail(self, product_data):
        from ....ui.components.productdetailspage import ProductDetailPage
        detail_page = ProductDetailPage(product_data)
        main_window = self.window()  # access Main_Window
        main_window.stacked_widget.addWidget(detail_page)
        main_window.stacked_widget.setCurrentWidget(detail_page)
    
    def refresh_products(self):
        """Refresh all products from database"""
        try:
            print("Refreshing products...")

            # Clear existing products data
            self.all_products.clear()
            
            # Clear existing cards
            self.clear_products()

            # Reload from database
            self.load_products_for_display()

            print("Products refreshed successfully!")

        except Exception as e:
            print(f"Error refreshing products: {e}")

    def clear_products(self):
        """Clear all product cards from the grid"""
        if not hasattr(self, 'products_grid') or self.products_grid is None:
            return

        # Remove all widgets from the grid
        while self.products_grid.count():
            item = self.products_grid.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        # Reset position counters
        self.current_row = 0
        self.current_col = 0

    def load_products_for_display(self):
        """Load all products and display them"""
        try:
            db = DatabaseManager()
            products_data = db.get_all_products_for_display()
            
            # Clear and repopulate all_products list
            self.all_products.clear()
            
            if len(products_data) == 0:
                # No products in database
                self.display_products([])
                return

            # Store all products for filtering
            for row in products_data:
                product_id = row[0]
                product_name = row[1] 
                product_description = row[2]
                brand = row[3]
                category = row[4]
                purchase_price = row[5]
                selling_price = row[6]
                stock = row[7]
                image_path = row[8]
                variant_id = row[9]
                status = row[10]  # New status field
                deactivated_reason = row[11]

                # Create product info dictionary
                product_info = {
                    'id': product_id,
                    'name': product_name,
                    'description': product_description,
                    'brand': brand,
                    'category': category,
                    'purchase_price': purchase_price,
                    'selling_price': selling_price,
                    'stock': stock,
                    'image': image_path,
                    'variant_id': variant_id,
                    'status': status,
                    'deactivated_reason': deactivated_reason
                }
                
                # Add to all products list
                self.all_products.append(product_info)
            
            # Display all products initially (or apply current search filter)
            if hasattr(self, 'searchbox') and self.searchbox.text().strip():
                # If there's already a search term, filter products
                self.filter_products()
            else:
                # Show all products
                self.display_products(self.all_products)

        except Exception as e:
            print(f"Error loading products: {e}")

    def clear_search(self):
        """Clear search and show all products"""
        if hasattr(self, 'searchbox'):
            self.searchbox.clear()
        self.display_products(self.all_products)

    def search_by_category(self, category_name):
        """Programmatically search by category"""
        if hasattr(self, 'searchbox'):
            self.searchbox.setText(category_name)

    def get_search_results_count(self):
        """Get count of current search results"""
        if not hasattr(self, 'searchbox'):
            return len(self.all_products)
            
        search_text = self.searchbox.text().lower().strip()
        if not search_text:
            return len(self.all_products)
        
        count = 0
        for product in self.all_products:
            product_name = product.get('name', '').lower()
            product_category = product.get('category', '').lower()
            product_brand = product.get('brand', '').lower()
            
            if (search_text in product_name or 
                search_text in product_category or 
                search_text in product_brand):
                count += 1
        
        return count


# Usage example
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = HomePage()
    window.show()
    
    sys.exit(app.exec())