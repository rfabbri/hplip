# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/mimetypesdialog_base.ui'
#
# Created: Mon May  4 14:30:34 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MimeTypesDialog_base(object):
    def setupUi(self, MimeTypesDialog_base):
        MimeTypesDialog_base.setObjectName("MimeTypesDialog_base")
        MimeTypesDialog_base.resize(500, 540)
        self.gridlayout = QtGui.QGridLayout(MimeTypesDialog_base)
        self.gridlayout.setObjectName("gridlayout")
        self.textLabel3_2 = QtGui.QLabel(MimeTypesDialog_base)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel3_2.sizePolicy().hasHeightForWidth())
        self.textLabel3_2.setSizePolicy(sizePolicy)
        self.textLabel3_2.setWordWrap(False)
        self.textLabel3_2.setObjectName("textLabel3_2")
        self.gridlayout.addWidget(self.textLabel3_2, 0, 0, 1, 2)
        self.line1_2 = QtGui.QFrame(MimeTypesDialog_base)
        self.line1_2.setFrameShape(QtGui.QFrame.HLine)
        self.line1_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1_2.setObjectName("line1_2")
        self.gridlayout.addWidget(self.line1_2, 1, 0, 1, 2)
        self.TypesTableWidget = QtGui.QTableWidget(MimeTypesDialog_base)
        self.TypesTableWidget.setAlternatingRowColors(True)
        self.TypesTableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.TypesTableWidget.setObjectName("TypesTableWidget")
        self.TypesTableWidget.setColumnCount(3)
        self.TypesTableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.TypesTableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.TypesTableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.TypesTableWidget.setHorizontalHeaderItem(2, item)
        self.gridlayout.addWidget(self.TypesTableWidget, 2, 0, 1, 2)
        self.textLabel1 = QtGui.QLabel(MimeTypesDialog_base)
        self.textLabel1.setWordWrap(True)
        self.textLabel1.setObjectName("textLabel1")
        self.gridlayout.addWidget(self.textLabel1, 3, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(301, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 4, 0, 1, 1)
        self.pushButton10 = QtGui.QPushButton(MimeTypesDialog_base)
        self.pushButton10.setObjectName("pushButton10")
        self.gridlayout.addWidget(self.pushButton10, 4, 1, 1, 1)

        self.retranslateUi(MimeTypesDialog_base)
        QtCore.QObject.connect(self.pushButton10, QtCore.SIGNAL("clicked()"), MimeTypesDialog_base.accept)
        QtCore.QMetaObject.connectSlotsByName(MimeTypesDialog_base)

    def retranslateUi(self, MimeTypesDialog_base):
        MimeTypesDialog_base.setWindowTitle(QtGui.QApplication.translate("MimeTypesDialog_base", "HP Device Manager - MIME Types", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel3_2.setText(QtGui.QApplication.translate("MimeTypesDialog_base", "<b>File/document types that can be added to the file list.</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.TypesTableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MimeTypesDialog_base", "MIME Type", None, QtGui.QApplication.UnicodeUTF8))
        self.TypesTableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MimeTypesDialog_base", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.TypesTableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MimeTypesDialog_base", "Usual File Extension(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setText(QtGui.QApplication.translate("MimeTypesDialog_base", "<i>Note: To print or fax file/document types that do not appear on this list, print the document from the application that created it through the appropriate CUPS printer.</i>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton10.setText(QtGui.QApplication.translate("MimeTypesDialog_base", "OK", None, QtGui.QApplication.UnicodeUTF8))

