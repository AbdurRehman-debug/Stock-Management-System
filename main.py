import sys
import os
from PySide6.QtWidgets import QStackedWidget, QMainWindow, QApplication
from PySide6.QtGui import QIcon
from src.ui.pages.welcomepage.widget import WelcomePage
from src.ui.pages.homePage.widget import HomePage
from src.ui.components.menubar import Navbar
from src.ui.pages.ProfilePage.widget import DashboardPage
from src.ui.pages.CustomersPage.widget import CustomersPage
from src.ui.pages.AddProductsPage.widget import AddProductsPage
from src.database.database_manager import DatabaseManager
from src.ui.pages.SalesPage.widget import SalesPage

# Import authentication screens
from src.ui.auth.login_screen import LoginScreen
from src.ui.auth.password_setup_screen import PasswordSetupScreen
from src.ui.auth.password_settings_page import PasswordSettingsPage


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StockPy")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "assets", "icons", "stock.png")
        self.setWindowIcon(QIcon(icon_path))
        
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.db = DatabaseManager()
        
        # IMPORTANT: Create password table (safe to run on existing database)
        self.db.create_password_table()
        
        self.nav_bar = Navbar(self)
        self.addToolBar(self.nav_bar)
        self.nav_bar.hide()
        self.nav_bar.setMovable(False)
        self.nav_bar.setFloatable(False)
        
        # Initialize pages as None - will be created after login
        self.welcome_page = None
        self.home_page = None
        self.profile_page = None
        self.customer_page = None
        self.add_products_page = None
        self.sales_page = None
        self.settings_page = None
        
        # Check if password exists and show appropriate screen
        if self.db.has_password():
            self.show_login_screen()
        else:
            self.show_password_setup_screen()
    
    def show_password_setup_screen(self):
        """Show password setup screen for first time users"""
        self.password_setup_screen = PasswordSetupScreen(self.db)
        self.password_setup_screen.password_set.connect(self.show_login_screen)
        self.stacked_widget.addWidget(self.password_setup_screen)
        self.stacked_widget.setCurrentWidget(self.password_setup_screen)
    
    def show_login_screen(self):
        """Show login screen"""
        # Clear password setup screen if it exists
        if hasattr(self, 'password_setup_screen'):
            self.stacked_widget.removeWidget(self.password_setup_screen)
            self.password_setup_screen.deleteLater()
        
        self.login_screen = LoginScreen(self.db)
        self.login_screen.login_successful.connect(self.initialize_main_app)
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.setCurrentWidget(self.login_screen)
    
    def initialize_main_app(self):
        """Initialize main application after successful login"""
        # Remove login screen
        self.stacked_widget.removeWidget(self.login_screen)
        self.login_screen.deleteLater()
        
        # Now create all the main pages
        self.welcome_page = WelcomePage()
        self.home_page = HomePage()
        self.profile_page = DashboardPage()
        self.customer_page = CustomersPage()
        self.add_products_page = AddProductsPage()
        self.sales_page = SalesPage()
        self.settings_page = PasswordSettingsPage(self.db)
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.welcome_page)  # index 0 
        self.stacked_widget.addWidget(self.home_page)     # index 1
        self.stacked_widget.addWidget(self.profile_page)  # index 2
        self.stacked_widget.addWidget(self.sales_page)    # index 3
        self.stacked_widget.addWidget(self.add_products_page) # index 4
        self.stacked_widget.addWidget(self.customer_page) # index 5
        self.stacked_widget.addWidget(self.settings_page) # index 6
        
        # Connect signals
        self.welcome_page.navigateToHome.connect(self.showHomePage)
        
        # Connect to page changes for auto-refresh
        self.stacked_widget.currentChanged.connect(self.on_page_changed)
        
        # Check if company exists and navigate accordingly
        self.check_company_exists()
        
        # Navigation connections
        self.nav_bar.home.triggered.connect(lambda: self.switch_to_page(1))
        self.nav_bar.profile.triggered.connect(lambda: self.switch_to_page(2))
        self.nav_bar.sales.triggered.connect(lambda: self.switch_to_page(3))
        self.nav_bar.addProduct.triggered.connect(lambda: self.switch_to_page(4))
        self.nav_bar.customerspage.triggered.connect(lambda: self.switch_to_page(5))
        self.nav_bar.settings.triggered.connect(lambda: self.switch_to_page(6))
    
    def switch_to_page(self, index):
        """Switch to a page by index"""
        self.stacked_widget.setCurrentIndex(index)
    
    def on_page_changed(self, index):
        """Called whenever the page changes"""
        # Handle navbar visibility
        if index == 0:
            self.nav_bar.hide()
        else:
            self.nav_bar.show()
        
        # AUTO-REFRESH: Refresh HomePage when navigating to it
        if index == 1 and self.home_page:  # HomePage index
            print("Switching to HomePage - refreshing products...")
            self.home_page.refresh_products()
    
    def check_company_exists(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT 1 FROM company LIMIT 1")
        exists = cursor.fetchone()
        if exists:
            self.stacked_widget.setCurrentIndex(1)
            self.nav_bar.show()
        else:
            self.stacked_widget.setCurrentIndex(0)
    
    def showHomePage(self):
        self.stacked_widget.setCurrentIndex(1)
        self.nav_bar.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Main_Window()
    window.show()
    sys.exit(app.exec())