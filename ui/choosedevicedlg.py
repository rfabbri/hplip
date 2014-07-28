# -*- coding: utf-8 -*-
#
# (c) Copyright 2001-2009 Hewlett-Packard Development Company, L.P.
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
import sys
from qt import *

class ChooseDeviceDlg(QDialog):
    def __init__(self, devices, parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ChooseDeviceDlg")

        self.device_uri = ''

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

        last_used_device_uri = user_conf.get('last_used', 'device_uri')
        last_used_index = None

        for y in range(len(devices)):
            self.radio_buttons[y] = QRadioButton(self.DevicesButtonGroup,"radioButton%d" % y)
            self.radio_buttons[y].setText(devices[y][0])

            if devices[y][0] == last_used_device_uri:
                last_used_index = y
                self.device_uri = devices[y][0]

            DevicesButtonGroupLayout.addWidget(self.radio_buttons[y], y, 0)

        if last_used_index is not None:
            self.radio_buttons[last_used_index].setChecked(1)
        else:
            self.radio_buttons[0].setChecked(1)
            self.device_uri = devices[0][0]

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
        self.DevicesButtonGroup.setTitle(self.__tr("Available Devices:"))


    def __tr(self,s,c = None):
        return qApp.translate("ChooseDeviceDlg",s,c)

    def DevicesButtonGroup_clicked(self,a0):
        self.device_uri = unicode(self.radio_buttons[a0].text())

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ChooseDeviceDlg()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
