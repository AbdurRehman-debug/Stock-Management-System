from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction



class Navbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Navigation", parent)

        
        self.home = QAction("Home", self)
        self.profile = QAction("Profile", self)
        self.sales = QAction("Sales", self)
        self.addProduct = QAction("Add Product", self)
        self.customerspage = QAction("Customers", self)
        

       
        self.addAction(self.home)
        self.addAction(self.profile)
        self.addAction(self.sales)
        self.addAction(self.addProduct)
        self.addAction(self.customerspage)
        

        self.setStyleSheet("""
            QToolBar {
                background-color: #003566;
            }
            QToolButton {
                font-size: 16px;
                font-weight: bold;
                padding: 6px 12px;
            }
            QToolButton:hover {
                background-color: #90E0EF;
                color: black;
            }
        """)



        # Example connections

