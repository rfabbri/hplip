# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dwelch/linux-imaging-and-printing/src/ui/imagepropertiesdlg_base.ui'
#
# Created: Fri Apr 1 14:51:29 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class ImagePropertiesDlg_base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ImagePropertiesDlg_base")


        ImagePropertiesDlg_baseLayout = QGridLayout(self,1,1,11,6,"ImagePropertiesDlg_baseLayout")

        self.textLabel6 = QLabel(self,"textLabel6")

        ImagePropertiesDlg_baseLayout.addWidget(self.textLabel6,3,0)

        self.textLabel8 = QLabel(self,"textLabel8")

        ImagePropertiesDlg_baseLayout.addWidget(self.textLabel8,4,0)

        self.textLabel10 = QLabel(self,"textLabel10")

        ImagePropertiesDlg_baseLayout.addWidget(self.textLabel10,2,0)

        self.EXifDataListView = QListView(self,"EXifDataListView")
        self.EXifDataListView.addColumn(self.__tr("EXIF Labels"))
        self.EXifDataListView.header().setResizeEnabled(0,self.EXifDataListView.header().count() - 1)
        self.EXifDataListView.addColumn(self.__tr("Contents "))
        self.EXifDataListView.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.EXifDataListView.sizePolicy().hasHeightForWidth()))
        self.EXifDataListView.setMinimumSize(QSize(400,100))
        self.EXifDataListView.setFrameShadow(QListView.Sunken)
        self.EXifDataListView.setResizeMode(QListView.AllColumns)

        ImagePropertiesDlg_baseLayout.addMultiCellWidget(self.EXifDataListView,5,5,0,2)

        self.LocationText = QLabel(self,"LocationText")

        ImagePropertiesDlg_baseLayout.addMultiCellWidget(self.LocationText,2,2,1,2)

        self.MimeTypeText = QLabel(self,"MimeTypeText")

        ImagePropertiesDlg_baseLayout.addMultiCellWidget(self.MimeTypeText,3,3,1,2)

        self.SizeText = QLabel(self,"SizeText")

        ImagePropertiesDlg_baseLayout.addMultiCellWidget(self.SizeText,4,4,1,2)

        self.FilenameText = QLabel(self,"FilenameText")

        ImagePropertiesDlg_baseLayout.addMultiCellWidget(self.FilenameText,0,0,0,2)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        ImagePropertiesDlg_baseLayout.addMultiCellWidget(self.line1,1,1,0,2)
        spacer3 = QSpacerItem(300,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        ImagePropertiesDlg_baseLayout.addMultiCell(spacer3,6,6,0,1)

        self.pushButton6 = QPushButton(self,"pushButton6")

        ImagePropertiesDlg_baseLayout.addWidget(self.pushButton6,6,2)

        self.languageChange()

        self.resize(QSize(431,388).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton6,SIGNAL("clicked()"),self.close)


    def languageChange(self):
        self.setCaption(self.__tr("Properties for"))
        self.textLabel6.setText(self.__tr("MIME Type:"))
        self.textLabel8.setText(self.__tr("Size:"))
        self.textLabel10.setText(self.__tr("Location:"))
        self.EXifDataListView.header().setLabel(0,self.__tr("EXIF Labels"))
        self.EXifDataListView.header().setLabel(1,self.__tr("Contents "))
        self.LocationText.setText(self.__tr("LOCATION"))
        self.MimeTypeText.setText(self.__tr("MIME TYPE"))
        self.SizeText.setText(self.__tr("SIZE"))
        self.FilenameText.setText(self.__tr("FILENAME"))
        self.pushButton6.setText(self.__tr("OK"))


    def ViewEXIFButton_clicked(self):
        print "ImagePropertiesDlg_base.ViewEXIFButton_clicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ImagePropertiesDlg_base",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ImagePropertiesDlg_base()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
