# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/pluginform2_base.ui'
#
# Created: Thu May 22 15:17:47 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *


class PluginForm2_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("PluginForm2_base")


        PluginForm2_baseLayout = QGridLayout(self,1,1,11,6,"PluginForm2_baseLayout")

        self.titleTextLabel = QLabel(self,"titleTextLabel")

        PluginForm2_baseLayout.addMultiCellWidget(self.titleTextLabel,0,0,0,2)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        PluginForm2_baseLayout.addMultiCellWidget(self.line1,1,1,0,2)
        spacer8 = QSpacerItem(390,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        PluginForm2_baseLayout.addItem(spacer8,6,0)

        self.cancelPushButton = QPushButton(self,"cancelPushButton")

        PluginForm2_baseLayout.addWidget(self.cancelPushButton,6,2)

        self.actionPushButton = QPushButton(self,"actionPushButton")
        self.actionPushButton.setDefault(1)

        PluginForm2_baseLayout.addWidget(self.actionPushButton,6,1)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        PluginForm2_baseLayout.addMultiCellWidget(self.textLabel1,2,2,0,2)
        spacer11 = QSpacerItem(20,50,QSizePolicy.Minimum,QSizePolicy.Expanding)
        PluginForm2_baseLayout.addItem(spacer11,5,2)

        self.sourceGroup = QButtonGroup(self,"sourceGroup")
        self.sourceGroup.setColumnLayout(0,Qt.Vertical)
        self.sourceGroup.layout().setSpacing(6)
        self.sourceGroup.layout().setMargin(11)
        sourceGroupLayout = QGridLayout(self.sourceGroup.layout())
        sourceGroupLayout.setAlignment(Qt.AlignTop)

        self.radioButton5 = QRadioButton(self.sourceGroup,"radioButton5")
        self.sourceGroup.insert( self.radioButton5,1)

        sourceGroupLayout.addWidget(self.radioButton5,1,0)

        self.browsePushButton = QPushButton(self.sourceGroup,"browsePushButton")
        self.browsePushButton.setEnabled(0)

        sourceGroupLayout.addWidget(self.browsePushButton,2,1)

        self.radioButton4 = QRadioButton(self.sourceGroup,"radioButton4")
        self.radioButton4.setChecked(1)
        self.sourceGroup.insert( self.radioButton4,0)

        sourceGroupLayout.addWidget(self.radioButton4,0,0)

        self.pathLineEdit = QLineEdit(self.sourceGroup,"pathLineEdit")
        self.pathLineEdit.setEnabled(0)

        sourceGroupLayout.addWidget(self.pathLineEdit,2,0)

        PluginForm2_baseLayout.addMultiCellWidget(self.sourceGroup,4,4,0,2)
        spacer13 = QSpacerItem(20,21,QSizePolicy.Minimum,QSizePolicy.Expanding)
        PluginForm2_baseLayout.addItem(spacer13,3,0)

        self.languageChange()

        self.resize(QSize(585,375).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.sourceGroup,SIGNAL("clicked(int)"),self.sourceGroup_clicked)
        self.connect(self.browsePushButton,SIGNAL("clicked()"),self.browsePushButton_clicked)
        self.connect(self.pathLineEdit,SIGNAL("textChanged(const QString&)"),self.pathLineEdit_textChanged)
        self.connect(self.actionPushButton,SIGNAL("clicked()"),self.actionPushButton_clicked)
        self.connect(self.cancelPushButton,SIGNAL("clicked()"),self.cancelPushButton_clicked)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Plugin Download and Install"))
        self.titleTextLabel.setText(self.__tr("Driver Plug-in Install"))
        self.cancelPushButton.setText(self.__tr("Cancel"))
        self.actionPushButton.setText(self.__tr("Download and Install"))
        self.textLabel1.setText(self.__tr("You may download the plug-in directly from an HP authorized server, or, if you already have a copy of the file, you can specify a path to the file."))
        self.sourceGroup.setTitle(self.__tr("Plug-in Source"))
        self.radioButton5.setText(self.__tr("Use an exisiting copy of the plug-in file (advanced):"))
        self.browsePushButton.setText(self.__tr("Browse..."))
        self.radioButton4.setText(self.__tr("Download the plug-in from an HP authorized server (recommended)"))


    def sourceGroup_clicked(self,a0):
        print "PluginForm2_base.sourceGroup_clicked(int): Not implemented yet"

    def browsePushButton_clicked(self):
        print "PluginForm2_base.browsePushButton_clicked(): Not implemented yet"

    def pathLineEdit_textChanged(self,a0):
        print "PluginForm2_base.pathLineEdit_textChanged(const QString&): Not implemented yet"

    def actionPushButton_clicked(self):
        print "PluginForm2_base.actionPushButton_clicked(): Not implemented yet"

    def cancelPushButton_clicked(self):
        print "PluginForm2_base.cancelPushButton_clicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("PluginForm2_base",s,c)
