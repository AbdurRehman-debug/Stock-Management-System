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
        
        # Try pattern: 2x/650) 1200 (stock, purchase, selling separated)
        match = re.search(r'(\d+)x/?(\d+)\)?\s*(\d+)', category_str)
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



# ============== JSON FILE FORMAT - BOTH WORK! ==============
"""
FORMAT 1: String format (messy, needs parsing)
[
  {
    "Name": "Reno 12F",
    "Brand": "OPPO",
    "Categories": {
      "8/256GB": "5x141250(150000)",
      "12/512GB": "3x180000(195000)"
    }
  }
]

FORMAT 2: Pre-parsed format (clean, already structured)
[
  {
    "Name": "Reno 12F",
    "Brand": "OPPO",
    "Description": "Latest flagship",
    "Categories": {
      "8/256GB": {
        "stock": 5,
        "purchase_price": 141250,
        "selling_price": 150000
      },
      "12/512GB": {
        "stock": 3,
        "purchase_price": 180000,
        "selling_price": 195000
      }
    }
  },
  {
    "Name": "A18",
    "Brand": "Samsung",
    "Categories": {
      "64GB": {
        "stock": 10,
        "purchase_price": 18000,
        "selling_price": 21000
      }
    }
  }
]

FORMAT 3: No categories (saves as "Uncategorized")
[
  {
    "Name": "Simple Phone",
    "Brand": "Local",
    "Description": "Basic phone with no variants"
  }
]

All three formats work! Mix and match in the same file if you want.
"""