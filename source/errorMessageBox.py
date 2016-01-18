# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Scripts\Eclipse\TianD_KX_TOOL\source\errorMessageBox.ui'
#
# Created: Mon Jan 18 17:48:55 2016
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ErrorMessageBox(object):
    def setupUi(self, ErrorMessageBox):
        ErrorMessageBox.setObjectName(_fromUtf8("ErrorMessageBox"))
        ErrorMessageBox.resize(320, 120)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ErrorMessageBox.sizePolicy().hasHeightForWidth())
        ErrorMessageBox.setSizePolicy(sizePolicy)
        ErrorMessageBox.setMinimumSize(QtCore.QSize(320, 120))
        ErrorMessageBox.setMaximumSize(QtCore.QSize(320, 120))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("content/bullet_deny.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ErrorMessageBox.setWindowIcon(icon)
        ErrorMessageBox.setWindowOpacity(1.0)
        self.centralwidget = QtGui.QWidget(ErrorMessageBox)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 60, 200, 40))
        self.pushButton.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("ADMUI3Lg"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        ErrorMessageBox.setCentralWidget(self.centralwidget)

        self.retranslateUi(ErrorMessageBox)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), ErrorMessageBox.close)
        QtCore.QMetaObject.connectSlotsByName(ErrorMessageBox)

    def retranslateUi(self, ErrorMessageBox):
        ErrorMessageBox.setWindowTitle(_translate("ErrorMessageBox", "ErrorMessageBox", None))
        self.pushButton.setText(_translate("ErrorMessageBox", "去修改吧", None))

