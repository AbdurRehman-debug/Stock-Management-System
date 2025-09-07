# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'welcomepage.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(692, 500)
        Form.setStyleSheet(u"#Form{\n"
"    background-color: #4a4747;\n"
"    color: #fff;\n"
"}\n"
"#Form * {\n"
"    color: #fff;\n"
"}\n"
"#btnCompany{\n"
"    background-color: #90E0EF;\n"
"    color: #000;\n"
"    padding:7px;\n"
"    border-radius: 4px;\n"
"    width:60px;\n"
"    margin-top: 15px;\n"
"\n"
"}\n"
"#companyname {\n"
"    width:250px;\n"
"    height:30px;\n"
"    padding:12px;\n"
"    color: #fff;\n"
"    background-color: #353333;\n"
"}\n"
"#label_2{\n"
"    margin-bottom: 15px;\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.label_welcome = QLabel(Form)
        self.label_welcome.setObjectName(u"label_welcome")
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.label_welcome.setFont(font)

        self.verticalLayout.addWidget(self.label_welcome, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(16)
        self.label_2.setFont(font1)

        self.verticalLayout.addWidget(self.label_2, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.companyname = QLineEdit(Form)
        self.companyname.setObjectName(u"companyname")

        self.verticalLayout.addWidget(self.companyname, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.btnCompany = QPushButton(Form)
        self.btnCompany.setObjectName(u"btnCompany")
        self.btnCompany.setFont(font1)

        self.verticalLayout.addWidget(self.btnCompany, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_welcome.setText(QCoreApplication.translate("Form", u"Welcome", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Enter Company Name", None))
        self.btnCompany.setText(QCoreApplication.translate("Form", u"Enter", None))
    # retranslateUi

