# -*- coding: utf-8 -*-
#
# (c) Copyright 2001-2007 Hewlett-Packard Development Company, L.P.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# Author: Don Welch
#

from base.g import *
from base.codes import *
from base import utils
from qt import *
from settingsdialog_base import SettingsDialog_base

class SettingsDialog(SettingsDialog_base):
    def __init__(self, parent = None,name = None,modal = 0,fl = 0):
        SettingsDialog_base.__init__(self,parent,name,modal,fl)
        self.DefaultsButton.setEnabled(False)
        #self.sendmail = utils.which('sendmail')

        #if not self.sendmail:
        #    self.EmailTestButton.setEnabled(False)

        self.user_settings = utils.UserSettings()
        self.updateControls()

    def updateControls(self):
        self.autoRefreshCheckBox.setChecked(self.user_settings.auto_refresh)
        self.AutoRefreshRate.setValue(self.user_settings.auto_refresh_rate) # min
        self.refreshScopeButtonGroup.setButton(self.user_settings.auto_refresh_type)

##        self.EmailCheckBox.setChecked(self.user_settings.email_alerts)
##        self.EmailAddress.setText(self.user_settings.email_to_addresses)
##        self.senderLineEdit.setText(self.user_settings.email_from_address)

        self.PrintCommand.setText(self.user_settings.cmd_print)
        #self.PrintCommand.setEnabled(not self.user_settings.cmd_print_int)

##        if self.user_settings.cmd_print_int:
##            self.printButtonGroup.setButton(0)
##        else:
##            self.printButtonGroup.setButton(1)

        self.ScanCommand.setText(self.user_settings.cmd_scan)
        #self.ScanCommand.setEnabled(not self.user_settings.cmd_scan_int)

##        if self.user_settings.cmd_scan_int:
##            self.scanButtonGroup.setButton(0)
##        else:
##            self.scanButtonGroup.setButton(1)

        self.AccessPCardCommand.setText(self.user_settings.cmd_pcard)
        #self.AccessPCardCommand.setEnabled(not self.user_settings.cmd_pcard_int)

##        if self.user_settings.cmd_pcard_int:
##            self.pcardButtonGroup.setButton(0)
##        else:
##            self.pcardButtonGroup.setButton(1)

        self.SendFaxCommand.setText(self.user_settings.cmd_fax)
        #self.SendFaxCommand.setEnabled(not self.user_settings.cmd_fax_int)

##        if self.user_settings.cmd_fax_int:
##            self.faxButtonGroup.setButton(0)
##        else:
##            self.faxButtonGroup.setButton(1)

        self.MakeCopiesCommand.setText(self.user_settings.cmd_copy)
        #self.MakeCopiesCommand.setEnabled(not self.user_settings.cmd_copy_int)

##        if self.user_settings.cmd_copy_int:
##            self.copyButtonGroup.setButton(0)
##        else:
##            self.copyButtonGroup.setButton(1)    

    def updateData(self):
        self.user_settings.cmd_print = unicode(self.PrintCommand.text())
        #self.user_settings.cmd_print_int = (self.printButtonGroup.selectedId() == 0)

        self.user_settings.cmd_scan = unicode(self.ScanCommand.text())
        #self.user_settings.cmd_scan_int = (self.scanButtonGroup.selectedId() == 0)

        self.user_settings.cmd_pcard = unicode(self.AccessPCardCommand.text())
        #self.user_settings.cmd_pcard_int = (self.pcardButtonGroup.selectedId() == 0)

        self.user_settings.cmd_fax   = unicode(self.SendFaxCommand.text())
        #self.user_settings.cmd_fax_int = (self.faxButtonGroup.selectedId() == 0)

        self.user_settings.cmd_copy  = unicode(self.MakeCopiesCommand.text())
        #self.user_settings.cmd_copy_int = (self.copyButtonGroup.selectedId() == 0)

##        self.user_settings.email_alerts = bool(self.EmailCheckBox.isChecked())
##        self.user_settings.email_to_addresses = unicode(self.EmailAddress.text())
##        self.user_settings.email_from_address = unicode(self.senderLineEdit.text())

        self.user_settings.auto_refresh = str(self.autoRefreshCheckBox.isChecked())
        self.user_settings.auto_refresh_type = str(self.refreshScopeButtonGroup.selectedId())
        self.user_settings.auto_refresh_rate = str(self.AutoRefreshRate.value())

##    def PrintCmdChangeButton_clicked(self):
##        pass
##
##    def ScanCmdChangeButton_clicked(self):
##        pass
##
##    def AccessPCardCmdChangeButton_clicked(self):
##        pass
##
##    def SendFaxCmdChangeButton_clicked(self):
##        pass
##
##    def MakeCopiesCmdChangeButton_clicked(self):
##        pass

    def DefaultsButton_clicked(self):
        self.user_settings.loadDefaults()
        self.updateControls()

    def TabWidget_currentChanged(self,a0):
        name = str(a0.name())

        if name == 'FunctionCommands':
            self.DefaultsButton.setEnabled(True)
        else:
            self.DefaultsButton.setEnabled(False)

##    def EmailTestButton_clicked(self): 
##        email_to_addresses = unicode(self.EmailAddress.text())
##        email_from_address = unicode(self.senderLineEdit.text())
##
##        if not email_to_addresses or not email_from_address:
##            QMessageBox.warning(self,
##                                 self.caption(),
##                                 self.__tr("<b>One or more email addresses are missing.</b><p>Please enter this information and try again."),
##                                  QMessageBox.Ok,
##                                  QMessageBox.NoButton,
##                                  QMessageBox.NoButton)
##            return
##        
##        # TODO:
####        service.setAlerts(self.hpssd_sock, 
####                          True,
####                          email_from_address,
####                          email_to_addresses)
##
##        #result_code = service.testEmail(self.hpssd_sock, prop.username)
##        log.debug(result_code)
##
##        QMessageBox.information(self,
##                     self.caption(),
##                     self.__tr("<p><b>Please check your email for a test message.</b><p>If the message doesn't arrive, please check your settings and try again."),
##                      QMessageBox.Ok,
##                      QMessageBox.NoButton,
##                      QMessageBox.NoButton)


    def autoRefreshCheckBox_clicked(self):
        pass

##    def CleaningLevel_clicked(self,a0):
##        pass

    def refreshScopeButtonGroup_clicked(self,a0):
        self.auto_refresh_type = int(a0)

##    def printButtonGroup_clicked(self,a0):
##        self.PrintCommand.setEnabled(a0)
##
##    def scanButtonGroup_clicked(self,a0):
##        self.ScanCommand.setEnabled(a0)
##
##    def faxButtonGroup_clicked(self,a0):
##        self.SendFaxCommand.setEnabled(a0)
##
##    def pcardButtonGroup_clicked(self,a0):
##        self.AccessPCardCommand.setEnabled(a0)
##
##    def copyButtonGroup_clicked(self,a0):
##        self.MakeCopiesCommand.setEnabled(a0)

    def accept(self):
        self.updateData()
        self.user_settings.save()
        SettingsDialog_base.accept(self)

    def __tr(self,s,c = None):
        return qApp.translate("SettingsDialog",s,c)


