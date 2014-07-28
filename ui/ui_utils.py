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
# Thanks to Henrique M. Holschuh <hmh@debian.org> for various security patches
#

# Std Lib
import os.path

# Local
from base.g import *
from base import utils

# Qt
try:
    from qt import *
except ImportError:
    log.error("Unable to load qt3. Is python-qt3 installed?")

# TODO: Cache pixmaps

def load_pixmap(name, subdir=None, resize_to=None): # Qt3 only
    name = ''.join([os.path.splitext(name)[0], '.png'])
    
    if subdir is None:
        dir = prop.image_dir
        ldir = os.path.join(os.getcwd(), 'data', 'images')
    else:
        dir = os.path.join(prop.image_dir, subdir)
        ldir = os.path.join(os.getcwd(), 'data', 'images', subdir)
    
    for d in [dir, ldir]:
        f = os.path.join(d, name)
    
        if os.path.exists(f):
            if resize_to is not None:
                img = QImage(f)
                pm = QPixmap()
                pm.convertFromImage(img.smoothScale(*resize_to), 0)
                return pm
            else:
                return QPixmap(f)
        
        for w in utils.walkFiles(dir, recurse=True, abs_paths=True, return_folders=False, pattern=name):
            if resize_to is not None:
                img = QImage(w)
                pm = QPixmap()
                pm.convertFromImage(img.smoothScale(*resize_to), 0)
                return pm
            else:
                return QPixmap(w)

    log.error("Pixmap '%s' not found!" % name)
    return QPixmap()
    
