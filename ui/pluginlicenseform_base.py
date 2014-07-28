# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/pluginlicenseform_base.ui'
#
# Created: Mon May 19 10:33:53 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *


class PluginLicenseForm_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("PluginLicenseForm_base")


        PluginLicenseForm_baseLayout = QGridLayout(self,1,1,11,6,"PluginLicenseForm_baseLayout")

        self.acceptCheckBox = QCheckBox(self,"acceptCheckBox")

        PluginLicenseForm_baseLayout.addWidget(self.acceptCheckBox,3,0)

        self.installPushButton = QPushButton(self,"installPushButton")
        self.installPushButton.setEnabled(0)

        PluginLicenseForm_baseLayout.addWidget(self.installPushButton,3,3)

        self.cancelPushButton = QPushButton(self,"cancelPushButton")

        PluginLicenseForm_baseLayout.addWidget(self.cancelPushButton,3,2)
        spacer3 = QSpacerItem(81,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        PluginLicenseForm_baseLayout.addItem(spacer3,3,1)

        self.licenseTextEdit = QTextEdit(self,"licenseTextEdit")
        self.licenseTextEdit.setReadOnly(1)

        PluginLicenseForm_baseLayout.addMultiCellWidget(self.licenseTextEdit,2,2,0,3)

        self.textLabel1 = QLabel(self,"textLabel1")

        PluginLicenseForm_baseLayout.addMultiCellWidget(self.textLabel1,1,1,0,3)

        self.titleText = QLabel(self,"titleText")
        titleText_font = QFont(self.titleText.font())
        titleText_font.setPointSize(16)
        self.titleText.setFont(titleText_font)

        PluginLicenseForm_baseLayout.addWidget(self.titleText,0,0)

        self.languageChange()

        self.resize(QSize(609,480).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.acceptCheckBox,SIGNAL("toggled(bool)"),self.installPushButton.setEnabled)
        self.connect(self.cancelPushButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.installPushButton,SIGNAL("clicked()"),self.accept)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Plugin Installer License"))
        self.acceptCheckBox.setText(self.__tr("I accept the terms of the license"))
        self.installPushButton.setText(self.__tr("Install Plugin"))
        self.cancelPushButton.setText(self.__tr("Cancel"))
        self.textLabel1.setText(self.__tr("Please read the plugin license agreement. Click \"I accept\" to accept the terms of the license."))
        self.titleText.setText(self.__tr("Plugin License Agreement"))


    def __tr(self,s,c = None):
        return qApp.translate("PluginLicenseForm_base",s,c)
