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

# Local
from base.g import *
from ui_utils import load_pixmap

# Qt
from qt import *


class AlignForm(QDialog):
    def __init__(self, parent, line_id, orientation, colors, line_count, 
                 choice_count, name = None, modal = 0, fl = 0):
        QDialog.__init__(self, parent, name, modal, fl)

        # line_id: 'A', 'B', etc.
        # orientation: 'v' or 'h'
        # colors: 'k' or 'c' or 'kc'
        # line_count: 2 or 3
        # choice_count: 5, 7, 9, 11, etc. (odd)
        mid_point = (choice_count+1)/2

        if not name:
            self.setProperty("name", QVariant("AlignForm"))

        AlignFormLayout = QGridLayout(self,1,1,11,6,"AlignFormLayout")

        #self.helpButton = QPushButton(self,"helpButton")

        #AlignFormLayout.addWidget(self.helpButton,1,0)

        self.CancelButton = QPushButton(self,"CancelButton")

        AlignFormLayout.addWidget(self.CancelButton,1,2)

        self.ContinueButton = QPushButton(self,"ContinueButton")

        AlignFormLayout.addWidget(self.ContinueButton,1,3)
        spacer1 = QSpacerItem(270,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        AlignFormLayout.addItem(spacer1,1,1)

        self.buttonGroup = QButtonGroup(self,"buttonGroup")
        self.buttonGroup.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup.layout().setSpacing(6)
        self.buttonGroup.layout().setMargin(11)

        buttonGroupLayout = QGridLayout(self.buttonGroup.layout())
        buttonGroupLayout.setAlignment(Qt.AlignTop)

        ChoiceLayout = QHBoxLayout(None,0,6,"ChoiceLayout")

        for x in range(1, choice_count+1):
            exec 'self.radioButton%d = QRadioButton( self.buttonGroup, "radioButton%d" )' % (x, x) 
            exec 'self.radioButton%d.setText( "%s%d" )' % (x, line_id, x) 
            if x == mid_point:
                exec 'self.radioButton%d.setChecked( 1 )' % x
            exec 'ChoiceLayout.addWidget( self.radioButton%d )' % x

        buttonGroupLayout.addMultiCellLayout(ChoiceLayout, 1, 1, 0, 1)

        self.Icon = QLabel(self.buttonGroup,"Icon")
        self.Icon.setProperty("sizePolicy",QVariant(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.Icon.sizePolicy().hasHeightForWidth())))
        self.Icon.setProperty("scaledContents",QVariant(QVariant(1,0)))

        buttonGroupLayout.addWidget(self.Icon,0,0)

        self.textLabel2_2 = QLabel(self.buttonGroup,"textLabel2_2")
        self.textLabel2_2.setProperty("alignment",QVariant(QLabel.WordBreak | QLabel.AlignVCenter))

        buttonGroupLayout.addWidget(self.textLabel2_2,0,1)

        AlignFormLayout.addMultiCellWidget(self.buttonGroup,0,0,0,3)

        self.languageChange()

        self.resize(QSize(608,222).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.CancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.ContinueButton,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.buttonGroup,SIGNAL("clicked(int)"),self.buttonGroup_clicked)

        self.Icon.setPixmap(load_pixmap('%s-%s-%d.png' % (orientation, colors, line_count), 'other'))

        self.buttonGroup.setTitle(line_id)

        self.value = (choice_count + 1) / 2

    def buttonGroup_clicked(self,a0):
        self.value = a0 + 1
        log.debug(self.value)

    def languageChange(self):
        self.setProperty("caption",QVariant(self.__tr("HP Device Manager - Alignment")))
        #self.helpButton.setProperty("text",QVariant(self.__tr("Help")))
        self.CancelButton.setProperty("text",QVariant(self.__tr("Cancel")))
        self.ContinueButton.setProperty("text",QVariant(self.__tr("Next >")))
        self.buttonGroup.setProperty("title",QVariant(self.__tr("")))
        self.textLabel2_2.setProperty("text",QVariant(self.__tr("Choose the set of lines where the line segments are <b>best</b> aligned.")))

    def __tr(self,s,c = None):
        return qApp.translate("AlignForm",s,c)
