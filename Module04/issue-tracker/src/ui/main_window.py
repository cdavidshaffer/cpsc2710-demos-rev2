# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFormLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(921, 770)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.issues_table = QTableWidget(self.centralwidget)
        if (self.issues_table.columnCount() < 4):
            self.issues_table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.issues_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.issues_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.issues_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.issues_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.issues_table.setObjectName(u"issues_table")
        self.issues_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.issues_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.horizontalLayout_2.addWidget(self.issues_table)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.new_issue_button = QPushButton(self.centralwidget)
        self.new_issue_button.setObjectName(u"new_issue_button")

        self.verticalLayout.addWidget(self.new_issue_button)

        self.delete_issue_button = QPushButton(self.centralwidget)
        self.delete_issue_button.setObjectName(u"delete_issue_button")

        self.verticalLayout.addWidget(self.delete_issue_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.title_edit = QLineEdit(self.widget)
        self.title_edit.setObjectName(u"title_edit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.title_edit)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.status_combo = QComboBox(self.widget)
        self.status_combo.setObjectName(u"status_combo")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.status_combo)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.priority_combo = QComboBox(self.widget)
        self.priority_combo.setObjectName(u"priority_combo")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.priority_combo)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.assigned_to_edit = QLineEdit(self.widget)
        self.assigned_to_edit.setObjectName(u"assigned_to_edit")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.assigned_to_edit)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.notes_plain_text = QPlainTextEdit(self.widget)
        self.notes_plain_text.setObjectName(u"notes_plain_text")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.notes_plain_text)


        self.verticalLayout_2.addWidget(self.widget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cancel_button = QPushButton(self.centralwidget)
        self.cancel_button.setObjectName(u"cancel_button")

        self.horizontalLayout.addWidget(self.cancel_button)

        self.save_button = QPushButton(self.centralwidget)
        self.save_button.setObjectName(u"save_button")

        self.horizontalLayout.addWidget(self.save_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 921, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.title_edit)
        self.label_2.setBuddy(self.status_combo)
        self.label_3.setBuddy(self.priority_combo)
        self.label_4.setBuddy(self.assigned_to_edit)
        self.label_5.setBuddy(self.notes_plain_text)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.title_edit, self.status_combo)
        QWidget.setTabOrder(self.status_combo, self.priority_combo)
        QWidget.setTabOrder(self.priority_combo, self.assigned_to_edit)
        QWidget.setTabOrder(self.assigned_to_edit, self.notes_plain_text)
        QWidget.setTabOrder(self.notes_plain_text, self.save_button)
        QWidget.setTabOrder(self.save_button, self.cancel_button)
        QWidget.setTabOrder(self.cancel_button, self.issues_table)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        ___qtablewidgetitem = self.issues_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        ___qtablewidgetitem1 = self.issues_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        ___qtablewidgetitem2 = self.issues_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Priority", None))
        ___qtablewidgetitem3 = self.issues_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Assigned to", None))
        self.new_issue_button.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.delete_issue_button.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"&Title", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"&Status", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"&Priority", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"&Assigned to", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"&Notes", None))
        self.cancel_button.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.save_button.setText(QCoreApplication.translate("MainWindow", u"Save", None))
    # retranslateUi

