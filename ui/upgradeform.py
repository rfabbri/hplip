#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) Copyright 2001-2012 Hewlett-Packard Development Company, L.P.
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
# Author: Don Welch, Goutam Korra, Naga Samrat Chowdary Narla,

# Std Lib
import sys
import re
import os.path, os
import time

# Local
from base.g import *
from base import device, utils, models, os_utils
from ui_utils import load_pixmap

# Qt
from qt import *
from upgradeform_base import UpgradeForm_base

MANUAL_INSTALL_LINK = "http://hplipopensource.com/hplip-web/install/manual/index.html"

class UpgradeForm(UpgradeForm_base):
    def __init__(self, parent=None, name="",modal=0, fl=0,distro_type= 1,msg=""):
        UpgradeForm_base.__init__(self, parent,  name, modal, fl,distro_type, msg)

        self.msg = msg
        self.distro_type = distro_type
        self.setIcon(load_pixmap('hp_logo', '128x128'))
        self.initUi()

    def initUi(self):
        self.connect(self.NextButton,SIGNAL('clicked()'),self.NextButton_clicked)
        self.connect(self.CancelButton, SIGNAL("clicked()"), self.CancelButton_clicked)

#        self.connect(self.installRadioBtton, SIGNAL("toggled(bool)"), self.installRadioBtton_toggled)
#        self.connect(self.remindRadioBtton, SIGNAL("toggled(bool)"), self.remindRadioBtton_toggled)
#        self.connect(self.dontRemindRadioBtton, SIGNAL("toggled(bool)"), self.dontRemindRadioBtton_toggled)


    def installRadioBtton_toggled(self, radio_enabled):
        log.info("+++++++ installRadioBtton_toggled  = %d" %radio_enabled)
        if radio_enabled is True:
            self.installRadioBtton.setChecked(True)
        else:
            self.installRadioBtton.setChecked(False)


    def remindRadioBtton_toggled(self, radio_enabled):
        log.info("+++++++ remindRadioBtton_toggled  = %d" %radio_enabled)
        if radio_enabled is True:
            self.remindRadioBtton.setChecked(True)
            self.daysSpinBox.setEnabled(True)
        else:
            self.remindRadioBtton.setChecked(False)
            self.daysSpinBox.setEnabled(False)


    def dontRemindRadioBtton_toggled(self, radio_enabled):
        log.info("+++++++ dontRemindRadioBtton_toggled  = %d" %radio_enabled)
        if radio_enabled is True:
            self.dontRemindRadioBtton.setChecked(True)
        else:
            self.dontRemindRadioBtton.setChecked(False)


    def NextButton_clicked (self):
        if self.dontRemindRadioBtton.isChecked():
            log.debug("HPLIP Upgrade, selected Don't remind again radiobutton")
            user_conf.set('upgrade', 'notify_upgrade', 'false')
            msg= "Check for HPLIP updates is disabled. To Upgrade again, check it in 'HP-toolbox' "
            self.SuccessUI( self.__tr(msg))
        elif self.remindRadioBtton.isChecked():
            schedule_days = str(self.daysSpinBox.value())
            log.debug("HPLIP Upgrade, selected remind later radiobutton  days= %d" %(int(schedule_days)))
            next_time = time.time() + (int(schedule_days) *24 * 60 *60)
            user_conf.set('upgrade', 'pending_upgrade_time', str(int(next_time)))
        else:
            log.debug("HPLIP Upgrade, selected Install radiobutton  distro_type=%d" %self.distro_type)
            self.NextButton.setEnabled(False)
            if self.distro_type != 1:		# not tier 1 distro
                utils.openURL(MANUAL_INSTALL_LINK)
            else:
                terminal_cmd = utils.get_terminal()
                if terminal_cmd is not None and utils.which("hp-upgrade"):
                    cmd = terminal_cmd + " 'hp-upgrade -w'"
                    os_utils.execute(cmd)
                    self.result = True
                else:
                    log.error("Failed to run hp-upgrade command from terminal =%s "%terminal_cmd)
                    self.FailureUI( self.__tr("Failed to run hp-upgrade"))

        self.close()


    def CancelButton_clicked(self):
        log.debug("User exit")
        self.close()


    def FailureUI(self, error_text):
        QMessageBox.critical(self,
            self.caption(),
            error_text,
            QMessageBox.Ok,
            QMessageBox.NoButton,
            QMessageBox.NoButton)

    def SuccessUI(self, text):
        QMessageBox.information(self,
                             self.caption(),
                             text,
                              QMessageBox.Ok,
                              QMessageBox.NoButton,
                              QMessageBox.NoButton)


    def __tr(self,s,c = None):
        return qApp.translate("UpgradeDialog",s,c)
