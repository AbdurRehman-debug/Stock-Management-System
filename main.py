import sys
import os
from PySide6.QtWidgets import QStackedWidget,QMainWindow, QApplication
from PySide6.QtGui import QIcon
from src.ui.pages.welcomepage.widget import WelcomePage
from src.ui.pages.homePage.widget import HomePage
from src.ui.components.menubar import Navbar
from src.ui.pages.ProfilePage.widget import DashboardPage
from src.ui.pages.CustomersPage.widget import CustomersPage
from src.ui.pages.AddProductsPage.widget import AddProductsPage
from src.database.database_manager import DatabaseManager
from src.ui.pages.SalesPage.widget import SalesPage
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
        
        self.nav_bar = Navbar(self)
        self.addToolBar(self.nav_bar)
        self.nav_bar.hide()

        self.nav_bar.setMovable(False)
        self.nav_bar.setFloatable(False)

        # Create page instances
        self.welcome_page = WelcomePage()
        self.home_page = HomePage()
        self.profile_page = DashboardPage()
        self.customer_page = CustomersPage()
        self.add_products_page = AddProductsPage()
        self.sales_page = SalesPage()

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.welcome_page)  # index 0 
        self.stacked_widget.addWidget(self.home_page)     # index 1
        self.stacked_widget.addWidget(self.profile_page)  # index 2
        self.stacked_widget.addWidget(self.sales_page) # index 3
        self.stacked_widget.addWidget(self.add_products_page) # index 4
        self.stacked_widget.addWidget(self.customer_page)


        # Connect signals
        self.welcome_page.navigateToHome.connect(self.showHomePage)
        self.stacked_widget.setCurrentIndex(0)
        
        # UPDATED: Connect to page changes for auto-refresh
        self.stacked_widget.currentChanged.connect(self.on_page_changed)
        
        self.check_company_exists()
        
        # Navigation connections
        self.nav_bar.home.triggered.connect(lambda: self.switch_to_page(1))
        self.nav_bar.profile.triggered.connect(lambda: self.switch_to_page(2))
        self.nav_bar.sales.triggered.connect(lambda: self.switch_to_page(3))
        self.nav_bar.addProduct.triggered.connect(lambda: self.switch_to_page(4))
        self.nav_bar.customerspage.triggered.connect(lambda: self.switch_to_page(5))

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
        if index == 1:  # HomePage index
            print("Switching to HomePage - refreshing products...")
            self.home_page.refresh_products()

    def check_company_exists(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT 1 FROM company LIMIT 1")
        exists = cursor.fetchone()
        if exists:
            self.stacked_widget.setCurrentIndex(1)

    def showHomePage(self):
        self.stacked_widget.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Main_Window()
    window.show()
    sys.exit(app.exec())