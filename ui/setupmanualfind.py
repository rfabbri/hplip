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

from qt import *
from setupmanualfind_base import SetupManualFind_base

class SetupManualFind(SetupManualFind_base):
    def __init__(self, bus, parent=None, name=None, modal=0, fl = 0):
        SetupManualFind_base.__init__(self, parent, name, modal, fl)
        self.bus = bus
        self.param = ''

        if self.bus == 'net':
            self.findHeadingText.setText(self.__tr("""Please enter the printer's network hostname or IP address."""))
            self.hintTextLabel.setText(self.__tr("""<i>(IPv4 address "a.b.c.d" or "hostname".)</i>"""))
            self.findTextLabel.setText(self.__tr("""Hostname or IP Address:"""))

        elif self.bus == 'usb':
            self.findHeadingText.setText(self.__tr("""Please enter the USB ID for the printer."""))
            self.hintTextLabel.setText(self.__tr("""<i>("xxx:yyy" where xxx is the USB bus ID and yyy is the USB device ID. The ':' and all leading zeroes must be present. Use 'lsusb' to determine this information.)</i>"""))
            self.findTextLabel.setText(self.__tr("""USB ID:"""))
            self.findLineEdit.setInputMask("000:000;0")

        elif self.bus == 'par':
            self.findHeadingText.setText(self.__tr("""Please enter the filesystem device node for the printer."""))
            self.hintTextLabel.setText(self.__tr(""" <i>("/dev/parportX", X=0,1,2,...)</i>"""))
            self.findTextLabel.setText(self.__tr("""Device Node:"""))

    def findLineEdit_textChanged(self,a0):
        self.param = unicode(a0)

        if self.bus == 'usb':
            bus, dev = self.param.split(':')
            self.param = ''.join(['0'*(3-len(bus)), bus, ':', '0'*(3-len(dev)), dev])

    def __tr(self,s,c = None):
        return qApp.translate("SetupManualFind_base",s,c)
