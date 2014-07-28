# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/pluginlicensedialog_base.ui'
#
# Created: Mon May  4 14:30:35 2009
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
        self.StackedWidget = QtGui.QStackedWidget(Dialog)
        self.StackedWidget.setObjectName("StackedWidget")
        self.page = QtGui.QWidget()
        self.page.setObjectName("page")
        self.gridlayout1 = QtGui.QGridLayout(self.page)
        self.gridlayout1.setObjectName("gridlayout1")
        self.label = QtGui.QLabel(self.page)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label, 0, 0, 1, 1)
        self.line = QtGui.QFrame(self.page)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.page)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2, 2, 0, 1, 1)
        self.LicenseTextEdit = QtGui.QTextEdit(self.page)
        self.LicenseTextEdit.setAutoFormatting(QtGui.QTextEdit.AutoAll)
        self.LicenseTextEdit.setReadOnly(True)
        self.LicenseTextEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.LicenseTextEdit.setObjectName("LicenseTextEdit")
        self.gridlayout1.addWidget(self.LicenseTextEdit, 3, 0, 1, 1)
        self.AgreeCheckBox = QtGui.QCheckBox(self.page)
        self.AgreeCheckBox.setObjectName("AgreeCheckBox")
        self.gridlayout1.addWidget(self.AgreeCheckBox, 4, 0, 1, 1)
        self.StackedWidget.addWidget(self.page)
        self.gridlayout.addWidget(self.StackedWidget, 0, 0, 1, 5)
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout.addWidget(self.line_2, 1, 0, 1, 5)
        spacerItem = QtGui.QSpacerItem(161, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 2, 1, 1, 1)
        self.BackButton = QtGui.QPushButton(Dialog)
        self.BackButton.setEnabled(False)
        self.BackButton.setObjectName("BackButton")
        self.gridlayout.addWidget(self.BackButton, 2, 2, 1, 1)
        self.NextButton = QtGui.QPushButton(Dialog)
        self.NextButton.setEnabled(False)
        self.NextButton.setObjectName("NextButton")
        self.gridlayout.addWidget(self.NextButton, 2, 3, 1, 1)
        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridlayout.addWidget(self.CancelButton, 2, 4, 1, 1)

        self.retranslateUi(Dialog)
        self.StackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.AgreeCheckBox, QtCore.SIGNAL("toggled(bool)"), self.NextButton.setEnabled)
        QtCore.QObject.connect(self.NextButton, QtCore.SIGNAL("clicked()"), Dialog.accept)
        QtCore.QObject.connect(self.CancelButton, QtCore.SIGNAL("clicked()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Plug-in Installer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Driver Plug-in License Agreement", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please read the driver plug-in license agreement and then check the <span style=\" font-style:italic;\">I agree</span> box and then click <span style=\" font-style:italic;\">Next</span> to continue.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.AgreeCheckBox.setText(QtGui.QApplication.translate("Dialog", "I agree to the terms of the driver plug-in license agreement", None, QtGui.QApplication.UnicodeUTF8))
        self.BackButton.setText(QtGui.QApplication.translate("Dialog", "< Back", None, QtGui.QApplication.UnicodeUTF8))
        self.NextButton.setText(QtGui.QApplication.translate("Dialog", "Next >", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

