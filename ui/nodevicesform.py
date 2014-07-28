# -*- coding: utf-8 -*-
#
# (c) Copyright 2001-2008 Hewlett-Packard Development Company, L.P.
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

# Std Lib
import os.path

# Local
from base.g import *
from base import utils
from prnt import cups
from ui_utils import load_pixmap

# Qt
from qt import *
from nodevicesform_base import NoDevicesForm_base



class NoDevicesForm(NoDevicesForm_base):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        NoDevicesForm_base.__init__(self, parent, name, modal, fl)

        self.Icon.setPixmap(load_pixmap("warning.png", '32x32'))


    def CUPSButton_clicked(self):
        self.close()
        utils.openURL("http://localhost:631/admin")


    def ExitButton_clicked(self):
        self.close()


    def setupPushButton_clicked(self):
        self.close()

        if utils.which('hp-setup'):
            cmd = 'hp-setup -u'
        else:
            cmd = 'python ./setup.py -u'

        log.debug(cmd)
        utils.run(cmd)

        try:
            self.parent().RescanDevices()
        except Error:
            QMessageBox.critical(self,
                                    self.caption(),
                                    self.__tr("<b>An error occurred.</b><p>Please re-start the Device Manager and try again."),
                                    QMessageBox.Ok,
                                    QMessageBox.NoButton,
                                    QMessageBox.NoButton)


    def __tr(self,s,c = None):
        return qApp.translate("NoDevicesForm",s,c)
