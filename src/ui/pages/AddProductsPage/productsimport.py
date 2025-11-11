from ....database.database_manager import DatabaseManager
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QGroupBox, QLabel,
    QLineEdit, QPushButton, QWidget, QSpinBox, QDoubleSpinBox, QFileDialog, QMessageBox
)
"""
Simple Product Import - Add to AddProductsPage
"""

import json
import re
from PySide6.QtWidgets import QFileDialog, QMessageBox


class ProductImporter:
    """Simple product importer for JSON files"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def parse_category_string(self, category_str):
        """
        Parse category string like "3x1500(4500)" or "2x/650) 1200"
        Returns: (stock, purchase_price, selling_price)
        """
        if not category_str or category_str.strip() == "":
            return None
        
        # Try pattern: 3x1500(4500) or 3x1500 (4500)
        match = re.search(r'(\d+)x(\d+)\s*\((\d+)\)', category_str)
        if match:
            stock = int(match.group(1))
            purchase = float(match.group(2))
            selling = float(match.group(3))
            return (stock, purchase, selling)
        
        
        
        return None
    
    def import_from_json(self, file_path):
        """Import products from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            imported = 0
            failed = 0
            errors = []
            
            for product in data:
                try:
                    name = product.get('Name', '').strip()
                    if not name:
                        failed += 1
                        errors.append(f"Missing name for product")
                        continue
                    
                    brand = product.get('Brand', 'Local')
                    description = product.get('Description', '')
                    categories = product.get('Categories', {})
                    
                    # Save base product
                    product_id = self.db.save_base_product(name, description, brand)
                    
                    # Check if categories exist
                    if not categories or len(categories) == 0:
                        # Save as uncategorized
                        self.db.save_product_variant(
                            product_id=product_id,
                            category_name="Uncategorized",
                            purchase_price=0,
                            selling_price=0,
                            stock_quantity=0
                        )
                    else:
                        # Save each category
                        for cat_name, cat_value in categories.items():
                            parsed = self.parse_category_string(cat_value)
                            if parsed:
                                stock, purchase, selling = parsed
                                self.db.save_product_variant(
                                    product_id=product_id,
                                    category_name=cat_name,
                                    purchase_price=purchase,
                                    selling_price=selling,
                                    stock_quantity=stock
                                )
                            else:
                                # If can't parse, save with 0 values
                                self.db.save_product_variant(
                                    product_id=product_id,
                                    category_name=cat_name,
                                    purchase_price=0,
                                    selling_price=0,
                                    stock_quantity=0
                                )
                    
                    imported += 1
                    
                except Exception as e:
                    failed += 1
                    errors.append(f"{name}: {str(e)}")
            
            return True, imported, failed, errors
            
        except Exception as e:
            return False, 0, 0, [f"Failed to read file: {str(e)}"]



# ============== JSON FILE FORMAT ==============
"""
Save this as 'products.json':

[
  {
    "Name": "Reno 12F",
    "Brand": "OPPO",
    "Description": "Latest Reno series",
    "Categories": {
      "R+B": "141250 (1950) 2x/ifo (1750)",
      "B": "1x600 (1150)"
    }
  },
  {
    "Name": "Note 50 (C51)",
    "Brand": "Infinix",
    "Categories": {
      "R+B": "2x/650) 1200"
    }
  },
  {
    "Name": "A18",
    "Brand": "Samsung",
    "Categories": {
      "Hosing+B": "1x(1250) (2100)"
    }
  },
  {
    "Name": "AS4, added",
    "Brand": "Samsung",
    "Categories": {
      "R+B": "2x750 (850)/(1200)",
      "B": "1x300 (500)",
      "Hosing+B": "1x1050 (1550)"
    }
  },
  {
    "Name": "Simple Product",
    "Brand": "Local",
    "Description": "No categories"
  }
]

Or simpler format:

[
  {
    "Name": "Reno 12F",
    "Categories": {
      "8/256GB": "5x141250(150000)",
      "12/512GB": "3x180000(195000)"
    }
  }
]

Format: STOCKxPURCHASE_PRICE(SELLING_PRICE)
Example: 5x141250(150000) = 5 units, buy at 141250, sell at 150000
"""