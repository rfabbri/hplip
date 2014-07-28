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
from base import device
import sys
from qt import *

class ChoosePrinterDlg(QDialog):
    def __init__(self, printers, back_end_filter=['hp'], parent = None,name = None,modal = 0,fl = 0, show_uris=True):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ChooseDeviceDlg")

        self.device_uri = ''
        self.printer_name = ''
        self.back_end_filter = back_end_filter

        ChooseDeviceDlg_Layout = QGridLayout(self,1,1,6,6,"ChooseDeviceDlg_Layout")

        self.OKButton = QPushButton(self,"OKButton")

        ChooseDeviceDlg_Layout.addWidget(self.OKButton,2,2)

        self.CancelButton = QPushButton(self,"CancelButton")

        ChooseDeviceDlg_Layout.addWidget(self.CancelButton,2,1)
        spacer1 = QSpacerItem(391,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        ChooseDeviceDlg_Layout.addItem(spacer1,2,0)
        spacer2 = QSpacerItem(20,290,QSizePolicy.Minimum,QSizePolicy.Expanding)
        ChooseDeviceDlg_Layout.addItem(spacer2,1,0)

        self.DevicesButtonGroup = QButtonGroup(self,"DevicesButtonGroup")
        self.DevicesButtonGroup.setColumnLayout(0,Qt.Vertical)
        self.DevicesButtonGroup.layout().setSpacing(6)
        self.DevicesButtonGroup.layout().setMargin(6)
        DevicesButtonGroupLayout = QGridLayout(self.DevicesButtonGroup.layout())
        DevicesButtonGroupLayout.setAlignment(Qt.AlignTop)

        self.radio_buttons = {}

        self.printer_index, x = {}, 0
        for p in printers:
            try:
                back_end, is_hp, bus, model, serial, dev_file, host, zc, port = \
                    device.parseDeviceURI(p.device_uri)

            except Error:
                continue

            if back_end in back_end_filter:
                self.printer_index[x] = (p.name, p.device_uri)
                x += 1


        for y in range(len(self.printer_index)):
            if y == 0:
                self.device_uri = self.printer_index[y][1]
                self.printer_name = self.printer_index[y][0]

            self.radio_buttons[y] = QRadioButton(self.DevicesButtonGroup,"radioButton%d" % y)

            if show_uris:
                self.radio_buttons[y].setText("%s  (%s)" % self.printer_index[y])
            else:
                self.radio_buttons[y].setText(self.printer_index[y])

            DevicesButtonGroupLayout.addWidget(self.radio_buttons[y], y, 0)

        self.radio_buttons[0].setChecked(1)

        ChooseDeviceDlg_Layout.addMultiCellWidget(self.DevicesButtonGroup,0,0,0,2)

        self.languageChange()

        self.resize(QSize(592,112).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.OKButton,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.CancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.DevicesButtonGroup,SIGNAL("clicked(int)"),self.DevicesButtonGroup_clicked)

    def languageChange(self):
        self.setCaption(self.__tr("Choose Device"))
        self.OKButton.setText(self.__tr("OK"))
        self.CancelButton.setText(self.__tr("Cancel"))

        if 'hp' in self.back_end_filter and 'hpfax' in self.back_end_filter:
            self.DevicesButtonGroup.setTitle(self.__tr("Available Devices:"))
        elif 'hp' in self.back_end_filter:
            self.DevicesButtonGroup.setTitle(self.__tr("Available Printers:"))
        elif 'hpfax' in self.back_end_filter:
            self.DevicesButtonGroup.setTitle(self.__tr("Available Faxes:"))
        else:
            self.DevicesButtonGroup.setTitle(self.__tr("Available Devices:"))

    def __tr(self,s,c = None):
        return qApp.translate("ChooseDeviceDlg",s,c)

    def DevicesButtonGroup_clicked(self,a0):
        for p in self.printer_index:
            pp = self.printer_index[p]
            if unicode(self.radio_buttons[a0].text()).startswith(pp[0]):
                self.device_uri = pp[1]
                self.printer_name = pp[0]
                break



class ChoosePrinterDlg2(QDialog):
    def __init__(self, printers, parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        self.printers = printers

        if not name:
            self.setName("ChooseDeviceDlg2")

        ChooseDeviceDlg_Layout = QGridLayout(self,1,1,6,6,"ChooseDeviceDlg_Layout")

        self.OKButton = QPushButton(self,"OKButton")

        ChooseDeviceDlg_Layout.addWidget(self.OKButton,2,2)

        self.CancelButton = QPushButton(self,"CancelButton")

        ChooseDeviceDlg_Layout.addWidget(self.CancelButton,2,1)
        spacer1 = QSpacerItem(391,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        ChooseDeviceDlg_Layout.addItem(spacer1,2,0)
        spacer2 = QSpacerItem(20,290,QSizePolicy.Minimum,QSizePolicy.Expanding)
        ChooseDeviceDlg_Layout.addItem(spacer2,1,0)

        self.DevicesButtonGroup = QButtonGroup(self,"DevicesButtonGroup")
        self.DevicesButtonGroup.setColumnLayout(0,Qt.Vertical)
        self.DevicesButtonGroup.layout().setSpacing(6)
        self.DevicesButtonGroup.layout().setMargin(6)
        DevicesButtonGroupLayout = QGridLayout(self.DevicesButtonGroup.layout())
        DevicesButtonGroupLayout.setAlignment(Qt.AlignTop)

        self.radio_buttons = {}

        for y in range(len(self.printers)):
            if y == 0:
                self.printer_name = self.printers[0]

            self.radio_buttons[y] = QRadioButton(self.DevicesButtonGroup,"radioButton%d" % y)
            self.radio_buttons[y].setText(self.printers[y])
            DevicesButtonGroupLayout.addWidget(self.radio_buttons[y], y, 0)

        self.radio_buttons[0].setChecked(1)

        ChooseDeviceDlg_Layout.addMultiCellWidget(self.DevicesButtonGroup,0,0,0,2)

        self.languageChange()

        self.resize(QSize(592,112).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.OKButton,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.CancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.DevicesButtonGroup,SIGNAL("clicked(int)"),self.DevicesButtonGroup_clicked)

    def languageChange(self):
        self.setCaption(self.__tr("Choose Printer"))
        self.OKButton.setText(self.__tr("OK"))
        self.CancelButton.setText(self.__tr("Cancel"))

        self.DevicesButtonGroup.setTitle(self.__tr("Printers:"))

    def __tr(self,s,c = None):
        return qApp.translate("ChooseDeviceDlg2",s,c)

    def DevicesButtonGroup_clicked(self,a0):
        self.printer_name = self.printers[a0]
