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

import sys
from qt import *
from imagepropertiesdlg_base import ImagePropertiesDlg_base

class ImagePropertiesDlg(ImagePropertiesDlg_base):
    def __init__(self, filename, location, mimetype, size, exif_info={}, parent = None,name = None,modal = 0,fl = 0):
        ImagePropertiesDlg_base.__init__(self,parent,name,modal,fl)

        self.setCaption('Properties for ' + filename)
        self.FilenameText.setText('<b>' + filename + '</b>')
        self.LocationText.setText(location)
        self.MimeTypeText.setText(mimetype)
        self.SizeText.setText(size)
        if exif_info:
            for k in exif_info:
                kk = k.lower()
                if kk != "jpegthumbnail":
                    #print repr(k), repr(exif_info[k])
                    QListViewItem(self.EXifDataListView, k, str(exif_info[k]))




