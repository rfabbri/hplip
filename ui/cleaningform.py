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
from cleaningform_base import CleaningForm_base


class CleaningForm(CleaningForm_base):
    def __init__(self, parent, dev, cleaning_level, name=None, modal=0, fl=0):
        CleaningForm_base.__init__(self, parent, name, modal, fl)
        self.dev = dev

        text = unicode(self.CleaningText.text())
        self.CleaningText.setText(text % str(cleaning_level + 1))

        text = unicode(self.Continue.text())
        self.Continue.setText(text % str(cleaning_level + 1))

        text = unicode(self.CleaningTitle.text())
        self.CleaningTitle.setText(text % str(cleaning_level))

        self.Icon.setPixmap(load_pixmap('clean.png', 'other'))

        self.check_timer = QTimer(self, "CheckTimer")
        self.connect(self.check_timer, SIGNAL('timeout()'), self.CheckTimerTimeout)

        self.check_timer.start(3000)

    def CheckTimerTimeout(self):
        if self.dev.isIdleAndNoError():
            self.Continue.setEnabled(True)
            self.check_timer.stop()

