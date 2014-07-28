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
import sys
import os.path

# Qt
from qt import *

# Local
from base.g import *
from aboutdlg_base import AboutDlg_base
from ui_utils import load_pixmap


class AboutDlg(AboutDlg_base):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        AboutDlg_base.__init__(self,parent,name,modal,fl)

        self.pyPixmap.setPixmap(load_pixmap('powered_by_python.png'))
        self.osiPixmap.setPixmap(load_pixmap('opensource-75x65.png'))
        self.logoPixmap.setPixmap(load_pixmap('hp-tux-printer.png'))
