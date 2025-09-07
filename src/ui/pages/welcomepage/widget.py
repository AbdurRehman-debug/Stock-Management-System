from PySide6.QtWidgets import QWidget,QMessageBox
from PySide6.QtCore import QTimer, Signal  # Add Signal import
from .ui_widget import Ui_Form
from src.database.database_manager import DatabaseManager

class WelcomePage(QWidget, Ui_Form):
    
    navigateToHome = Signal()
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnCompany.clicked.connect(self.getCompanyName)
        self.db = DatabaseManager()

    def getCompanyName(self):
        company_name = self.companyname.text().strip()
        #insert in to databse
        if not company_name:
            QMessageBox.warning(self, "Input Error", "Please enter a valid company name.")
            return
        self.db.insert_company_name(company_name)
        self.label_welcome.setText(f"Welcome {company_name}")
        QTimer.singleShot(1000, self.navigateToHome_emit)  # Changed this line

    def navigateToHome_emit(self):  # Renamed to avoid confusion
        self.navigateToHome.emit()  # This emits the signal