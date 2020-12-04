# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SetPara.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class Ui_DialogSet(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(32, 32))
        self.tabWidget.setElideMode(QtCore.Qt.ElideMiddle)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textEdit1 = QtWidgets.QTextEdit(self.tab1)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit1.setFont(font)
        self.textEdit1.setObjectName("textEdit1")
        self.gridLayout_2.addWidget(self.textEdit1, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab1, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab2)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit2 = QtWidgets.QTextEdit(self.tab2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit2.setFont(font)
        self.textEdit2.setObjectName("textEdit2")
        self.gridLayout.addWidget(self.textEdit2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab2, "")
        self.tab3 = QtWidgets.QWidget()
        self.tab3.setObjectName("tab3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textEdit3 = QtWidgets.QTextEdit(self.tab3)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit3.setFont(font)
        self.textEdit3.setObjectName("textEdit3")
        self.gridLayout_3.addWidget(self.textEdit3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab3, "")
        self.tab4 = QtWidgets.QWidget()
        self.tab4.setObjectName("tab4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textEdit4 = QtWidgets.QTextEdit(self.tab4)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit4.setFont(font)
        self.textEdit4.setObjectName("textEdit4")
        self.gridLayout_4.addWidget(self.textEdit4, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab4, "")
        self.verticalLayout.addWidget(self.tabWidget)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(3)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowStaysOnTopHint
                                            | Qt.WindowCloseButtonHint)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.textEdit1.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:400;\"><br /></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("Dialog", "关键字"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("Dialog", "算术运算符"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3), _translate("Dialog", "关系运算符"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab4), _translate("Dialog", "分界符"))

