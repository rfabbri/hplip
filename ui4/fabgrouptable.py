# -*- coding: utf-8 -*-
#
# (c) Copyright 2003-2007 Hewlett-Packard Development Company, L.P.
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

# Local
from base.g import *

# Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *



class FABGroupTable(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        
        self.db = None
        
        
    def setDatabase(self, db):
        self.db = db
        

    def dragMoveEvent(self, e):
        item = self.itemAt(e.pos())
        if item is not None:
            group = unicode(item.text())
            
            if group  == u'All':
                e.ignore()
                return

            names = unicode(e.mimeData().data(u'text/plain')).split(u'|')
            group_members = self.db.group_members(group)
            
            if not group_members:
                e.accept()
                return
            
            for n in names:
                if n not in group_members:
                   e.accept()
                   return
                
        e.ignore()
        
        
    def dropMimeData(self, row, col, data, action):
        items = unicode(data.data(u'text/plain')).split(u'|')
        self.emit(SIGNAL("namesAddedToGroup"), row, items)
        return False
        
        
    def mimeTypes(self):
        return QStringList([u'text/plain'])
        
        
