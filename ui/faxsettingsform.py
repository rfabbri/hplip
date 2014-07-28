# -*- coding: utf-8 -*-
#
# (c) Copyright 2003-2009 Hewlett-Packard Development Company, L.P.
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



from qt import *
from faxsettingsform_base import FaxSettingsForm_base
from base.g import *
from base import device, pml, utils

class PhoneNumValidator(QValidator):
    def __init__(self, parent=None, name=None):
        QValidator.__init__(self, parent, name)

    def validate(self, input, pos):
        input = unicode(input)
        try:
            input = input.encode('ascii')
        except UnicodeEncodeError:
            return QValidator.Invalid, pos

        if not input:
            return QValidator.Acceptable, pos
        elif input[pos-1] not in '0123456789-(+) ':
            return QValidator.Invalid, pos
        elif len(input) > 50:
            return QValidator.Invalid, pos
        else:
            return QValidator.Acceptable, pos


class StationNameValidator(QValidator):
    def __init__(self, parent=None, name=None):
        QValidator.__init__(self, parent, name)

    def validate(self, input, pos):
        input = unicode(input)

        try:
            input = input.encode('ascii')
        except UnicodeEncodeError:
            return QValidator.Invalid, pos

        if not input:
            return QValidator.Acceptable, pos
        # TODO: Find valid chars for this field
        elif input != utils.printable(input):
            return QValidator.Invalid, pos
        elif len(input) > 50:
            return QValidator.Invalid, pos
        else:
            return QValidator.Acceptable, pos



class FaxSettingsForm(FaxSettingsForm_base):

    def __init__(self, dev, fax_num, name_co, parent = None,name = None,modal = 0,fl = 0):
        FaxSettingsForm_base.__init__(self,parent,name,modal,fl)
        self.dev = dev
        self.faxEdit.setValidator(PhoneNumValidator(self.faxEdit))
        self.nameEdit.setValidator(StationNameValidator(self.nameEdit))
        self.voiceEdit.setValidator(PhoneNumValidator(self.voiceEdit))
        self.faxEdit.setText(fax_num)
        self.nameEdit.setText(name_co)
        self.setOKButton(fax_num and name_co)
        self.voiceEdit.setText(QString(user_conf.get('fax', 'voice_phone')))
        self.emailEdit.setText(QString(user_conf.get('fax', 'email_address')))

    def faxEdit_textChanged(self,a0):
        self.setOKButton()

    def nameEdit_textChanged(self,a0):
        self.setOKButton()

    def setOKButton(self, toggle=None):
        if toggle is not None:
            self.pushButtonOK.setEnabled(bool(toggle))
        else:
            name = unicode(self.nameEdit.text())
            fax_num = unicode(self.faxEdit.text())
            self.pushButtonOK.setEnabled(bool(name and fax_num))

    def accept(self):
        # str() is OK here since the validators removed any non-ascii chars
        fax = str(self.faxEdit.text())
        log.debug(fax)
        name = str(self.nameEdit.text())
        log.debug(name)
        try:
            self.dev.setPML(pml.OID_FAX_LOCAL_PHONE_NUM, fax)
            self.dev.setPML(pml.OID_FAX_STATION_NAME, name)
        except Error:
            log.error("Error setting fax settings to device.")

        # TODO: This is a problem - user can enter non-ascii chars...
        # user config needs to be in utf-8 encoding (but its not right now)
        user_conf.set('fax', 'voice_phone', unicode(self.voiceEdit.text()).encode('utf-8'))
        user_conf.set('fax', 'email_address', unicode(self.emailEdit.text()).encode('utf-8'))
        FaxSettingsForm_base.accept(self)

