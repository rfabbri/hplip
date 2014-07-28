# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/makecopiesdialog_base.ui'
#
# Created: Mon May  4 14:30:34 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
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
        self.DeviceComboBox = DeviceUriComboBox(Dialog)
        self.DeviceComboBox.setObjectName("DeviceComboBox")
        self.gridlayout.addWidget(self.DeviceComboBox, 2, 0, 1, 4)
        spacerItem = QtGui.QSpacerItem(20, 341, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(391, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 4, 0, 1, 2)
        self.CopyButton = QtGui.QPushButton(Dialog)
        self.CopyButton.setObjectName("CopyButton")
        self.gridlayout.addWidget(self.CopyButton, 4, 2, 1, 1)
        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridlayout.addWidget(self.CancelButton, 4, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Make Copies", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Make Copies", None, QtGui.QApplication.UnicodeUTF8))
        self.CopyButton.setText(QtGui.QApplication.translate("Dialog", "Make Copies", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

from deviceuricombobox import DeviceUriComboBox
