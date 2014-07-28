# -*- coding: utf-8 -*-
#
# (c) Copyright 2003-2008 Hewlett-Packard Development Company, L.P.
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
from fax import coverpages
from ui_utils import load_pixmap

# Qt
from qt import *
from coverpageform_base import CoverpageForm_base



class CoverpageForm(CoverpageForm_base):
    def __init__(self, cover_page_name='', preserve_formatting=False, parent=None, name=None, modal=0, fl=0):
        CoverpageForm_base.__init__(self, parent, name, modal, fl)

        self.preserve_formatting = preserve_formatting
        self.preserveFormattingCheckBox.setChecked(preserve_formatting)
        self.prevCoverpageButton.setPixmap(load_pixmap('prev', '16x16'))
        self.nextCoverpageButton.setPixmap(load_pixmap('next', '16x16'))
        self.coverpage_list = coverpages.COVERPAGES.keys()

        if cover_page_name:
            self.coverpage_index = self.coverpage_list.index(cover_page_name)
        else:    
            self.coverpage_index = 0

        self.setCoverpage()


    def setCoverpage(self, inc=0):
        self.coverpage_index += inc

        if self.coverpage_index > len(self.coverpage_list) - 1:
            self.coverpage_index = 0

        elif self.coverpage_index < 0:
            self.coverpage_index = len(self.coverpage_list) - 1

        self.coverpage_name = self.coverpage_list[self.coverpage_index]
        self.data = coverpages.COVERPAGES[self.coverpage_name]

        self.coverpagePixmap.setPixmap(load_pixmap(self.data[1], 'other'))

        
    def prevCoverpageButton_clicked(self):
        self.setCoverpage(-1)

        
    def nextCoverpageButton_clicked(self):
        self.setCoverpage(1)

        
    def preserveFormattingCheckBox_toggled(self,a0):
        self.preserve_formatting = bool(a0)

        
    def __tr(self,s,c = None):
        return qApp.translate("CoverpageForm_base",s,c)
