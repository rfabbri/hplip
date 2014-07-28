# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/printtestpagedialog_base.ui'
#
# Created: Mon May  4 14:30:36 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(700, 500)
        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line, 1, 0, 1, 4)
        self.PrinterNameCombo = PrinterNameComboBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrinterNameCombo.sizePolicy().hasHeightForWidth())
        self.PrinterNameCombo.setSizePolicy(sizePolicy)
        self.PrinterNameCombo.setObjectName("PrinterNameCombo")
        self.gridlayout.addWidget(self.PrinterNameCombo, 2, 0, 1, 4)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setObjectName("gridlayout1")
        self.HPLIPTestPageRadioButton = QtGui.QRadioButton(self.groupBox)
        self.HPLIPTestPageRadioButton.setObjectName("HPLIPTestPageRadioButton")
        self.gridlayout1.addWidget(self.HPLIPTestPageRadioButton, 0, 0, 1, 1)
        self.PrinterDiagnosticRadioButto = QtGui.QRadioButton(self.groupBox)
        self.PrinterDiagnosticRadioButto.setEnabled(False)
        self.PrinterDiagnosticRadioButto.setObjectName("PrinterDiagnosticRadioButto")
        self.gridlayout1.addWidget(self.PrinterDiagnosticRadioButto, 1, 0, 1, 1)
        self.gridlayout.addWidget(self.groupBox, 3, 0, 1, 4)
        self.LoadPaper = LoadPaperGroupBox(Dialog)
        self.LoadPaper.setObjectName("LoadPaper")
        self.gridlayout.addWidget(self.LoadPaper, 4, 0, 1, 4)
        spacerItem = QtGui.QSpacerItem(189, 61, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.gridlayout.addItem(spacerItem, 5, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(400, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 6, 0, 1, 2)
        self.PrintTestpageButton = QtGui.QPushButton(Dialog)
        self.PrintTestpageButton.setObjectName("PrintTestpageButton")
        self.gridlayout.addWidget(self.PrintTestpageButton, 6, 2, 1, 1)
        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridlayout.addWidget(self.CancelButton, 6, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Print Test Page", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Print Test Page", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.HPLIPTestPageRadioButton.setText(QtGui.QApplication.translate("Dialog", "HPLIP test page (tests print driver)", None, QtGui.QApplication.UnicodeUTF8))
        self.PrinterDiagnosticRadioButto.setText(QtGui.QApplication.translate("Dialog", "Printer diagnostic page (does not test print driver)", None, QtGui.QApplication.UnicodeUTF8))
        self.PrintTestpageButton.setText(QtGui.QApplication.translate("Dialog", "Print Test Page", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

from printernamecombobox import PrinterNameComboBox
from loadpapergroupbox import LoadPaperGroupBox
