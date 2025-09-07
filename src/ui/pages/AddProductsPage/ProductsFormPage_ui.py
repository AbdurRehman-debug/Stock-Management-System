# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProductsFormPage.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet(u"#very_basic_info,\n"
"#general_info,\n"
"#groupBox_3 {\n"
"    background-color: #00607A;\n"
"    border: 5px solid #d0dd0e;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"#img_btn,\n"
"#addCategoryBtn,\n"
"#saveproductbtn,#categories_img_btn {\n"
"    background-color: #007BFF;\n"
"    border: 2px solid #0056b3;\n"
"    border-radius: 5px;\n"
"    padding: 4px;\n"
"    color: white;\n"
"    margin:10px\n"
"}\n"
"\n"
"#img_btn:hover,\n"
"#addCategoryBtn:hover,\n"
"#saveproductbtn:hover,\n"
"#categories_img_btn:hover {\n"
"    background-color: #780057b3;\n"
"}\n"
"#dynamic_category {\n"
"    background-color: #ff413a3a;\n"
"    border: 4px solid #ffffff;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"    color: white;\n"
"    margin-bottom: 15px;\n"
"}\n"
"\n"
"#remove_category_btn {\n"
"    background-color: #ffb72c2c;\n"
"    border: 2px solid #000000;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    color: white;\n"
"    margin: 5px;\n"
"\n"
"}\n"
""
                        "QLineEdit,QTextEdit,QSpinBox,QDoubleSpinBox {\n"
"    font-size: 13px;\n"
"    border: 3px solid;\n"
"    padding: 4px;\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 768, 886))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(25)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.very_basic_info = QGroupBox(self.scrollAreaWidgetContents)
        self.very_basic_info.setObjectName(u"very_basic_info")
        self.very_basic_info.setMaximumSize(QSize(16777215, 400))
        font1 = QFont()
        font1.setBold(True)
        self.very_basic_info.setFont(font1)
        self.formLayout_2 = QFormLayout(self.very_basic_info)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_2 = QLabel(self.very_basic_info)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.base_name = QLineEdit(self.very_basic_info)
        self.base_name.setObjectName(u"base_name")
        self.base_name.setMaximumSize(QSize(500, 16777215))

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.base_name)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")

        self.formLayout_2.setLayout(6, QFormLayout.ItemRole.LabelRole, self.formLayout)

        self.brand = QLineEdit(self.very_basic_info)
        self.brand.setObjectName(u"brand")
        self.brand.setMaximumSize(QSize(500, 16777215))

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.brand)

        self.label_8 = QLabel(self.very_basic_info)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.label_3 = QLabel(self.very_basic_info)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.description = QTextEdit(self.very_basic_info)
        self.description.setObjectName(u"description")
        self.description.setMinimumSize(QSize(0, 180))
        self.description.setMaximumSize(QSize(500, 300))

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.description)


        self.verticalLayout_2.addWidget(self.very_basic_info)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.general_info = QGroupBox(self.scrollAreaWidgetContents)
        self.general_info.setObjectName(u"general_info")
        self.general_info.setMaximumSize(QSize(16777215, 200))
        self.general_info.setFont(font1)
        self.formLayout_4 = QFormLayout(self.general_info)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_4 = QLabel(self.general_info)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.purchaseprice = QDoubleSpinBox(self.general_info)
        self.purchaseprice.setObjectName(u"purchaseprice")
        self.purchaseprice.setMaximumSize(QSize(500, 16777215))
        self.purchaseprice.setMaximum(9999999.000000000000000)

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.FieldRole, self.purchaseprice)

        self.label_7 = QLabel(self.general_info)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.sellingprice = QDoubleSpinBox(self.general_info)
        self.sellingprice.setObjectName(u"sellingprice")
        self.sellingprice.setMaximumSize(QSize(500, 16777215))
        self.sellingprice.setMaximum(9999999.990000000223517)

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.FieldRole, self.sellingprice)

        self.label_5 = QLabel(self.general_info)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.stockquantity = QSpinBox(self.general_info)
        self.stockquantity.setObjectName(u"stockquantity")
        self.stockquantity.setMaximumSize(QSize(500, 16777215))
        self.stockquantity.setMaximum(1000000)

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.FieldRole, self.stockquantity)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")

        self.formLayout_4.setLayout(3, QFormLayout.ItemRole.LabelRole, self.formLayout_3)


        self.verticalLayout_2.addWidget(self.general_info)

        self.img_btn = QPushButton(self.scrollAreaWidgetContents)
        self.img_btn.setObjectName(u"img_btn")

        self.verticalLayout_2.addWidget(self.img_btn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.removegeneralimgBtn = QPushButton(self.scrollAreaWidgetContents)
        self.removegeneralimgBtn.setObjectName(u"removegeneralimgBtn")
        self.removegeneralimgBtn.setEnabled(True)

        self.verticalLayout_2.addWidget(self.removegeneralimgBtn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.image_path_label = QLabel(self.scrollAreaWidgetContents)
        self.image_path_label.setObjectName(u"image_path_label")

        self.verticalLayout_2.addWidget(self.image_path_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.addCategoryBtn = QPushButton(self.scrollAreaWidgetContents)
        self.addCategoryBtn.setObjectName(u"addCategoryBtn")

        self.verticalLayout_2.addWidget(self.addCategoryBtn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setEnabled(True)
        self.groupBox_3.setFont(font1)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.label_6.setFont(font2)

        self.verticalLayout_4.addWidget(self.label_6)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.saveproductbtn = QPushButton(self.scrollAreaWidgetContents)
        self.saveproductbtn.setObjectName(u"saveproductbtn")

        self.verticalLayout_2.addWidget(self.saveproductbtn, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Products Form", None))
        self.very_basic_info.setTitle(QCoreApplication.translate("MainWindow", u"Basic info", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Product Name", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Product brand (local by default)", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Product Description (if any)", None))
        self.general_info.setTitle(QCoreApplication.translate("MainWindow", u"Pricing and Stock", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"purchase price", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Selling Price", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Stock", None))
        self.img_btn.setText(QCoreApplication.translate("MainWindow", u"Add image", None))
        self.removegeneralimgBtn.setText(QCoreApplication.translate("MainWindow", u"Remove Image", None))
        self.image_path_label.setText(QCoreApplication.translate("MainWindow", u"No Image Uploaded", None))
        self.addCategoryBtn.setText(QCoreApplication.translate("MainWindow", u"Add categories", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"categories if (any)", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"No categories added yet", None))
        self.saveproductbtn.setText(QCoreApplication.translate("MainWindow", u"Save Product", None))
    # retranslateUi

