# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/pluginlicenseform_base.ui'
#
# Created: Thu May 15 11:08:01 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *
from pluginlicenseform_base import PluginLicenseForm_base

class PluginLicenseForm(PluginLicenseForm_base):
    def __init__(self, license_txt, parent=None, name=None, modal=0, fl=0):
        PluginLicenseForm_base.__init__(self,parent,name,modal,fl)

        self.titleText.setFont(QFont("Helvetica", 16))
        self.licenseTextEdit.setText(license_txt)
        

    def __tr(self,s,c = None):
        return qApp.translate("PluginLicenseForm",s,c)
