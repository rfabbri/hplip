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

# Local
from base.g import *
from base import utils
from prnt import cups

# Qt
from qt import *

class PINValidator(QValidator):
    def __init__(self, parent=None, name=None):
        QValidator.__init__(self, parent, name)

    def validate(self, input, pos):
        for x in unicode(input)[pos-1:]:
            if x not in u'0123456789':
                return QValidator.Invalid, pos

        return QValidator.Acceptable, pos 
     
class TextValidator(QValidator):
    def __init__(self, parent=None, name=None):
        QValidator.__init__(self, parent, name)

    def validate(self, input, pos):
        for x in unicode(input)[pos-1:]:
            if x not in u'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -':
                return QValidator.Invalid, pos

        return QValidator.Acceptable, pos 


class JobStorageMixin(object):  
    def __init__(self):
        pass
 
    def initJobStorage(self, print_settings_mode=False):
        self.print_settings_mode = print_settings_mode
        self.job_storage_mode = JOB_STORAGE_TYPE_OFF
        self.job_storage_pin = u"0000"
        self.job_storage_use_pin = False
        self.job_storage_username = unicode(prop.username[:16])
        self.job_storage_auto_username = True
        self.job_storage_jobname = u"Untitled"
        self.job_storage_auto_jobname = True
        self.job_storage_job_exist = 0
        
        
    def addJobStorage(self, current_options=None):
        self.addJobStorageMode()
        self.addJobStoragePIN()
        self.addJobStorageUsername()
        self.addJobStorageID()
        self.addJobStorageIDExists()
        self.jobStorageDisable()
        
        if current_options is None:
            cups.resetOptions()
            cups.openPPD(self.cur_printer)
            current_options = dict(cups.getOptions())
            cups.closePPD()

        self.job_storage_pin = unicode(current_options.get('HOLDKEY', '0000')[:4])
        self.jobStoragePINEdit.setText(self.job_storage_pin)
        
        self.job_storage_username = unicode(current_options.get('USERNAME', prop.username)[:16])
        self.jobStorageUsernameEdit.setText(self.job_storage_username)
        
        self.job_storage_jobname = unicode(current_options.get('JOBNAME', u"Untitled")[:16])
        self.jobStorageIDEdit.setText(self.job_storage_jobname)
        
        hold = current_options.get('HOLD', 'OFF')
        holdtype = current_options.get('HOLDTYPE', 'PUBLIC')

        if hold == 'OFF':
            self.job_storage_mode = JOB_STORAGE_TYPE_OFF
        
        elif hold == 'ON':
            if holdtype == 'PUBLIC':
                self.job_storage_mode = JOB_STORAGE_TYPE_QUICK_COPY
            
            else: # 'PRIVATE'
                self.job_storage_mode = JOB_STORAGE_TYPE_PERSONAL
                self.job_storage_use_pin = True
            
        elif hold == 'PROOF':
            if holdtype == 'PUBLIC':
                self.job_storage_mode = JOB_STORAGE_TYPE_PROOF_AND_HOLD
            else:
                self.job_storage_mode = JOB_STORAGE_TYPE_PERSONAL
                self.job_storage_use_pin = True
            
        elif hold == 'STORE':
            self.job_storage_mode = JOB_STORAGE_TYPE_STORE
            self.job_storage_use_pin = (holdtype == 'PRIVATE')
        
        self.jobStorageModeComboBox.setCurrentItem(self.job_storage_mode)
        self.jobStorageModeDefaultPushButton.setEnabled(self.job_storage_mode != JOB_STORAGE_TYPE_OFF)
        self.setModeTooltip()
        self.setPrinterOptionHold()

        duplicate = current_options.get('DUPLICATEJOB', 'REPLACE')
        
        if duplicate == 'REPLACE':
            self.job_storage_job_exist = 0
        else:
            self.job_storage_job_exist = 1
            
        self.jobStorageIDExistsComboBox.setCurrentItem(self.job_storage_job_exist)
        self.setPrinterOptionIDExists()
        
        #
        
        if self.job_storage_mode == JOB_STORAGE_TYPE_OFF:
            self.jobStorageDisable()
        else:
            self.jobStorageUserJobEnable()
            self.setPrinterOptionID()
            self.setPrinterOptionPIN()
            self.setPrinterOptionUsername()
                
        self.jobStoragePINButtonGroup.setButton(self.job_storage_use_pin)
        self.jobStoragePINEnable(self.job_storage_mode in (JOB_STORAGE_TYPE_PERSONAL, JOB_STORAGE_TYPE_STORE))
        
        
    def addJobStorageMode(self):
        widget = self.getWidget()

        layout34 = QHBoxLayout(widget,5,10,"layout34")

        self.jobStorageModeLabel = QLabel(widget,"jobStorageModeLabel")
        layout34.addWidget(self.jobStorageModeLabel)
        spacer20_4 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout34.addItem(spacer20_4)

        self.jobStorageModeComboBox = QComboBox(0,widget,"jobStorageModeComboBox")
        layout34.addWidget(self.jobStorageModeComboBox)

        self.jobStorageModeDefaultPushButton = QPushButton(widget,"pagesetDefaultPushButton")
        layout34.addWidget(self.jobStorageModeDefaultPushButton)

        self.jobStorageModeLabel.setText(self.__tr("Job Storage Mode:"))
        self.jobStorageModeComboBox.clear()
        self.jobStorageModeComboBox.insertItem(self.__tr("Off"))
        self.jobStorageModeComboBox.insertItem(self.__tr("Proof and Hold"))
        self.jobStorageModeComboBox.insertItem(self.__tr("Personal/Private Job"))
        self.jobStorageModeComboBox.insertItem(self.__tr("Quick Copy"))
        self.jobStorageModeComboBox.insertItem(self.__tr("Stored Job"))
        
        self.jobStorageModeDefaultPushButton.setText(self.__tr("Default"))
        self.jobStorageModeDefaultPushButton.setEnabled(False)

        self.connect(self.jobStorageModeComboBox, SIGNAL("activated(int)"), self.jobStorageModeComboBox_activated)
        self.connect(self.jobStorageModeDefaultPushButton, SIGNAL("clicked()"), self.jobStorageModeDefaultPushButton_clicked)

        self.addWidget(widget, "job_storage_mode")
        
    def jobStorageModeComboBox_activated(self, a):
        #print a
        self.job_storage_mode = a
        self.jobStorageModeDefaultPushButton.setEnabled(a != JOB_STORAGE_TYPE_OFF)
        
        if a == JOB_STORAGE_TYPE_OFF:
            #print "off!"
            self.jobStorageDisable()
        else:
            self.jobStorageUserJobEnable()
            
        self.setPrinterOptionHold()        
        self.jobStoragePINEnable(a in (JOB_STORAGE_TYPE_PERSONAL, JOB_STORAGE_TYPE_STORE))
        self.setModeTooltip()
        

    def setModeTooltip(self):
        QToolTip.remove(self.jobStorageModeComboBox)
        
        if self.job_storage_mode == JOB_STORAGE_TYPE_OFF:
            QToolTip.add(self.jobStorageModeComboBox,
                self.__tr("""Your job will be printed but not stored on the printer."""))
        
        elif self.job_storage_mode == JOB_STORAGE_TYPE_PERSONAL:
            QToolTip.add(self.jobStorageModeComboBox,
                self.__tr("""Your job will be stored on the printer and nothing will be printed until you request the job from the printer's control panel.<br>Once the job is printed, it will automatically be removed from the printer's job storage. For Private print jobs, add a 4-digit PIN."""))
                
        elif self.job_storage_mode == JOB_STORAGE_TYPE_PROOF_AND_HOLD:
            QToolTip.add(self.jobStorageModeComboBox,
                self.__tr("""When multiples copies are requested, the first copy will be printed.<br>The remaining copies will be held on the printer until you release them using the printer's control panel."""))
                
        elif self.job_storage_mode == JOB_STORAGE_TYPE_QUICK_COPY:
            QToolTip.add(self.jobStorageModeComboBox,
                self.__tr("""After your job prints, you can use the printer's control panel to print additional copies of your job."""))
                
        elif self.job_storage_mode == JOB_STORAGE_TYPE_STORE:
            QToolTip.add(self.jobStorageModeComboBox,
                self.__tr("""Your job will not immediately print, but instead be stored in the printer. <br>You can request copies of this job from the printer's control panel. Use this for storage of forms and other common or shared documents."""))
            
    
    def setPrinterOptionHold(self):
        if self.print_settings_mode:
            if self.job_storage_mode == JOB_STORAGE_TYPE_OFF:
                #print "off!!!"
                self.setPrinterOption('HOLD', 'OFF')
                self.removePrinterOption('HOLDTYPE')
                self.removePrinterOption('HOLDKEY')
                self.removePrinterOption('USERNAME')
                self.removePrinterOption('JOBNAME')
                self.removePrinterOption('DUPLICATEJOB')
                
            elif self.job_storage_mode == JOB_STORAGE_TYPE_PROOF_AND_HOLD:
                #print "proof"
                self.job_storage_use_pin = False
                self.setPrinterOption('HOLD', 'PROOF')
                self.removePrinterOption('HOLDTYPE')
                self.removePrinterOption('HOLDKEY')
            
            elif self.job_storage_mode == JOB_STORAGE_TYPE_PERSONAL: 
                #print "personal"
                #self.setPrinterOption('HOLDTYPE', 'PRIVATE')
                
                if self.job_storage_use_pin:
                    self.setPrinterOption('HOLD', 'ON')
                    self.setPrinterOption('HOLDTYPE', 'PRIVATE')
                else:
                    self.setPrinterOption('HOLD', 'PROOF')
                    self.setPrinterOption('HOLDTYPE', 'PUBLIC')
                    self.removePrinterOption('HOLDKEY')
                    
            
            elif self.job_storage_mode == JOB_STORAGE_TYPE_QUICK_COPY:
                #print "qc"
                self.job_storage_use_pin = False
                self.setPrinterOption('HOLD', 'ON')
                self.setPrinterOption('HOLDTYPE', 'PUBLIC')
                self.removePrinterOption('HOLDKEY')
            
            elif self.job_storage_mode == JOB_STORAGE_TYPE_STORE:
                #print "store"
                
                self.setPrinterOption('HOLD', 'STORE')
                
                if self.job_storage_use_pin:
                    self.setPrinterOption('HOLDTYPE', 'PRIVATE')
                else:
                    self.removePrinterOption('HOLDTYPE')
                    self.removePrinterOption('HOLDKEY')
        
        
    def jobStorageModeDefaultPushButton_clicked(self):
        self.jobStorageModeComboBox.setCurrentItem(0)
        self.job_storage_mode = JOB_STORAGE_TYPE_OFF
        self.setPrinterOptionHold()
        self.setModeTooltip()
    
    def jobStorageDisable(self): # Off: Turn off all options
        self.jobStorageModeDefaultPushButton.setEnabled(False)
        self.jobStoragePINEnable(False)
        self.jobStorageUserJobEnable(False)
        #self.setPrinterOptionHold()
        
    def jobStoragePINEnable(self, e=True): # PIN On/Off
        t = e and self.jobStoragePINButtonGroup.selectedId() == 1
        self.jobStoragePINButtonGroup.setEnabled(e)
        self.jobStoragePINEdit.setEnabled(t)
        self.jobStoragePINDefaultPushButton.setEnabled(t)
        self.setPrinterOptionPIN()
        
    def jobStorageUserJobEnable(self, e=True): # Username/Job ID/Job ID Exists On/Off
        t = e and self.jobStorageUsernameButtonGroup.selectedId() == 1
        self.jobStorageUsernameButtonGroup.setEnabled(e)
        self.jobStorageUsernameDefaultPushButton.setEnabled(t)
        self.jobStorageUsernameEdit.setEnabled(t)
        if e: self.setPrinterOptionUsername()
        
        t = e and self.jobStorageIDButtonGroup.selectedId() == 1
        self.jobStorageIDButtonGroup.setEnabled(e)
        self.jobStorageIDDefaultPushButton.setEnabled(t)
        self.jobStorageIDEdit.setEnabled(t)
        if e: self.setPrinterOptionID()

        t = e and self.jobStorageIDExistsComboBox.currentItem() == 1
        self.jobStorageIDExistsComboBox.setEnabled(e)
        self.jobStorageIDExistsDefaultPushButton.setEnabled(t)
        if e: self.setPrinterOptionIDExists()

        
    # PIN
    
        
    def addJobStoragePIN(self):
        widget = self.getWidget()

        layout39 = QGridLayout(widget,1,1,5,10,"layout39")

        self.jobStoragePINEdit = QLineEdit(widget,"self.jobStoragePINEdit")
        self.jobStoragePINEdit.setMaxLength(4)
        self.jobStoragePINEdit.setInputMask(QString("9999"))
        self.jobStoragePINEdit.setText(self.job_storage_pin)
        layout39.addWidget(self.jobStoragePINEdit,0,3)

        spacer20_2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout39.addItem(spacer20_2,0,1)

        textLabel5_2 = QLabel(widget,"textLabel5_2")
        layout39.addWidget(textLabel5_2,0,0)

        self.jobStoragePINDefaultPushButton = QPushButton(widget,"jobStoragePINDefaultPushButton")
        layout39.addWidget(self.jobStoragePINDefaultPushButton,0,4)

        self.jobStoragePINButtonGroup = QButtonGroup(widget,"self.jobStoragePINButtonGroup")
        self.jobStoragePINButtonGroup.setLineWidth(0)
        self.jobStoragePINButtonGroup.setColumnLayout(0,Qt.Vertical)
        self.jobStoragePINButtonGroup.layout().setSpacing(0)
        self.jobStoragePINButtonGroup.layout().setMargin(0)
        self.jobStoragePINButtonGroupLayout = QGridLayout(self.jobStoragePINButtonGroup.layout())
        self.jobStoragePINButtonGroupLayout.setAlignment(Qt.AlignTop)

        radioButton3_2 = QRadioButton(self.jobStoragePINButtonGroup,"radioButton3_2")
        radioButton3_2.setChecked(1)
        self.jobStoragePINButtonGroup.insert( radioButton3_2,0)
        self.jobStoragePINButtonGroupLayout.addWidget(radioButton3_2,0,0)

        radioButton4_2 = QRadioButton(self.jobStoragePINButtonGroup,"radioButton4_2")
        self.jobStoragePINButtonGroup.insert( radioButton4_2,1)
        self.jobStoragePINButtonGroupLayout.addWidget(radioButton4_2,0,1)

        layout39.addWidget(self.jobStoragePINButtonGroup,0,2)

        self.bg = self.jobStoragePINEdit.paletteBackgroundColor()
        self.invalid_page_range = False

        self.jobStoragePINEdit.setValidator(PINValidator(self.jobStoragePINEdit))

        textLabel5_2.setText(self.__tr("Make Job Private (use PIN to print):"))
        radioButton3_2.setText(self.__tr("Public/Off"))
        radioButton4_2.setText(self.__tr("Private/Use PIN:"))

        self.jobStoragePINDefaultPushButton.setText(self.__tr("Default"))

        self.connect(self.jobStoragePINButtonGroup, SIGNAL("clicked(int)"), self.jobStoragePINButtonGroup_clicked)
        self.connect(self.jobStoragePINEdit,SIGNAL("lostFocus()"),self.jobStoragePINEdit_lostFocus)
        self.connect(self.jobStoragePINEdit,SIGNAL("textChanged(const QString&)"),self.jobStoragePINEdit_textChanged)
        self.connect(self.jobStoragePINDefaultPushButton, SIGNAL("clicked()"), self.jobStoragePINDefaultPushButton_clicked)

        self.addWidget(widget, "job_storage_pin")
        
    def jobStoragePINButtonGroup_clicked(self, a):
        if a == 0: # Public/Off
            self.jobStoragePINDefaultPushButton.setEnabled(False)
            self.jobStoragePINEdit.setEnabled(False)
            self.job_storage_use_pin = False
            self.job_storage_pin = u"0000"
            self.setPrinterOptionPIN()
            
        else: # On/Private/Use PIN
            self.jobStoragePINDefaultPushButton.setEnabled(True)
            self.jobStoragePINEdit.setEnabled(True)
            self.job_storage_use_pin = True
            self.job_storage_pin = unicode(self.jobStoragePINEdit.text())
            self.setPrinterOptionPIN()
                            
    def setPrinterOptionPIN(self):
        if self.print_settings_mode :
            if self.job_storage_use_pin:
                                
                self.setPrinterOption('HOLDKEY', self.job_storage_pin.encode('ascii'))
                #self.setPrinterOption('HOLD', 'ON')
            else:
                self.removePrinterOption('HOLDKEY')
                #self.setPrinterOption('HOLD', 'PROOF')
            
    
    def jobStoragePINEdit_lostFocus(self):
        #self.setPrinterOptionPIN()
        pass
        
    def jobStoragePINEdit_textChanged(self, a):
        self.job_storage_pin = unicode(a)
        self.setPrinterOptionPIN()
        
    def jobStoragePINDefaultPushButton_clicked(self):
        self.jobStoragePINButtonGroup.setButton(0)
        self.jobStoragePINDefaultPushButton.setEnabled(False)
        self.jobStoragePINEdit.setEnabled(False)
        self.job_storage_use_pin = False

    # Username    

    def addJobStorageUsername(self):
        widget = self.getWidget()

        layout39 = QGridLayout(widget,1,1,5,10,"layout39")

        self.jobStorageUsernameEdit = QLineEdit(widget,"self.jobStorageUsernameEdit")
        self.jobStorageUsernameEdit.setMaxLength(16)
        self.jobStorageUsernameEdit.setText(self.job_storage_username)
        layout39.addWidget(self.jobStorageUsernameEdit,0,3)
        
        spacer20_2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout39.addItem(spacer20_2,0,1)

        textLabel5_2 = QLabel(widget,"textLabel5_2")
        layout39.addWidget(textLabel5_2,0,0)

        self.jobStorageUsernameDefaultPushButton = QPushButton(widget,"jobStorageUsernameDefaultPushButton")
        layout39.addWidget(self.jobStorageUsernameDefaultPushButton,0,4)

        self.jobStorageUsernameButtonGroup = QButtonGroup(widget,"self.jobStorageUsernameButtonGroup")
        self.jobStorageUsernameButtonGroup.setLineWidth(0)
        self.jobStorageUsernameButtonGroup.setColumnLayout(0,Qt.Vertical)
        self.jobStorageUsernameButtonGroup.layout().setSpacing(0)
        self.jobStorageUsernameButtonGroup.layout().setMargin(0)
        self.jobStorageUsernameButtonGroupLayout = QGridLayout(self.jobStorageUsernameButtonGroup.layout())
        self.jobStorageUsernameButtonGroupLayout.setAlignment(Qt.AlignTop)

        radioButton3_2 = QRadioButton(self.jobStorageUsernameButtonGroup,"radioButton3_2")
        radioButton3_2.setChecked(1)
        self.jobStorageUsernameButtonGroup.insert( radioButton3_2,0)
        self.jobStorageUsernameButtonGroupLayout.addWidget(radioButton3_2,0,0)

        radioButton4_2 = QRadioButton(self.jobStorageUsernameButtonGroup,"radioButton4_2")
        self.jobStorageUsernameButtonGroup.insert( radioButton4_2,1)
        self.jobStorageUsernameButtonGroupLayout.addWidget(radioButton4_2,0,1)

        layout39.addWidget(self.jobStorageUsernameButtonGroup,0,2)

        self.bg = self.jobStorageUsernameEdit.paletteBackgroundColor()
        self.invalid_page_range = False

        self.jobStorageUsernameEdit.setValidator(TextValidator(self.jobStorageUsernameEdit))

        textLabel5_2.setText(self.__tr("User name (for job identification):"))
        radioButton3_2.setText(self.__tr("Automatic"))
        radioButton4_2.setText(self.__tr("Custom:"))

        self.jobStorageUsernameDefaultPushButton.setText(self.__tr("Default"))

        self.connect(self.jobStorageUsernameButtonGroup, SIGNAL("clicked(int)"), self.jobStorageUsernameButtonGroup_clicked)
        self.connect(self.jobStorageUsernameEdit,SIGNAL("lostFocus()"),self.jobStorageUsernameEdit_lostFocus)
        self.connect(self.jobStorageUsernameEdit,SIGNAL("textChanged(const QString&)"),self.jobStorageUsernameEdit_textChanged)
        self.connect(self.jobStorageUsernameDefaultPushButton, SIGNAL("clicked()"), self.jobStorageUsernameDefaultPushButton_clicked)

        self.addWidget(widget, "job_storage_username")
        
    def jobStorageUsernameButtonGroup_clicked(self, a):
        if a == 0: # Automatic
            self.jobStorageUsernameDefaultPushButton.setEnabled(False)
            self.jobStorageUsernameEdit.setEnabled(False)
            self.job_storage_auto_username = True
            self.job_storage_username = unicode(prop.username[:16])
            self.setPrinterOptionUsername()
        
        else: # Custom
            self.jobStorageUsernameDefaultPushButton.setEnabled(True)
            self.jobStorageUsernameEdit.setEnabled(True)
            self.job_storage_auto_username = False
            self.job_storage_username = unicode(self.jobStorageUsernameEdit.text())
            self.setPrinterOptionUsername()
            
    def jobStorageUsernameEdit_lostFocus(self):
        #self.setPrinterOptionUsername()
        pass
        
    def jobStorageUsernameEdit_textChanged(self, a):
        self.job_storage_username = unicode(a)
        self.setPrinterOptionUsername()
        
    def jobStorageUsernameDefaultPushButton_clicked(self):
        self.jobStorageUsernameButtonGroup.setButton(0)
        self.jobStorageUsernameDefaultPushButton.setEnabled(False)
        self.jobStorageUsernameEdit.setEnabled(False)
        self.job_storage_auto_username = True
        self.job_storage_username = unicode(prop.username[:16])
        self.setPrinterOptionUsername()
        
    def setPrinterOptionUsername(self):
        if self.print_settings_mode:
            self.setPrinterOption('USERNAME', self.job_storage_username.encode('ascii').replace(' ', '_'))
        

    # Job ID    

    def addJobStorageID(self):
        widget = self.getWidget()

        layout39 = QGridLayout(widget,1,1,5,10,"layout39")

        self.jobStorageIDEdit = QLineEdit(widget,"self.jobStorageIDEdit")
        self.jobStorageIDEdit.setMaxLength(16)
        self.jobStorageIDEdit.setText(self.job_storage_jobname)
        layout39.addWidget(self.jobStorageIDEdit,0,3)

        spacer20_2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout39.addItem(spacer20_2,0,1)

        textLabel5_2 = QLabel(widget,"textLabel5_2")
        layout39.addWidget(textLabel5_2,0,0)

        self.jobStorageIDDefaultPushButton = QPushButton(widget,"jobStorageIDDefaultPushButton")
        layout39.addWidget(self.jobStorageIDDefaultPushButton,0,4)

        self.jobStorageIDButtonGroup = QButtonGroup(widget,"self.jobStorageIDButtonGroup")
        self.jobStorageIDButtonGroup.setLineWidth(0)
        self.jobStorageIDButtonGroup.setColumnLayout(0,Qt.Vertical)
        self.jobStorageIDButtonGroup.layout().setSpacing(0)
        self.jobStorageIDButtonGroup.layout().setMargin(0)
        self.jobStorageIDButtonGroupLayout = QGridLayout(self.jobStorageIDButtonGroup.layout())
        self.jobStorageIDButtonGroupLayout.setAlignment(Qt.AlignTop)

        radioButton3_2 = QRadioButton(self.jobStorageIDButtonGroup,"radioButton3_2")
        radioButton3_2.setChecked(1)
        self.jobStorageIDButtonGroup.insert( radioButton3_2,0)
        self.jobStorageIDButtonGroupLayout.addWidget(radioButton3_2,0,0)

        radioButton4_2 = QRadioButton(self.jobStorageIDButtonGroup,"radioButton4_2")
        self.jobStorageIDButtonGroup.insert( radioButton4_2,1)
        self.jobStorageIDButtonGroupLayout.addWidget(radioButton4_2,0,1)

        layout39.addWidget(self.jobStorageIDButtonGroup,0,2)

        self.bg = self.jobStorageIDEdit.paletteBackgroundColor()
        self.invalid_page_range = False

        self.jobStorageIDEdit.setValidator(TextValidator(self.jobStorageIDEdit))

        textLabel5_2.setText(self.__tr("Job name (for job identification):"))
        radioButton3_2.setText(self.__tr("Automatic"))
        radioButton4_2.setText(self.__tr("Custom:"))

        self.jobStorageIDDefaultPushButton.setText(self.__tr("Default"))

        self.connect(self.jobStorageIDButtonGroup, SIGNAL("clicked(int)"), self.jobStorageIDButtonGroup_clicked)
        self.connect(self.jobStorageIDEdit,SIGNAL("lostFocus()"),self.jobStorageIDEdit_lostFocus)
        self.connect(self.jobStorageIDEdit,SIGNAL("textChanged(const QString&)"),self.jobStorageIDEdit_textChanged)
        self.connect(self.jobStorageIDDefaultPushButton, SIGNAL("clicked()"), self.jobStorageIDDefaultPushButton_clicked)

        self.addWidget(widget, "job_storage_ID")
        
    def jobStorageIDButtonGroup_clicked(self, a):
        if a == 0: # Automatic
            self.jobStorageIDDefaultPushButton.setEnabled(False)
            self.jobStorageIDEdit.setEnabled(False)
            self.job_storage_auto_jobname = True
            self.job_storage_jobname = u"Untitled"
            self.setPrinterOptionID()
            
        else: # Custom
            self.jobStorageIDDefaultPushButton.setEnabled(True)
            self.jobStorageIDEdit.setEnabled(True)
            self.job_storage_auto_jobname = False
            self.job_storage_jobname = unicode(self.jobStorageIDEdit.text())
            self.setPrinterOptionID()
        
    def jobStorageIDEdit_lostFocus(self):
        #self.setPrinterOptionID()
        pass
        
    def jobStorageIDEdit_textChanged(self, a):
        self.job_storage_jobname = unicode(a)
        self.setPrinterOptionID()
                
    def jobStorageIDDefaultPushButton_clicked(self):
        self.jobStorageIDButtonGroup.setButton(0)
        self.jobStorageIDDefaultPushButton.setEnabled(False)
        self.jobStorageIDEdit.setEnabled(False)
        self.job_storage_auto_jobname = True
        self.job_storage_jobname = u"Untitled"
        self.setPrinterOptionID()
        
    def setPrinterOptionID(self):
        if self.print_settings_mode:
            self.setPrinterOption('JOBNAME', self.job_storage_jobname.encode('ascii').replace(' ', '_'))

    # Job ID Exists

    def addJobStorageIDExists(self):
        widget = self.getWidget()

        layout34 = QHBoxLayout(widget,5,10,"layout34")

        self.jobStorageIDExistsLabel = QLabel(widget,"jobStorageIDExistsLabel")
        layout34.addWidget(self.jobStorageIDExistsLabel)
        spacer20_4 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout34.addItem(spacer20_4)

        self.jobStorageIDExistsComboBox = QComboBox(0,widget,"jobStorageIDExistsComboBox")
        layout34.addWidget(self.jobStorageIDExistsComboBox)

        self.jobStorageIDExistsDefaultPushButton = QPushButton(widget,"pagesetDefaultPushButton")
        layout34.addWidget(self.jobStorageIDExistsDefaultPushButton)

        self.jobStorageIDExistsLabel.setText(self.__tr("If Job Name already exists:"))
        self.jobStorageIDExistsComboBox.clear()
        self.jobStorageIDExistsComboBox.insertItem(self.__tr("Replace existing job"))
        self.jobStorageIDExistsComboBox.insertItem(self.__tr("Use Job Name + (1-99)"))
        
        self.jobStorageIDExistsDefaultPushButton.setText(self.__tr("Default"))

        self.connect(self.jobStorageIDExistsComboBox, SIGNAL("activated(int)"), self.jobStorageIDExistsComboBox_activated)
        self.connect(self.jobStorageIDExistsDefaultPushButton, SIGNAL("clicked()"), self.jobStorageIDExistsDefaultPushButton_clicked)

        self.addWidget(widget, "job_storage_id_exists")
        
    def jobStorageIDExistsComboBox_activated(self, a):
        self.jobStorageIDExistsDefaultPushButton.setEnabled(a==1)
        self.job_storage_job_exist = a
        self.setPrinterOptionIDExists()
        
    def jobStorageIDExistsDefaultPushButton_clicked(self):
        self.jobStorageIDExistsComboBox.setCurrentItem(0)
        self.jobStorageIDExistsDefaultPushButton.setEnabled(False)
        self.job_storage_job_exist = 0
        self.setPrinterOptionIDExists()
        
    def setPrinterOptionIDExists(self):
        if self.print_settings_mode:
            if self.job_storage_job_exist == 0:
                self.setPrinterOption('DUPLICATEJOB', 'REPLACE')
            else:
                self.setPrinterOption('DUPLICATEJOB', 'APPEND')

    def __tr(self,s,c = None):
        return qApp.translate("JobStorage",s,c)
   
