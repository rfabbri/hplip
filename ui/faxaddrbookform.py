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

# Std Lib
import sys
import os
import os.path

# Local
from base.g import *
from base import utils
from ui_utils import load_pixmap

try:
    from fax import fax
except ImportError:
    # This can fail on Python < 2.3 due to the datetime module
    log.error("Fax address book disabled - Python 2.3+ required.")
    sys.exit(1)

# Qt
from qt import *
from faxaddrbookform_base import FaxAddrBookForm_base
from faxaddrbookeditform_base import FaxAddrBookEditForm_base
from faxaddrbookgroupsform_base import FaxAddrBookGroupsForm_base
from faxaddrbookgroupeditform_base import FaxAddrBookGroupEditForm_base

# globals
db = None

# ****************************************************************************

class AddressBookItem2(QListViewItem):

    def __init__(self, parent, entry):
        QListViewItem.__init__(self, parent)
        self.entry = entry
        self.setText(0, entry['name'])
        self.setText(1, entry['title'])
        self.setText(2, entry['firstname'])
        self.setText(3, entry['lastname'])
        self.setText(4, entry['fax'])
        self.setText(5, ', '.join(entry['groups']))
        self.setText(6, entry['notes'])

class GroupValidator(QValidator):
    def __init__(self, parent=None, name=None):
        QValidator.__init__(self, parent, name)

    def validate(self, input, pos):
        input = unicode(input)
        if input.find(u',') > 0:
            return QValidator.Invalid, pos
        elif len(input) > 50:
            return QValidator.Invalid, pos
        else:
            return QValidator.Acceptable, pos


class PhoneNumValidator(QValidator):
    def __init__(self, parent=None, name=None):
        QValidator.__init__(self, parent, name)

    def validate(self, input, pos):
        input = unicode(input)
        if not input:
            return QValidator.Acceptable, pos
        elif input[pos-1] not in u'0123456789-(+) *#':
            return QValidator.Invalid, pos
        elif len(input) > 50:
            return QValidator.Invalid, pos
        else:
            return QValidator.Acceptable, pos


# **************************************************************************** #

class FaxAddrBookGroupEditForm(FaxAddrBookGroupEditForm_base):
    """
        Called when clicking New... or Edit... from the Group Dialog
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        FaxAddrBookGroupEditForm_base.__init__(self,parent,name,modal,fl)
        self.edit_mode = False
        self.okButton.setEnabled(True)
        self.all_groups = db.get_all_groups()
        self.groupnameEdit.setValidator(GroupValidator(self.groupnameEdit))

    def setDlgData(self, group_name):
        self.edit_mode = True
        self.groupnameEdit.setText(group_name)
        self.groupnameEdit.setReadOnly(True)
        self.setEntries(group_name)

    def setEntries(self, group_name=''):
        self.entriesListView.clear()
        all_entries = db.get_all_records()

        for e, v in all_entries.items():
            i = QCheckListItem(self.entriesListView, e, QCheckListItem.CheckBox)

            if group_name and group_name in v['groups']:
                i.setState(QCheckListItem.On)

        self.CheckOKButton()


    def getDlgData(self):
        group_name = unicode(self.groupnameEdit.text())
        entries = []

        i = self.entriesListView.firstChild()

        while i is not None:
            if i.isOn():
                entries.append(unicode(i.text()))

            i = i.itemBelow()

        return group_name, entries

    def groupnameEdit_textChanged(self,a0):
        self.CheckOKButton()

    def entriesListView_clicked(self,a0):
        self.CheckOKButton()

    def CheckOKButton(self):
        group_name = unicode(self.groupnameEdit.text())

        if not group_name or \
            (not self.edit_mode and group_name in self.all_groups):

            self.okButton.setEnabled(False)
            return

        i = self.entriesListView.firstChild()

        while i is not None:
            if i.isOn():
                break

            i = i.itemBelow()

        else:
            self.okButton.setEnabled(False)
            return

        self.okButton.setEnabled(True)

    def __tr(self,s,c = None):
        return qApp.translate("FaxAddrBookGroupEditForm",s,c)


# **************************************************************************** #

class FaxAddrBookGroupsForm(FaxAddrBookGroupsForm_base):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        FaxAddrBookGroupsForm_base.__init__(self,parent,name,modal,fl)
        self.current = None
        QTimer.singleShot(0, self.InitialUpdate)

    def InitialUpdate(self):
        self.UpdateList()

    def UpdateList(self):
        self.groupListView.clear()
        first_rec = None
        all_groups = db.get_all_groups()
        if all_groups:

            for group in all_groups:
                i = QListViewItem(self.groupListView, group,
                                  u', '.join(db.group_members(group)))

                if first_rec is None:
                    first_rec = i

            self.groupListView.setCurrentItem(i)
            self.current = i

            self.editButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

        else:
            self.editButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def newButton_clicked(self):
        dlg = FaxAddrBookGroupEditForm(self)
        dlg.setEntries()
        if dlg.exec_loop() == QDialog.Accepted:
            group_name, entries = dlg.getDlgData()
            db.update_groups(group_name, entries)
            self.UpdateList()

    def editButton_clicked(self):
        dlg = FaxAddrBookGroupEditForm(self)
        group_name = unicode(self.current.text(0))
        dlg.setDlgData(group_name)
        if dlg.exec_loop() == QDialog.Accepted:
            group_name, entries = dlg.getDlgData()
            db.update_groups(group_name, entries)
            self.UpdateList()


    def deleteButton_clicked(self):
        x = QMessageBox.critical(self,
                                 self.caption(),
                                 self.__tr("<b>Annoying Confirmation: Are you sure you want to delete this group?</b>"),
                                  QMessageBox.Yes,
                                  QMessageBox.No | QMessageBox.Default,
                                  QMessageBox.NoButton)
        if x == QMessageBox.Yes:
            db.delete_group(unicode(self.current.text(0)))
            self.UpdateList()

    def groupListView_currentChanged(self, a0):
        self.current = a0

    def groupListView_doubleClicked(self, a0):
        self.editButton_clicked()

    def groupListView_rightButtonClicked(self, item, pos, a2):
        popup = QPopupMenu(self)

        popup.insertItem(self.__tr("New..."), self.newButton_clicked)

        if item is not None:
            popup.insertItem(self.__tr("Edit..."), self.editButton_clicked)
            popup.insertItem(self.__tr("Delete..."), self.deleteButton_clicked)

        popup.insertSeparator()
        popup.insertItem(self.__tr("Refresh List"), self.UpdateList)
        popup.popup(pos)

    def __tr(self,s,c = None):
        return qApp.translate("FaxAddrBookGroupsForm",s,c)


# **************************************************************************** #


class FaxAddrBookEditForm(FaxAddrBookEditForm_base):
    def __init__(self, editing=True, parent = None,name = None,modal = 0,fl = 0):
        FaxAddrBookEditForm_base.__init__(self,parent,name,modal,fl)
        self.editing = editing
        self.faxEdit.setValidator(PhoneNumValidator(self.faxEdit))
        self.initial_nickname = ''
        self.OKButton.setEnabled(self.editing)

    def setDlgData(self, name, title, firstname, lastname, fax, group_list, notes):
        self.initial_nickname = name
        self.name = name
        self.titleEdit.setText(title)
        self.firstnameEdit.setText(firstname)
        self.lastnameEdit.setText(lastname)
        self.faxEdit.setText(fax)
        self.notesEdit.setText(notes)
        self.nicknameEdit.setText(name)
        self.setGroups(group_list)

    def setGroups(self, entry_groups=[]):
        self.groupListView.clear()
        for g in db.get_all_groups():
            i = QCheckListItem(self.groupListView, g, QCheckListItem.CheckBox)

            if g in entry_groups:
                i.setState(QCheckListItem.On)

    def getDlgData(self):
        in_groups = []
        i = self.groupListView.firstChild()

        while i is not None:
            if i.isOn():
                in_groups.append(unicode(i.text()))
            i = i.itemBelow()

        return {'name': unicode(self.nicknameEdit.text()),
                'title': unicode(self.titleEdit.text()),
                'firstname': unicode(self.firstnameEdit.text()),
                'lastname': unicode(self.lastnameEdit.text()),
                'fax': unicode(self.faxEdit.text()),
                'groups': in_groups,
                'notes': unicode(self.notesEdit.text())}

    def firstnameEdit_textChanged(self,a0):
        pass

    def lastnameEdit_textChanged(self,a0):
        pass

    def nicknameEdit_textChanged(self, nickname):
        self.CheckOKButton(nickname, None)

    def faxEdit_textChanged(self, fax):
        self.CheckOKButton(None, fax)

    def CheckOKButton(self, nickname=None, fax=None):
        if nickname is None:
            nickname = unicode(self.nicknameEdit.text())

        if fax is None:
            fax = unicode(self.faxEdit.text())

        ok = bool(len(nickname) and len(fax))

        if nickname:
            all_entries = db.get_all_records()
            for e, v in all_entries.items():
                if nickname == e and nickname != self.initial_nickname:
                    ok = False

        self.OKButton.setEnabled(ok)

    def __tr(self,s,c = None):
        return qApp.translate("FaxAddrBookEditForm",s,c)

# **************************************************************************** #

class FaxAddrBookForm(FaxAddrBookForm_base):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        FaxAddrBookForm_base.__init__(self,parent,name,modal,fl)

        self.setIcon(load_pixmap('hp_logo', '128x128'))

        global db
        db =  fax.FaxAddressBook()
        self.init_problem = False

        QTimer.singleShot(0, self.InitialUpdate)


    def InitialUpdate(self):
        if self.init_problem:
            self.close()
            return

        self.UpdateList()

    def UpdateList(self):
        self.addressListView.clear()
        first_rec = None
        all_entries = db.get_all_records()
        log.debug("Number of records is: %d" % len(all_entries))

        if all_entries:
            for e, v in all_entries.items():

                if v['name'].startswith('__'):
                    continue

                i = AddressBookItem2(self.addressListView, v)

                if first_rec is None:
                    first_rec = i

            self.addressListView.setCurrentItem(i)
            self.current = i

            self.editButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

        else:
            self.editButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

    def groupButton_clicked(self):
        FaxAddrBookGroupsForm(self).exec_loop()
        self.sendUpdateEvent()
        self.UpdateList()

    def newButton_clicked(self):
        dlg = FaxAddrBookEditForm(False, self)
        dlg.setGroups()
        if dlg.exec_loop() == QDialog.Accepted:
            d = dlg.getDlgData()
            db.set(**d)
            self.sendUpdateEvent()
            self.UpdateList()

    def editButton_clicked(self):
        dlg = FaxAddrBookEditForm(True, self)
        c = self.current.entry
        dlg.setDlgData(c['name'], c['title'], c['firstname'],
            c['lastname'], c['fax'], c['groups'], c['notes'])
        prev_name = c['name']
        if dlg.exec_loop() == QDialog.Accepted:
            d = dlg.getDlgData()

            if prev_name != d['name']:
                db.delete(prev_name)

            db.set(**d)
            self.sendUpdateEvent()
            self.UpdateList()


    def deleteButton_clicked(self):
        if QMessageBox.critical(self,
             self.caption(),
             self.__tr("<b>Annoying Confirmation: Are you sure you want to delete this address book entry?</b>"),
              QMessageBox.Yes,
              QMessageBox.No | QMessageBox.Default,
              QMessageBox.NoButton) == QMessageBox.Yes:
            db.delete(self.current.entry['name'])
            self.UpdateList()
            self.sendUpdateEvent()


    def addressListView_rightButtonClicked(self, item, pos, a2):
        popup = QPopupMenu(self)
        popup.insertItem(self.__tr("New..."), self.newButton_clicked)
        if item is not None:
            popup.insertItem(self.__tr("Edit..."), self.editButton_clicked)
            popup.insertItem(self.__tr("Delete..."), self.deleteButton_clicked)

        popup.insertSeparator()
        popup.insertItem(self.__tr("Refresh List"), self.UpdateList)
        popup.popup(pos)

    def addressListView_doubleClicked(self,a0):
        self.editButton_clicked()

    def addressListView_currentChanged(self,item):
        self.current = item

    def FailureUI(self, error_text):
        log.error(unicode(error_text).replace("<b>", "").replace("</b>", "").replace("<p>", " "))
        QMessageBox.critical(self,
                             self.caption(),
                             QString(error_text),
                              QMessageBox.Ok,
                              QMessageBox.NoButton,
                              QMessageBox.NoButton)

    def __tr(self,s,c = None):
        return qApp.translate("FaxAddrBookForm",s,c)

    def accept(self):
        self.sendUpdateEvent()

        FaxAddrBookForm_base.accept(self)

    def sendUpdateEvent(self):
        pass # TODO:

    def importPushButton_clicked(self):
        dlg = QFileDialog(user_conf.workingDirectory(), "LDIF (*.ldif *.ldi);;vCard (*.vcf)", None, None, True)

        dlg.setCaption("openfile")
        dlg.setMode(QFileDialog.ExistingFile)
        dlg.show()

        if dlg.exec_loop() == QDialog.Accepted:
                result = str(dlg.selectedFile())
                working_directory = unicode(dlg.dir().absPath())
                log.debug("result: %s" % result)
                user_conf.setWorkingDirectory(working_directory)

                if result:
                    if result.endswith('.vcf'):
                        ok, error_str = db.import_vcard(result)
                    else:
                        ok, error_str = db.import_ldif(result)

                    if not ok:
                        self.FailureUI(error_str)

                    else:
                        self.UpdateList()

