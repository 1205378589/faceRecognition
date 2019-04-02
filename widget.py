#!/usr/bin/pyton3.6
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(930, 661)
        self.startBtn = QtWidgets.QPushButton(Form)
        self.startBtn.setGeometry(QtCore.QRect(20, 220, 89, 25))
        self.startBtn.setObjectName("startBtn")
        self.quitBtn = QtWidgets.QPushButton(Form)
        self.quitBtn.setGeometry(QtCore.QRect(20, 330, 89, 25))
        self.quitBtn.setObjectName("quitBtn")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(180, 40, 731, 591))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        self.quitBtn.clicked.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.startBtn.setText(_translate("Form", "开始"))
        self.quitBtn.setText(_translate("Form", "退出"))
        self.label.setText(_translate("Form", "TextLabel")) 

