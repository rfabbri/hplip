# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'align13form_base.ui'
#
# Created: Tue Oct 14 13:35:16 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *


class Align13Form_Base(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Align13Form_base")



        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setGeometry(QRect(30,20,540,140))

        self.OKButton = QPushButton(self,"OKButton")
        self.OKButton.setGeometry(QRect(490,180,80,30))

        self.languageChange()

        self.resize(QSize(600,232).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.OKButton,SIGNAL("clicked()"),self.accept)


    def languageChange(self):
        self.setCaption(self.__tr("HP Device Manager - Align Print Cartridges"))
        self.textLabel2.setText(self.__tr("<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'DejaVu Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Follow these steps to complete the alignment:</span> </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">1.</span> Place the alignment page, with the printed side facing down, on the scanner. </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">2.</span> Press the <span style=\" font-style:italic;\">Enter</span> or <span style=\" font-style:italic;\">Scan</span> button on the printer. </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">3.</span> \"Alignment Complete\" will be displayed when the process is finished (on some models with a front panel display) or the green light that was blinking during the process will stop blinking and remain green (on some models without a front panel display).</p></body></html>"))
        self.OKButton.setText(self.__tr("OK"))


    def __tr(self,s,c = None):
        return qApp.translate("Align13Form_Base",s,c)
