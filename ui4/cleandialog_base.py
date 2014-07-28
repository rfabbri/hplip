# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4/cleandialog_base.ui'
#
# Created: Mon May  4 14:30:31 2009
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
        self.gridlayout.addWidget(self.label, 0, 0, 1, 2)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line, 1, 0, 1, 4)
        self.StackedWidget = QtGui.QStackedWidget(Dialog)
        self.StackedWidget.setFrameShape(QtGui.QFrame.NoFrame)
        self.StackedWidget.setObjectName("StackedWidget")
        self.StartPage = QtGui.QWidget()
        self.StartPage.setObjectName("StartPage")
        self.gridlayout1 = QtGui.QGridLayout(self.StartPage)
        self.gridlayout1.setObjectName("gridlayout1")
        self.DeviceComboBox = DeviceUriComboBox(self.StartPage)
        self.DeviceComboBox.setObjectName("DeviceComboBox")
        self.gridlayout1.addWidget(self.DeviceComboBox, 0, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.StartPage)
        self.groupBox.setObjectName("groupBox")
        self.gridlayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout2.setObjectName("gridlayout2")
        self.Prompt = QtGui.QLabel(self.groupBox)
        self.Prompt.setObjectName("Prompt")
        self.gridlayout2.addWidget(self.Prompt, 0, 0, 1, 1)
        self.gridlayout1.addWidget(self.groupBox, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem, 2, 0, 1, 1)
        self.StackedWidget.addWidget(self.StartPage)
        self.Level1Page = QtGui.QWidget()
        self.Level1Page.setObjectName("Level1Page")
        self.gridlayout3 = QtGui.QGridLayout(self.Level1Page)
        self.gridlayout3.setObjectName("gridlayout3")
        self.LoadPaper = LoadPaperGroupBox(self.Level1Page)
        self.LoadPaper.setObjectName("LoadPaper")
        self.gridlayout3.addWidget(self.LoadPaper, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.Level1Page)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridlayout4 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout4.setObjectName("gridlayout4")
        self.Prompt_2 = QtGui.QLabel(self.groupBox_2)
        self.Prompt_2.setWordWrap(True)
        self.Prompt_2.setObjectName("Prompt_2")
        self.gridlayout4.addWidget(self.Prompt_2, 0, 0, 1, 1)
        self.gridlayout3.addWidget(self.groupBox_2, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout3.addItem(spacerItem1, 2, 0, 1, 1)
        self.StackedWidget.addWidget(self.Level1Page)
        self.Level2Page = QtGui.QWidget()
        self.Level2Page.setObjectName("Level2Page")
        self.gridlayout5 = QtGui.QGridLayout(self.Level2Page)
        self.gridlayout5.setObjectName("gridlayout5")
        self.LoadPaper_2 = LoadPaperGroupBox(self.Level2Page)
        self.LoadPaper_2.setObjectName("LoadPaper_2")
        self.gridlayout5.addWidget(self.LoadPaper_2, 0, 0, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.Level2Page)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridlayout6 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout6.setObjectName("gridlayout6")
        self.Prompt_5 = QtGui.QLabel(self.groupBox_3)
        self.Prompt_5.setWordWrap(True)
        self.Prompt_5.setObjectName("Prompt_5")
        self.gridlayout6.addWidget(self.Prompt_5, 0, 0, 1, 1)
        self.gridlayout5.addWidget(self.groupBox_3, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 91, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout5.addItem(spacerItem2, 2, 0, 1, 1)
        self.StackedWidget.addWidget(self.Level2Page)
        self.Level3Page = QtGui.QWidget()
        self.Level3Page.setObjectName("Level3Page")
        self.gridlayout7 = QtGui.QGridLayout(self.Level3Page)
        self.gridlayout7.setObjectName("gridlayout7")
        self.LoadPaper_3 = LoadPaperGroupBox(self.Level3Page)
        self.LoadPaper_3.setObjectName("LoadPaper_3")
        self.gridlayout7.addWidget(self.LoadPaper_3, 0, 0, 1, 1)
        self.groupBox_4 = QtGui.QGroupBox(self.Level3Page)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridlayout8 = QtGui.QGridLayout(self.groupBox_4)
        self.gridlayout8.setObjectName("gridlayout8")
        self.Prompt_6 = QtGui.QLabel(self.groupBox_4)
        self.Prompt_6.setWordWrap(True)
        self.Prompt_6.setObjectName("Prompt_6")
        self.gridlayout8.addWidget(self.Prompt_6, 0, 0, 1, 1)
        self.gridlayout7.addWidget(self.groupBox_4, 1, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 71, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout7.addItem(spacerItem3, 2, 0, 1, 1)
        self.StackedWidget.addWidget(self.Level3Page)
        self.FrontPanelPage = QtGui.QWidget()
        self.FrontPanelPage.setObjectName("FrontPanelPage")
        self.gridlayout9 = QtGui.QGridLayout(self.FrontPanelPage)
        self.gridlayout9.setObjectName("gridlayout9")
        self.label_2 = QtGui.QLabel(self.FrontPanelPage)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridlayout9.addWidget(self.label_2, 0, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout9.addItem(spacerItem4, 1, 0, 1, 1)
        self.StackedWidget.addWidget(self.FrontPanelPage)
        self.gridlayout.addWidget(self.StackedWidget, 2, 0, 1, 4)
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout.addWidget(self.line_2, 4, 0, 1, 4)
        self.StepText = QtGui.QLabel(Dialog)
        self.StepText.setObjectName("StepText")
        self.gridlayout.addWidget(self.StepText, 5, 0, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(351, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem5, 5, 1, 1, 1)
        self.NextButton = QtGui.QPushButton(Dialog)
        self.NextButton.setObjectName("NextButton")
        self.gridlayout.addWidget(self.NextButton, 5, 2, 1, 1)
        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.gridlayout.addWidget(self.CancelButton, 5, 3, 1, 1)

        self.retranslateUi(Dialog)
        self.StackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "HP Device Manager - Clean Print Cartridges", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Clean Print Cartridges", None, QtGui.QApplication.UnicodeUTF8))
        self.Prompt.setText(QtGui.QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Click<span style=\" font-style:italic;\"> Next</span> to begin the cleaning process.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.Prompt_2.setText(QtGui.QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Click <span style=\" font-style:italic;\">Clean</span> to begin the level 1 cleaning process.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.Prompt_5.setText(QtGui.QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Cleaning level 1 is done after the page being printed is complete.</span> If the printed output from level 1 cleaning is acceptable, then click <span style=\" font-style:italic;\">Cancel</span> to exit. Otherwise, click <span style=\" font-style:italic;\">Clean</span> again to begin the level 2 cleaning process.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.Prompt_6.setText(QtGui.QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Cleaning level 2 is done after the page being printed is complete.</span> If the printed output from level 2 cleaning is acceptable, then click <span style=\" font-style:italic;\">Cancel</span> to exit. Otherwise, click <span style=\" font-style:italic;\">Clean</span> again to begin the level 3 cleaning process. </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Cartridge cleaning on this printer is only available by accessing the front panel of the printer. </span>Please refer to the user guide for the printer for more information. Click <span style=\" font-style:italic;\">Finish</span> to exit.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.StepText.setText(QtGui.QApplication.translate("Dialog", "Step %1 of %2", None, QtGui.QApplication.UnicodeUTF8))
        self.NextButton.setText(QtGui.QApplication.translate("Dialog", "Next >", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

from loadpapergroupbox import LoadPaperGroupBox
from deviceuricombobox import DeviceUriComboBox
