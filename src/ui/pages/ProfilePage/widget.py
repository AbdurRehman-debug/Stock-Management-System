from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel, 
                             QPushButton, QFrame, QScrollArea, QHBoxLayout, 
                             QMessageBox, QLineEdit, QComboBox, QGridLayout, 
                             QProgressBar)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from ....database.database_manager import DatabaseManager
import datetime


class DashboardPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.setup_ui()
        self.load_data()
        self.setup_auto_refresh()
        
    def setup_ui(self):
        """Setup the main dashboard UI with scroll area"""
        self.setWindowTitle("Business Dashboard")
        self.setMinimumSize(800, 600)
        
        # Create main scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #2c3e50;
            }
            QScrollBar:vertical {
                background-color: #34495e;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #7f8c8d;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #95a5a6;
            }
        """)
        
        # Create scrollable content widget
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #2c3e50;")
        
        # Main layout for scrollable content
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Company header (always visible)
        self.setup_company_header(layout)
        
        # Overall stats (always visible)
        self.setup_overall_stats(layout)
        
        # NEW: Inventory stats section
        self.setup_inventory_stats(layout)
        
        # Filter section
        self.setup_filters(layout)
        
        # Filtered stats
        self.setup_filtered_stats(layout)
        
        # Add stretch to push content to top
        layout.addStretch()
        
        # Set the content widget to scroll area
        scroll_area.setWidget(content_widget)
        
        # Set scroll area as central widget
        self.setCentralWidget(scroll_area)
        
    def setup_company_header(self, parent_layout):
        """Setup company name header"""
        header_frame = QFrame()
        header_frame.setFixedHeight(200)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(header_frame)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.company_name_label = QLabel("Loading Company...")
        self.company_name_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: white;
                text-align: center;
            }
        """)
        self.company_name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.company_name_label)
        
        parent_layout.addWidget(header_frame)
        
    def setup_overall_stats(self, parent_layout):
        """Setup overall business stats (always visible)"""
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(stats_frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("Overall Business Statistics")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Stats grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        # Create stat cards
        self.total_sales_card = self.create_stat_card("Total Sales", "0", "#e74c3c")
        self.total_profit_card = self.create_stat_card("Total Profit", "PKR 0", "#27ae60")
        self.total_customers_card = self.create_stat_card("Total Customers", "0", "#3498db")
        self.pending_payments_card = self.create_stat_card("Pending Payments", "PKR 0", "#f39c12")
        
        stats_grid.addWidget(self.total_sales_card, 0, 0)
        stats_grid.addWidget(self.total_profit_card, 0, 1)
        stats_grid.addWidget(self.total_customers_card, 1, 0)
        stats_grid.addWidget(self.pending_payments_card, 1, 1)
        
        layout.addLayout(stats_grid)
        parent_layout.addWidget(stats_frame)
    
    def setup_inventory_stats(self, parent_layout):
        """Setup inventory statistics section"""
        inventory_frame = QFrame()
        inventory_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(inventory_frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("Inventory Overview")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: bold; margin-bottom: 15px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Inventory stats grid
        inventory_grid = QGridLayout()
        inventory_grid.setSpacing(15)
        
        # Create inventory stat cards
        self.total_items_card = self.create_stat_card("Total Items in Stock", "0", "#9b59b6")
        self.total_budget_card = self.create_stat_card("Total Budget Spent", "PKR 0", "#e67e22")
        self.expected_revenue_card = self.create_stat_card("Expected Revenue", "PKR 0", "#1abc9c")
        self.potential_profit_card = self.create_stat_card("Potential Profit", "PKR 0", "#16a085")
        
        inventory_grid.addWidget(self.total_items_card, 0, 0)
        inventory_grid.addWidget(self.total_budget_card, 0, 1)
        inventory_grid.addWidget(self.expected_revenue_card, 1, 0)
        inventory_grid.addWidget(self.potential_profit_card, 1, 1)
        
        layout.addLayout(inventory_grid)
        parent_layout.addWidget(inventory_frame)
        
    def create_stat_card(self, title, value, color):
        """Create a simple stat card"""
        card = QFrame()
        card.setMinimumHeight(20)
        card.setMaximumHeight(200)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #2c3e50;
                border-radius: 10px;
                border-left: 5px solid {color};
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #bdc3c7; font-size: 14px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setObjectName("value_label")
        value_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return card
        
    def setup_filters(self, parent_layout):
        """Setup simple time filters"""
        filter_frame = QFrame()
        filter_frame.setFixedHeight(200)
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 12px;
                padding: 15px;
            }
            QComboBox {
                background-color: #2c3e50;
                border: 2px solid #7f8c8d;
                border-radius: 6px;
                padding: 8px 12px;
                color: white;
                font-size: 14px;
                min-width: 150px;
            }
            QComboBox:focus {
                border: 2px solid #3498db;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                width: 0;
                height: 0;
            }
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
        """)
        
        layout = QHBoxLayout(filter_frame)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        filter_label = QLabel("View Statistics For:")
        self.period_filter = QComboBox()
        self.period_filter.addItems([
            "Today", "Yesterday", "This Week", "Previous Week", 
            "This Month", "Previous Month"
        ])
        self.period_filter.setCurrentText("This Month")
        self.period_filter.currentTextChanged.connect(self.apply_filter)
        
        layout.addWidget(filter_label)
        layout.addWidget(self.period_filter)
        layout.addStretch()
        
        parent_layout.addWidget(filter_frame)
        
    def setup_filtered_stats(self, parent_layout):
        """Setup filtered statistics section"""
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(stats_frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.filtered_title = QLabel("This Month Statistics")
        self.filtered_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        self.filtered_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.filtered_title)
        
        # Filtered stats grid
        filtered_grid = QGridLayout()
        filtered_grid.setSpacing(20)
        
        self.filtered_sales_card = self.create_stat_card("Sales", "0", "#9b59b6")
        self.filtered_revenue_card = self.create_stat_card("Revenue", "PKR 0", "#e67e22")
        self.filtered_profit_card = self.create_stat_card("Profit", "PKR 0", "#1abc9c")
        self.filtered_customers_card = self.create_stat_card("New Customers", "0", "#16a085")
        
        filtered_grid.addWidget(self.filtered_sales_card, 0, 0)
        filtered_grid.addWidget(self.filtered_revenue_card, 0, 1)
        filtered_grid.addWidget(self.filtered_profit_card, 1, 0)
        filtered_grid.addWidget(self.filtered_customers_card, 1, 1)
        
        layout.addLayout(filtered_grid)
        parent_layout.addWidget(stats_frame)
        
    def get_date_range(self):
        """Get date range for selected period"""
        period = self.period_filter.currentText()
        today = datetime.date.today()
        
        if period == "Today":
            return today, today
        elif period == "Yesterday":
            yesterday = today - datetime.timedelta(days=1)
            return yesterday, yesterday
        elif period == "This Week":
            days_since_monday = today.weekday()
            start_of_week = today - datetime.timedelta(days=days_since_monday)
            return start_of_week, today
        elif period == "Previous Week":
            days_since_monday = today.weekday()
            start_of_last_week = today - datetime.timedelta(days=days_since_monday + 7)
            end_of_last_week = start_of_last_week + datetime.timedelta(days=6)
            return start_of_last_week, end_of_last_week
        elif period == "This Month":
            start_of_month = today.replace(day=1)
            return start_of_month, today
        elif period == "Previous Month":
            first_of_this_month = today.replace(day=1)
            last_month_end = first_of_this_month - datetime.timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            return last_month_start, last_month_end
        
        return today, today
        
    def apply_filter(self):
        """Apply the selected filter"""
        try:
            period = self.period_filter.currentText()
            self.filtered_title.setText(f"{period} Statistics")
            
            start_date, end_date = self.get_date_range()
            
            # Get filtered stats
            filtered_stats = self.db_manager.get_filtered_stats(
                start_date.isoformat(), 
                end_date.isoformat()
            )
            
            if filtered_stats:
                sales_count, revenue, profit, customers = filtered_stats
                
                # Update filtered cards with proper error handling
                sales_label = self.filtered_sales_card.findChild(QLabel, "value_label")
                if sales_label:
                    sales_label.setText(str(sales_count))
                
                revenue_label = self.filtered_revenue_card.findChild(QLabel, "value_label")
                if revenue_label:
                    revenue_label.setText(f"PKR {revenue:,.2f}")
                
                profit_label = self.filtered_profit_card.findChild(QLabel, "value_label")
                if profit_label:
                    profit_label.setText(f"PKR {profit:,.2f}")
                
                customers_label = self.filtered_customers_card.findChild(QLabel, "value_label")
                if customers_label:
                    customers_label.setText(str(customers))
            else:
                # Set default values if no data
                self.filtered_sales_card.findChild(QLabel, "value_label").setText("0")
                self.filtered_revenue_card.findChild(QLabel, "value_label").setText("PKR 0")
                self.filtered_profit_card.findChild(QLabel, "value_label").setText("PKR 0")
                self.filtered_customers_card.findChild(QLabel, "value_label").setText("0")
                
        except Exception as e:
            print(f"Error applying filter: {e}")
    
    def load_inventory_stats(self):
        """Load inventory statistics"""
        try:
            inventory_stats = self.db_manager.get_inventory_stats()
            
            if inventory_stats:
                total_items, total_budget, expected_revenue, potential_profit = inventory_stats
                
                # Update inventory cards
                items_label = self.total_items_card.findChild(QLabel, "value_label")
                if items_label:
                    items_label.setText(str(total_items))
                
                budget_label = self.total_budget_card.findChild(QLabel, "value_label")
                if budget_label:
                    budget_label.setText(f"PKR {total_budget:,.2f}")
                
                revenue_label = self.expected_revenue_card.findChild(QLabel, "value_label")
                if revenue_label:
                    revenue_label.setText(f"PKR {expected_revenue:,.2f}")
                
                profit_label = self.potential_profit_card.findChild(QLabel, "value_label")
                if profit_label:
                    profit_label.setText(f"PKR {potential_profit:,.2f}")
            else:
                # Set default values
                self.total_items_card.findChild(QLabel, "value_label").setText("0")
                self.total_budget_card.findChild(QLabel, "value_label").setText("PKR 0")
                self.expected_revenue_card.findChild(QLabel, "value_label").setText("PKR 0")
                self.potential_profit_card.findChild(QLabel, "value_label").setText("PKR 0")
                
        except Exception as e:
            print(f"Error loading inventory stats: {e}")
        
    def load_data(self):
        """Load all dashboard data"""
        try:
            # Load company name
            company_name = self.db_manager.get_company_name()
            if company_name:
                self.company_name_label.setText(company_name)
            else:
                self.company_name_label.setText("Your Business")
                
            # Load overall stats (always visible)
            overall_stats = self.db_manager.get_overall_stats()
            if overall_stats:
                total_sales, total_profit, total_customers, pending_payments = overall_stats
                
                # Update overall stats cards with proper error handling
                sales_label = self.total_sales_card.findChild(QLabel, "value_label")
                if sales_label:
                    sales_label.setText(str(total_sales))
                
                profit_label = self.total_profit_card.findChild(QLabel, "value_label")
                if profit_label:
                    profit_label.setText(f"PKR {total_profit:,.2f}")
                
                customers_label = self.total_customers_card.findChild(QLabel, "value_label")
                if customers_label:
                    customers_label.setText(str(total_customers))
                
                pending_label = self.pending_payments_card.findChild(QLabel, "value_label")
                if pending_label:
                    pending_label.setText(f"PKR {pending_payments:,.2f}")
            else:
                # Set default values if no data
                self.total_sales_card.findChild(QLabel, "value_label").setText("0")
                self.total_profit_card.findChild(QLabel, "value_label").setText("PKR 0")
                self.total_customers_card.findChild(QLabel, "value_label").setText("0")
                self.pending_payments_card.findChild(QLabel, "value_label").setText("PKR 0")
            
            # Load inventory stats
            self.load_inventory_stats()
            
            # Load filtered data
            self.apply_filter()
            
        except Exception as e:
            print(f"Error loading data: {e}")
            # Set default values on error
            self.company_name_label.setText("Your Business")
        
    def setup_auto_refresh(self):
        """Setup auto refresh every 5 seconds"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_data)
        self.refresh_timer.start(5000)  # 5 seconds

    def refresh_data(self):
        """Manual refresh method"""
        self.load_data()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = DashboardPage()
    window.show()
    sys.exit(app.exec())