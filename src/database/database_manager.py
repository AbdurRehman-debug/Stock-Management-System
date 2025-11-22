import sqlite3
from datetime import datetime
import os
import hashlib
class DatabaseManager:
    def __init__(self, db_name="stock_management.db"):
        # Get AppData folder (Windows) or ~/.local/share (Linux/macOS)
        appdata_dir = os.getenv("APPDATA") or os.path.expanduser("~/.local/share")

        # Make a subfolder for your app inside AppData
        db_dir = os.path.join(appdata_dir, "StockManager")
        os.makedirs(db_dir, exist_ok=True)

        # Final DB path
        db_path = os.path.join(db_dir, db_name)

        # Connect to SQLite
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")

        # Create tables only if they don't exist
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()

        # Company Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS company (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        total_sales REAL DEFAULT 0,
        total_profit REAL DEFAULT 0
        )
        """)

        # Enhanced Customers Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL DEFAULT 'guest',
        phone TEXT,
        address TEXT,
        customer_type TEXT DEFAULT 'walk_in',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        notes TEXT
        )
        """)

        # Products Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        brand TEXT,
        status TEXT DEFAULT 'active',
        deactivated_at TEXT,
        deactivated_reason TEXT
        );
        """)

        # Categories Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
        )
        """)

        # Product Variants Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_variants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        purchase_price REAL NOT NULL,
        selling_price REAL NOT NULL,
        image_path TEXT,
        status TEXT DEFAULT 'active',
        deactivated_at TEXT,
        deactivated_reason TEXT,
        stock_quantity INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (category_id) REFERENCES categories(id),
        UNIQUE(product_id, category_id)
        );
        """)

        # Enhanced Sales Table with Payment Tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            status TEXT NOT NULL DEFAULT 'draft',
            sale_date TEXT,
            
            total_amount REAL NOT NULL DEFAULT 0,
            amount_paid REAL NOT NULL DEFAULT 0,
            balance_due REAL NOT NULL DEFAULT 0,
            payment_method TEXT DEFAULT 'cash',
            payment_status TEXT NOT NULL DEFAULT 'pending',
            due_date TEXT,
            
            total_profit REAL NOT NULL DEFAULT 0,
            discount_amount REAL DEFAULT 0,
            notes TEXT,
            
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
        """)

        # Payment History Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payment_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            payment_amount REAL NOT NULL,
            payment_method TEXT NOT NULL DEFAULT 'cash',
            payment_date TEXT DEFAULT CURRENT_TIMESTAMP,
            received_by TEXT,
            notes TEXT,
            FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE
        )
        """)

        # Sale Items Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER NOT NULL,
        product_variant_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        unit_cost REAL NOT NULL,
        line_total REAL NOT NULL,
        line_profit REAL NOT NULL,
        discount_per_item REAL DEFAULT 0,
        FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
        FOREIGN KEY (product_variant_id) REFERENCES product_variants(id)
        )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_status ON sales(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_payment_status ON sales(payment_status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(customer_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_payment_history_sale ON payment_history(sale_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_customers_type ON customers(customer_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_status ON products(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_variants_status ON product_variants(status)")

        self.conn.commit()

    # ============== PRODUCT METHODS ==============
    
    def save_base_product(self, name, description=None, brand="Local"):
        """Save just the base product info, return product_id"""
        cursor = self.conn.cursor()
        if not brand:
            brand = "Local"

        cursor.execute("""
            INSERT INTO products (name, description, brand) 
            VALUES (?, ?, ?)
        """, (name, description, brand))
        product_id = cursor.lastrowid
        self.conn.commit()
        return product_id

    def save_product_variant(self, product_id, category_name, purchase_price, 
                            selling_price, stock_quantity, image_path=None):
        """Save a variant for an existing product"""
        cursor = self.conn.cursor()
        
        # Insert/get category
        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category_name,))
        cursor.execute("SELECT id FROM categories WHERE name=?", (category_name,))
        category_id = cursor.fetchone()[0]

        # Insert product variant
        cursor.execute("""
            INSERT INTO product_variants 
            (product_id, category_id, purchase_price, selling_price, image_path, stock_quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (product_id, category_id, purchase_price, selling_price, image_path, stock_quantity))
        
        self.conn.commit()
        return cursor.lastrowid

    def insert_company_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO company (name) VALUES (?)", (name,))
        self.conn.commit()

    def get_company_name(self):
        """Get company name from database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM company LIMIT 1")
        result = cursor.fetchone()
        return result[0] if result else None

    def get_overall_stats(self):
        """Get overall business statistics (all time)"""
        cursor = self.conn.cursor()
        
        # Total sales count
        cursor.execute("SELECT COUNT(*) FROM sales WHERE status = 'completed'")
        total_sales = cursor.fetchone()[0]
        
        # Total profit
        cursor.execute("SELECT COALESCE(SUM(total_profit), 0) FROM sales WHERE status = 'completed'")
        total_profit = cursor.fetchone()[0]
        
        # Total customers
        cursor.execute("SELECT COUNT(DISTINCT id) FROM customers")
        total_customers = cursor.fetchone()[0]
        
        # Total pending payments
        cursor.execute("""
            SELECT COALESCE(SUM(balance_due), 0) 
            FROM sales 
            WHERE status = 'completed' AND payment_status != 'paid_full'
        """)
        pending_payments = cursor.fetchone()[0]
        
        return total_sales, total_profit, total_customers, pending_payments

    def get_filtered_stats(self, start_date, end_date):
        """Get statistics for a specific date range"""
        cursor = self.conn.cursor()
        
        # Sales count in period
        cursor.execute("""
            SELECT COUNT(*) FROM sales 
            WHERE status = 'completed' 
            AND date(sale_date) BETWEEN ? AND ?
        """, (start_date, end_date))
        sales_count = cursor.fetchone()[0]
        
        # Revenue in period
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0) FROM sales 
            WHERE status = 'completed' 
            AND date(sale_date) BETWEEN ? AND ?
        """, (start_date, end_date))
        revenue = cursor.fetchone()[0]
        
        # Profit in period
        cursor.execute("""
            SELECT COALESCE(SUM(total_profit), 0) FROM sales 
            WHERE status = 'completed' 
            AND date(sale_date) BETWEEN ? AND ?
        """, (start_date, end_date))
        profit = cursor.fetchone()[0]
        
        # New customers in period
        cursor.execute("""
            SELECT COUNT(DISTINCT customer_id) FROM sales 
            WHERE status = 'completed' 
            AND customer_id IS NOT NULL
            AND date(sale_date) BETWEEN ? AND ?
        """, (start_date, end_date))
        customers = cursor.fetchone()[0]
        
        return sales_count, revenue, profit, customers

    def get_variant_by_id(self, variant_id: int):
        """Fetch full product + variant details by variant_id"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                p.id as product_id,
                p.name as product_name,
                p.description as product_description,
                p.brand as product_brand,
                c.name as category_name,
                pv.purchase_price,
                pv.selling_price,
                pv.stock_quantity,
                pv.image_path,
                pv.id as variant_id,
                COALESCE(pv.status, 'active') as variant_status,
                pv.deactivated_reason
            FROM product_variants pv
            JOIN products p ON pv.product_id = p.id
            JOIN categories c ON pv.category_id = c.id
            WHERE pv.id = ?
        """, (variant_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
    
        return {
            "product_id": row[0],
            "name": row[1],
            "description": row[2],
            "brand": row[3],
            "category": row[4],
            "purchase_price": row[5],
            "selling_price": row[6],
            "stock": row[7],
            "image_path": row[8],
            "variant_id": row[9],
            "status": row[10],
            "deactivated_reason": row[11],
        }

    def get_all_products_for_display(self):
        """Get all products with their variants including status info"""
        cursor = self.conn.cursor()
    
        cursor.execute("""
            SELECT 
                p.id as product_id,
                p.name as product_name,
                p.description as product_description,
                p.brand as product_brand,
                c.name as category_name,
                pv.purchase_price,
                pv.selling_price,
                pv.stock_quantity,
                pv.image_path,
                pv.id as variant_id,
                COALESCE(pv.status, 'active') as variant_status,
                pv.deactivated_reason
            FROM products p
            JOIN product_variants pv ON p.id = pv.product_id
            JOIN categories c ON pv.category_id = c.id
            ORDER BY p.name, c.name
        """)
    
        return cursor.fetchall()

    def save_edited_products(self,name, brand,category, description, purchase_price, selling_price, stock_quantity, image_path=None, variant_id=None):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE products
            SET name = ?,
                brand = ?,
                description = ?
            WHERE id = (SELECT product_id FROM product_variants WHERE id = ?)
        """, (name, brand, description, variant_id))

        cursor.execute("""UPDATE categories
            SET name = ?
            WHERE id = (SELECT category_id FROM product_variants WHERE id = ?)
        """, (category, variant_id))
        print("Updated category to =", category)
        
        cursor.execute("""
            UPDATE product_variants
            SET purchase_price = ?, selling_price = ?, stock_quantity = ?, image_path = ?
            WHERE id = ?
        """, (purchase_price, selling_price, stock_quantity, image_path, variant_id))
        self.conn.commit()

    def delete_variant(self, variant_id: int):
        cursor = self.conn.cursor()

        # Check if this variant is in any sale_items
        cursor.execute("""
            SELECT COUNT(*) as total_count,
                   SUM(CASE WHEN s.status = 'draft' THEN 1 ELSE 0 END) as cart_count,
                   SUM(CASE WHEN s.status = 'completed' THEN 1 ELSE 0 END) as sale_count
            FROM sale_items si
            JOIN sales s ON si.sale_id = s.id
            WHERE si.product_variant_id = ?
        """, (variant_id,))

        result = cursor.fetchone()
        total_count, cart_count, sale_count = result[0], result[1] or 0, result[2] or 0

        # Case 1: Product is in completed sales - can only be deactivated
        if sale_count > 0:
            cursor.execute("""
                UPDATE product_variants 
                SET status = 'inactive', 
                    deactivated_at = ?, 
                    deactivated_reason = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), 
                  "Product was part of sales history - cannot be deleted", 
                  variant_id))

            self.conn.commit()
            return False, "This product is linked to completed sales and can only be deactivated. It has been marked as inactive."

        # Case 2: Product is in cart (draft sales) - must be removed from cart first
        if cart_count > 0:
            return False, "This product is currently in the cart. Remove it from cart first before deleting."

        # Case 3: Product is safe to delete (not in any sales or cart)
        if total_count == 0:
            # Find product_id and category_id of this variant
            cursor.execute("SELECT product_id, category_id FROM product_variants WHERE id = ?", (variant_id,))
            row = cursor.fetchone()
            if not row:
                return False, "Variant not found"
            product_id, category_id = row

            # Delete the variant
            cursor.execute("DELETE FROM product_variants WHERE id = ?", (variant_id,))

            # Check if product has variants left
            cursor.execute("SELECT COUNT(*) FROM product_variants WHERE product_id = ?", (product_id,))
            remaining_variants = cursor.fetchone()[0]

            if remaining_variants < 1:
                cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

            # Check if category has variants left
            cursor.execute("SELECT COUNT(*) FROM product_variants WHERE category_id = ?", (category_id,))
            remaining_in_category = cursor.fetchone()[0]

            if remaining_in_category < 1:
                cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))

            self.conn.commit()
            return True, "Product deleted successfully"

        return False, "Unable to process delete request"

    def reactivate_variant(self, variant_id: int):
        """Reactivate a deactivated product variant"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            UPDATE product_variants 
            SET status = 'active', 
                deactivated_at = NULL, 
                deactivated_reason = NULL
            WHERE id = ?
        """, (variant_id,))
        
        if cursor.rowcount > 0:
            self.conn.commit()
            return True, "Product reactivated successfully"
        else:
            return False, "Variant not found"

    # ============== CART METHODS ==============
    
    def get_or_create_draft_sale(self):
        """Get existing draft sale or create a new one for cart"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT id FROM sales WHERE status = 'draft' LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            cursor.execute("""
                INSERT INTO sales (status, created_at, updated_at) 
                VALUES ('draft', ?, ?)
            """, (datetime.now().isoformat(), datetime.now().isoformat()))
            self.conn.commit()
            return cursor.lastrowid

    def add_to_cart(self, product_variant_id, quantity=1):
        """Add product to persistent cart"""
        cursor = self.conn.cursor()

        # Get product variant details including status
        cursor.execute("""
            SELECT pv.selling_price, pv.purchase_price, pv.stock_quantity,
                   COALESCE(pv.status, 'active') as status,
                   p.name, c.name as category_name
            FROM product_variants pv
            JOIN products p ON pv.product_id = p.id
            JOIN categories c ON pv.category_id = c.id
            WHERE pv.id = ?
        """, (product_variant_id,))

        variant_data = cursor.fetchone()
        if not variant_data:
            return False, "Product not found"

        selling_price, purchase_price, stock_quantity, status, product_name, category_name = variant_data

        # Check if product is active
        if status != 'active':
            return False, f"Product '{product_name} - {category_name}' is no longer available"

        # Check stock
        if quantity > stock_quantity:
            return False, f"Insufficient stock. Available: {stock_quantity}"

        # Get or create draft sale
        sale_id = self.get_or_create_draft_sale()

        # Check if item already exists in cart
        cursor.execute("""
            SELECT id, quantity FROM sale_items 
            WHERE sale_id = ? AND product_variant_id = ?
        """, (sale_id, product_variant_id))

        existing_item = cursor.fetchone()

        if existing_item:
            # Update existing item
            new_quantity = existing_item[1] + quantity
            if new_quantity > stock_quantity:
                return False, f"Total quantity would exceed stock. Available: {stock_quantity}"

            line_total = new_quantity * selling_price
            line_profit = (selling_price - purchase_price) * new_quantity

            cursor.execute("""
                UPDATE sale_items 
                SET quantity = ?, line_total = ?, line_profit = ?
                WHERE id = ?
            """, (new_quantity, line_total, line_profit, existing_item[0]))
        else:
            # Add new item
            line_total = quantity * selling_price
            line_profit = (selling_price - purchase_price) * quantity

            cursor.execute("""
                INSERT INTO sale_items 
                (sale_id, product_variant_id, quantity, unit_price, unit_cost, line_total, line_profit)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (sale_id, product_variant_id, quantity, selling_price, purchase_price, line_total, line_profit))

        # Update sale totals
        self.update_sale_totals(sale_id)
        self.conn.commit()
        return True, "Item added to cart successfully"

    def get_cart_items(self):
        """Get all items in the persistent cart"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT id FROM sales WHERE status = 'draft' LIMIT 1")
        result = cursor.fetchone()
        
        if not result:
            return []
        
        sale_id = result[0]
        
        cursor.execute("""
            SELECT 
                si.id as item_id,
                si.quantity,
                si.unit_price,
                si.line_total,
                si.line_profit,
                p.name as product_name,
                c.name as category_name,
                pv.image_path,
                pv.id as variant_id,
                pv.stock_quantity
            FROM sale_items si
            JOIN product_variants pv ON si.product_variant_id = pv.id
            JOIN products p ON pv.product_id = p.id
            JOIN categories c ON pv.category_id = c.id
            WHERE si.sale_id = ?
            ORDER BY p.name
        """, (sale_id,))
        
        return cursor.fetchall()

    def update_cart_item_quantity(self, item_id, new_quantity):
        """Update quantity of item in cart"""
        cursor = self.conn.cursor()
        
        if new_quantity <= 0:
            return self.remove_from_cart(item_id)
        
        # Get item details
        cursor.execute("""
            SELECT si.sale_id, si.product_variant_id, si.unit_price, si.unit_cost,
                   pv.stock_quantity
            FROM sale_items si
            JOIN product_variants pv ON si.product_variant_id = pv.id
            WHERE si.id = ?
        """, (item_id,))
        
        result = cursor.fetchone()
        if not result:
            return False, "Item not found"
        
        sale_id, variant_id, unit_price, unit_cost, stock_quantity = result
        
        # Check stock
        if new_quantity > stock_quantity:
            return False, f"Insufficient stock. Available: {stock_quantity}"
        
        # Update item
        line_total = new_quantity * unit_price
        line_profit = (unit_price - unit_cost) * new_quantity
        
        cursor.execute("""
            UPDATE sale_items 
            SET quantity = ?, line_total = ?, line_profit = ?
            WHERE id = ?
        """, (new_quantity, line_total, line_profit, item_id))
        
        self.update_sale_totals(sale_id)
        self.conn.commit()
        return True, "Cart updated successfully"

    def remove_from_cart(self, item_id):
        """Remove item from cart"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT sale_id FROM sale_items WHERE id = ?", (item_id,))
        result = cursor.fetchone()
        
        if not result:
            return False, "Item not found"
        
        sale_id = result[0]
        
        cursor.execute("DELETE FROM sale_items WHERE id = ?", (item_id,))
        self.update_sale_totals(sale_id)
        self.conn.commit()
        return True, "Item removed from cart"

    def clear_cart(self):
        """Clear all items from cart"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT id FROM sales WHERE status = 'draft' LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            sale_id = result[0]
            cursor.execute("DELETE FROM sale_items WHERE sale_id = ?", (sale_id,))
            cursor.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
            self.conn.commit()
        
        return True, "Cart cleared"

    def update_sale_totals(self, sale_id):
        """Update total amount and profit for a sale"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT COALESCE(SUM(line_total), 0), COALESCE(SUM(line_profit), 0)
            FROM sale_items WHERE sale_id = ?
        """, (sale_id,))
        
        total_amount, total_profit = cursor.fetchone()
        
        cursor.execute("""
            UPDATE sales 
            SET total_amount = ?, total_profit = ?, updated_at = ?
            WHERE id = ?
        """, (total_amount, total_profit, datetime.now().isoformat(), sale_id))

    # ============== CUSTOMER METHODS ==============
    
    def save_customer_enhanced(self, name="guest", phone=None, address=None, customer_type='walk_in', notes=None):
        """Enhanced customer saving"""
        cursor = self.conn.cursor()
        
        # Check if customer already exists by phone
        if phone:
            cursor.execute("SELECT id FROM customers WHERE phone = ?", (phone,))
            existing = cursor.fetchone()
            if existing:
                return existing[0]
        
        cursor.execute("""
            INSERT INTO customers (name, phone, address, customer_type, notes, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, phone, address, customer_type, notes, datetime.now().isoformat()))
        
        self.conn.commit()
        return cursor.lastrowid

    # ============== SALES COMPLETION METHODS ==============
    
    def complete_sale_enhanced(self, sale_data):
        """Complete sale with full payment tracking"""
        cursor = self.conn.cursor()
        
        # Get draft sale
        cursor.execute("SELECT id, total_amount FROM sales WHERE status = 'draft' LIMIT 1")
        result = cursor.fetchone()
        
        if not result:
            return False, "No items in cart"
        
        sale_id, total_amount = result
        
        # Check if cart has items
        cursor.execute("SELECT COUNT(*) FROM sale_items WHERE sale_id = ?", (sale_id,))
        if cursor.fetchone()[0] == 0:
            return False, "No items in cart"
        
        # Save/get customer
        customer_id = None
        if sale_data.get('customer_name', 'guest').strip() or 'guest':
            customer_id = self.save_customer_enhanced(
                name=sale_data.get('customer_name', 'guest').strip() or 'guest',
                phone=sale_data.get('customer_phone'),
                customer_type=sale_data.get('customer_type', 'walk_in').lower().replace(' ', '_').replace('/', '_'),
                notes=f"Added during sale #{sale_id}"
            )
        
        # Calculate payment details
        amount_paid = sale_data.get('amount_paid', 0)
        balance_due = total_amount - amount_paid
        
        # Determine payment status
        if balance_due <= 0:
            payment_status = 'paid_full'
        elif amount_paid == 0:
            payment_status = 'pending'
        else:
            payment_status = 'partial'
        
        # Update sale with enhanced payment info
        cursor.execute("""
            UPDATE sales 
            SET status = 'completed',
                customer_id = ?,
                sale_date = ?,
                amount_paid = ?,
                balance_due = ?,
                payment_method = ?,
                payment_status = ?,
                due_date = ?,
                notes = ?,
                updated_at = ?
            WHERE id = ?
        """, (
            customer_id,
            sale_data['sale_date'].isoformat(),
            amount_paid,
            balance_due,
            sale_data['payment_method'].lower().replace(' ', '_'),
            payment_status,
            sale_data['due_date'].isoformat() if sale_data['due_date'] else None,
            sale_data['notes'],
            datetime.now().isoformat(),
            sale_id
        ))
        
        # Record initial payment if any
        if amount_paid > 0:
            cursor.execute("""
                INSERT INTO payment_history (sale_id, payment_amount, payment_method, notes)
                VALUES (?, ?, ?, ?)
            """, (sale_id, amount_paid, sale_data.get('payment_method', 'cash'), "Initial payment during sale"))
        
        # Update stock quantities
        cursor.execute("SELECT product_variant_id, quantity FROM sale_items WHERE sale_id = ?", (sale_id,))
        for variant_id, quantity in cursor.fetchall():
            cursor.execute("""
                UPDATE product_variants 
                SET stock_quantity = stock_quantity - ?
                WHERE id = ?
            """, (quantity, variant_id))
        
        # Update company totals
        cursor.execute("SELECT COUNT(*) FROM sales WHERE status = 'completed'")
        sales_count = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(total_profit), 0) FROM sales WHERE status = 'completed'")
        total_profit = cursor.fetchone()[0]

        cursor.execute("""
            UPDATE company 
            SET total_sales = ?, total_profit = ?
        """, (sales_count, total_profit))

        self.conn.commit()
        return True, f"Sale completed successfully. Sale ID: {sale_id}"
    
    

    # ============== REPORTING METHODS ==============
    
    def get_customers_with_payment_status(self):
        """Get customers with their payment status and outstanding amounts"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                c.id, c.name, c.phone, c.customer_type, c.notes, 
                s.id as sale_id, s.payment_status, s.total_amount, 
                s.amount_paid, s.balance_due, s.due_date, s.created_at
            FROM customers c 
            JOIN sales s ON c.id = s.customer_id
            WHERE s.status = 'completed'
            ORDER BY s.created_at DESC
        """)

        result = cursor.fetchall()
        
        sale_id = result[0][5] if result else None
        
        #get the name of items the customer bought with categories
        cursor.execute("""
            SELECT 
                p.name as product_name, c.name as category_name, pv.selling_price, si.quantity
            FROM sale_items si
            JOIN product_variants pv ON si.product_variant_id = pv.id
            JOIN products p ON pv.product_id = p.id
            JOIN categories c ON pv.category_id = c.id
            WHERE si.sale_id = ?
        """, (sale_id,))
        item_names = cursor.fetchall()
        

        customers = []
        for row in result:
            customer = {
                "id": row[0],
                "name": row[1],
                "phone": row[2],
                "customer_type": row[3],
                "notes": row[4],
                "sale_id": row[5],
                "payment_status": row[6],
                "total_amount": row[7],
                "amount_paid": row[8],
                "balance_due": row[9],
                "due_date": row[10],
                "created_at": row[11],
                "items_purchased": item_names
            }
            customers.append(customer)
        return customers
    
    def process_partial_payment(self, sale_id, payment_amount, payment_method='cash', notes=None):
        """Process a partial payment for an existing sale"""
        cursor = self.conn.cursor()
        
        try:
            # Get current sale information
            cursor.execute("""
                SELECT total_amount, amount_paid, balance_due, payment_status
                FROM sales 
                WHERE id = ? AND status = 'completed'
            """, (sale_id,))
            
            sale_info = cursor.fetchone()
            if not sale_info:
                return False, "Sale not found or not completed"
            
            total_amount, current_paid, current_balance, current_status = sale_info
            
            # Validate payment amount
            if payment_amount <= 0:
                return False, "Payment amount must be greater than 0"
            
            if payment_amount > current_balance:
                return False, f"Payment amount cannot exceed outstanding balance of PKR {current_balance:,.2f}"
            
            # Calculate new amounts
            new_amount_paid = current_paid + payment_amount
            new_balance_due = total_amount - new_amount_paid
            
            # Determine new payment status
            if new_balance_due <= 0:
                new_payment_status = 'paid_full'
            elif new_amount_paid > 0 and new_balance_due > 0:
                new_payment_status = 'partial'
            else:
                new_payment_status = 'pending'
            
            # Update sales table
            if new_payment_status == 'paid_full':
                # Clear due date when fully paid
                cursor.execute("""
                    UPDATE sales 
                    SET amount_paid = ?, 
                        balance_due = ?, 
                        payment_status = ?,
                        due_date = NULL,
                        updated_at = ?
                    WHERE id = ?
                """, (new_amount_paid, new_balance_due, new_payment_status, 
                      datetime.now().isoformat(), sale_id))
            else:
                # Keep due date for partial payments
                cursor.execute("""
                    UPDATE sales 
                    SET amount_paid = ?, 
                        balance_due = ?, 
                        payment_status = ?,
                        updated_at = ?
                    WHERE id = ?
                """, (new_amount_paid, new_balance_due, new_payment_status, 
                      datetime.now().isoformat(), sale_id))
            
            # Record payment in payment history
            cursor.execute("""
                INSERT INTO payment_history 
                (sale_id, payment_amount, payment_method, payment_date, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (sale_id, payment_amount, payment_method, 
                  datetime.now().isoformat(), notes or f"Partial payment of PKR {payment_amount:,.2f}"))
            
            self.conn.commit()
            
            return True, f"Payment of PKR {payment_amount:,.2f} processed successfully. New balance: PKR {new_balance_due:,.2f}"
            
        except Exception as e:
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def get_sales_report(self, start_date=None, end_date=None, status=None):
        """Get sales report with filters"""
        cursor = self.conn.cursor()
        
        query = """
            SELECT 
                s.id, s.sale_date, s.status, s.payment_status,
                s.total_amount, s.total_profit,
                c.name as customer_name, s.notes
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.id
            WHERE s.status != 'draft'
        """
        
        params = []
        if start_date:
            query += " AND date(s.sale_date) >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date(s.sale_date) <= ?"
            params.append(end_date)
        if status:
            query += " AND s.status = ?"
            params.append(status)
        
        query += " ORDER BY s.sale_date DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()

    def get_sale_details(self, sale_id):
        """Get detailed information about a specific sale"""
        cursor = self.conn.cursor()
        
        # Get sale info
        cursor.execute("""
            SELECT 
                s.id, s.sale_date, s.status, s.payment_status, 
                s.total_amount, s.total_profit, s.notes,
                c.name as customer_name, c.phone, c.address
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.id
            WHERE s.id = ?
        """, (sale_id,))
        
        sale_info = cursor.fetchone()
        
        # Get sale items
        cursor.execute("""
            SELECT 
                p.name as product_name,
                cat.name as category_name,
                si.quantity,
                si.unit_price,
                si.line_total,
                si.line_profit
            FROM sale_items si
            JOIN product_variants pv ON si.product_variant_id = pv.id
            JOIN products p ON pv.product_id = p.id
            JOIN categories cat ON pv.category_id = cat.id
            WHERE si.sale_id = ?
        """, (sale_id,))
        
        sale_items = cursor.fetchall()
        
        return sale_info, sale_items
    # Add this method to your DatabaseManager class in database_manager.py

    def get_inventory_stats(self):
        """Get inventory statistics: total items, budget spent, expected revenue, potential profit"""
        cursor = self.conn.cursor()
        
        # Get total stock quantity across all active variants
        cursor.execute("""
            SELECT COALESCE(SUM(stock_quantity), 0)
            FROM product_variants
            WHERE status = 'active'
        """)
        total_items = cursor.fetchone()[0]
        
        # Get total budget spent (purchase_price * stock_quantity)
        cursor.execute("""
            SELECT COALESCE(SUM(purchase_price * stock_quantity), 0)
            FROM product_variants
            WHERE status = 'active'
        """)
        total_budget = cursor.fetchone()[0]
        
        # Get expected revenue (selling_price * stock_quantity)
        cursor.execute("""
            SELECT COALESCE(SUM(selling_price * stock_quantity), 0)
            FROM product_variants
            WHERE status = 'active'
        """)
        expected_revenue = cursor.fetchone()[0]
        
        # Calculate potential profit
        potential_profit = expected_revenue - total_budget
        
        return total_items, total_budget, expected_revenue, potential_profit



# Add these methods to the DatabaseManager class:

    def create_password_table(self):
        """Create password table if it doesn't exist - safe to run on existing database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_password (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def set_password(self, password):
        """Set or update the app password"""
        cursor = self.conn.cursor()
        password_hash = self.hash_password(password)
        
        cursor.execute("""
            INSERT OR REPLACE INTO app_password (id, password_hash, updated_at)
            VALUES (1, ?, ?)
        """, (password_hash, datetime.now().isoformat()))
        
        self.conn.commit()
        return True
    
    def verify_password(self, password):
        """Verify if the entered password is correct"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT password_hash FROM app_password WHERE id = 1")
        result = cursor.fetchone()
        
        if not result:
            return False
        
        stored_hash = result[0]
        entered_hash = self.hash_password(password)
        
        return stored_hash == entered_hash
    
    def has_password(self):
        """Check if a password has been set"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM app_password WHERE id = 1")
        return cursor.fetchone()[0] > 0
    
    def change_password(self, old_password, new_password):
        """Change password after verifying old password"""
        if not self.verify_password(old_password):
            return False, "Current password is incorrect"
        
        self.set_password(new_password)
        return True, "Password changed successfully"

if __name__ == "__main__":
    db = DatabaseManager()
    print("Enhanced database with full payment tracking created successfully!")