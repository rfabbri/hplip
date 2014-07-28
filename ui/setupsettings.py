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

from qt import *
from setupsettings_base import SetupSettings_base

class SetupSettings(SetupSettings_base):
    def __init__(self, bus, filter, search, ttl, timeout, parent=None, name=None, modal=0, fl = 0):
        SetupSettings_base.__init__(self, parent, name, modal, fl)

        self.filter = filter
        self.search = search
        self.ttl = ttl
        self.timeout = timeout

        log.debug("filter is %s" % filter)
        if prop.fax_build and prop.scan_build:
            if not filter:
                self.filterButtonGroup.setButton(0)
            else:
                self.filterButtonGroup.setButton(1)
                self.faxCheckBox.setChecked('fax' in filter)
                self.scanCheckBox.setChecked('scan' in filter)
                self.pcardCheckBox.setChecked('pcard' in filter)
                self.copyCheckBox.setChecked('copy' in filter)
        else:
            self.filterButtonGroup.setEnabled(False)

        self.searchTermLineEdit.setText(self.search)

        self.ttlSpinBox.setValue(self.ttl)
        self.timeoutSpinBox.setValue(self.timeout)
        
        if not prop.net_build:
            self.ttlSpinBox.setEnabled(False)
            self.timeoutSpinBox.setEnabled(False)
            self.groupBox3.setEnabled(False)
            self.textLabel7.setEnabled(False)
            self.textLabel8.setEnabled(False)

    def faxCheckBox_toggled(self,a0):
        self.updateFilter()

    def scanCheckBox_toggled(self,a0):
        self.updateFilter()

    def pcardCheckBox_toggled(self,a0):
        self.updateFilter()

    def copyCheckBox_toggled(self,a0):
        self.updateFilter()

    def filterButtonGroup_clicked(self, a0):
        self.updateFilter(a0)

    def searchTermLineEdit_textChanged(self, a0):
        self.search = unicode(a0)

    def ttlSpinBox_valueChanged(self, a0):
        self.ttl = a0
        log.debug(self.ttl)

    def timeoutSpinBox_valueChanged(self, a0):
        self.timeout = a0
        log.debug(self.timeout)

    def updateFilter(self, id=-1):
        self.filter = []
        
        if id == 0:
            return 

        else:
            if self.faxCheckBox.isChecked():
                self.filter.append('fax')

            if self.scanCheckBox.isChecked():
                self.filter.append('scan')

            if self.pcardCheckBox.isChecked():
                self.filter.append('pcard')

            if self.copyCheckBox.isChecked():
                self.filter.append('copy')

            #if not filter:
            #    filter.append('none')

        log.debug(self.filter)


    def defaultsPushButton_clicked(self):
        self.filterButtonGroup.setButton(0)
        self.updateFilter(0)
        self.searchTermLineEdit.setText('')
        self.ttlSpinBox.setValue(4)
        self.timeoutSpinBox.setValue(5)

    def __tr(self,s,c = None):
        return qApp.translate("SetupSettings_base",s,c)
