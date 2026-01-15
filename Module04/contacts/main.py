# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSplitter, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(779, 477)
        self.horizontalLayout_3 = QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.listWidget = QListWidget(self.widget)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.splitter.addWidget(self.widget)
        self.widget1 = QWidget(self.splitter)
        self.widget1.setObjectName(u"widget1")
        self.verticalLayout_2 = QVBoxLayout(self.widget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.label = QLabel(self.widget1)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.name_edit = QLineEdit(self.widget1)
        self.name_edit.setObjectName(u"name_edit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.name_edit)

        self.label_2 = QLabel(self.widget1)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.address_edit = QTextEdit(self.widget1)
        self.address_edit.setObjectName(u"address_edit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.address_edit)

        self.label_3 = QLabel(self.widget1)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.phone_edit = QLineEdit(self.widget1)
        self.phone_edit.setObjectName(u"phone_edit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.phone_edit)

        self.emailLabel = QLabel(self.widget1)
        self.emailLabel.setObjectName(u"emailLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.emailLabel)

        self.email_edit = QLineEdit(self.widget1)
        self.email_edit.setObjectName(u"email_edit")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.email_edit)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_3 = QPushButton(self.widget1)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.widget1)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_2.addWidget(self.pushButton_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.splitter.addWidget(self.widget1)

        self.horizontalLayout_3.addWidget(self.splitter)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"-", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"+", None))
        self.label.setText(QCoreApplication.translate("Form", u"Name:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Address:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Phone:", None))
        self.emailLabel.setText(QCoreApplication.translate("Form", u"Email", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"Save", None))
    # retranslateUi

