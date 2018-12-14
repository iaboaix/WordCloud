# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1143, 793)
        self.gridLayout = QtWidgets.QGridLayout(MainWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.load_text = QtWidgets.QPushButton(MainWindow)
        self.load_text.setObjectName("load_text")
        self.gridLayout.addWidget(self.load_text, 0, 4, 1, 1)
        self.pic_show = QtWidgets.QLabel(MainWindow)
        self.pic_show.setText("")
        self.pic_show.setObjectName("pic_show")
        self.gridLayout.addWidget(self.pic_show, 2, 0, 1, 6)
        self.make_cloud = QtWidgets.QPushButton(MainWindow)
        self.make_cloud.setObjectName("make_cloud")
        self.gridLayout.addWidget(self.make_cloud, 1, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.change_setting = QtWidgets.QPushButton(MainWindow)
        self.change_setting.setObjectName("change_setting")
        self.gridLayout.addWidget(self.change_setting, 1, 0, 1, 1)
        self.save_pic = QtWidgets.QPushButton(MainWindow)
        self.save_pic.setObjectName("save_pic")
        self.gridLayout.addWidget(self.save_pic, 1, 3, 1, 1)
        self.text_path = QtWidgets.QLineEdit(MainWindow)
        self.text_path.setMinimumSize(QtCore.QSize(0, 30))
        self.text_path.setDragEnabled(True)
        self.text_path.setObjectName("text_path")
        self.gridLayout.addWidget(self.text_path, 0, 0, 1, 4)
        self.label = QtWidgets.QLabel(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 4, 1, 1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "词云生成器"))
        self.load_text.setText(_translate("MainWindow", "加载文本"))
        self.make_cloud.setText(_translate("MainWindow", "开始生成"))
        self.change_setting.setText(_translate("MainWindow", "调整配置"))
        self.save_pic.setText(_translate("MainWindow", "保存图片"))
        self.label.setText(_translate("MainWindow", "版本号V1.0"))

import source_rc
