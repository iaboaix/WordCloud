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
        self.text_path = QtWidgets.QLineEdit(MainWindow)
        self.text_path.setMinimumSize(QtCore.QSize(0, 30))
        self.text_path.setDragEnabled(True)
        self.text_path.setObjectName("text_path")
        self.gridLayout.addWidget(self.text_path, 0, 0, 1, 3)
        self.load_text = QtWidgets.QPushButton(MainWindow)
        self.load_text.setObjectName("load_text")
        self.gridLayout.addWidget(self.load_text, 0, 3, 1, 1)
        self.change_setting = QtWidgets.QPushButton(MainWindow)
        self.change_setting.setObjectName("change_setting")
        self.gridLayout.addWidget(self.change_setting, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 3, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(MainWindow)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.chart_widget = QtWidgets.QWidget(MainWindow)
        self.chart_widget.setObjectName("chart_widget")
        self.horizontalLayout.addWidget(self.chart_widget)
        self.pic_show = QtWidgets.QLabel(MainWindow)
        self.pic_show.setText("")
        self.pic_show.setObjectName("pic_show")
        self.horizontalLayout.addWidget(self.pic_show)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 7)
        self.horizontalLayout.setStretch(2, 7)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.save_pic = QtWidgets.QPushButton(MainWindow)
        self.save_pic.setObjectName("save_pic")
        self.gridLayout.addWidget(self.save_pic, 1, 2, 1, 1)
        self.make_cloud = QtWidgets.QPushButton(MainWindow)
        self.make_cloud.setObjectName("make_cloud")
        self.gridLayout.addWidget(self.make_cloud, 1, 3, 1, 1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "词云生成器"))
        self.load_text.setText(_translate("MainWindow", "加载文本"))
        self.change_setting.setText(_translate("MainWindow", "调整配置"))
        self.label.setText(_translate("MainWindow", "版本号V1.0"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "词语"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "次数"))
        self.save_pic.setText(_translate("MainWindow", "保存图片"))
        self.make_cloud.setText(_translate("MainWindow", "开始生成"))

import source_rc
