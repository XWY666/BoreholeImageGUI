# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PIL import ImageGrab
import sys,os
import numpy as np
import threading
from AC import *

X=0
Y=0
#记录截屏区域坐标

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(713, 543)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 340, 428))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.Imagelabel = MyLabel(self.scrollAreaWidgetContents)
        self.Imagelabel.setText("")
        self.Imagelabel.setObjectName("Imagelabel")
        self.gridLayout.addWidget(self.Imagelabel, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        spacerItem = QtWidgets.QSpacerItem(339, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 713, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuCustom = QtWidgets.QMenu(self.menubar)
        self.menuCustom.setObjectName("menuCustom")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.ac_import = QtWidgets.QAction(MainWindow)
        self.ac_import.setObjectName("ac_import")
        self.ac_export = QtWidgets.QAction(MainWindow)
        self.ac_export.setObjectName("ac_export")
        self.ac_ZoomIn = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../ZoomIn.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_ZoomIn.setIcon(icon)
        self.ac_ZoomIn.setObjectName("ac_ZoomIn")
        self.ac_ZoomOut = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../ZoomOut.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_ZoomOut.setIcon(icon1)
        self.ac_ZoomOut.setObjectName("ac_ZoomOut")
        self.ac_ScreenShot = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../ScreenShot.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ac_ScreenShot.setIcon(icon2)
        self.ac_ScreenShot.setObjectName("ac_ScreenShot")
        self.menuFile.addAction(self.ac_import)
        self.menuFile.addAction(self.ac_export)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCustom.menuAction())
        self.toolBar.addAction(self.ac_ZoomIn)
        self.toolBar.addAction(self.ac_ZoomOut)
        self.toolBar.addAction(self.ac_ScreenShot)

        self.retranslateUi(MainWindow)
        self.ac_import.triggered.connect(MainWindow.openImage)
        self.ac_ZoomIn.triggered.connect(MainWindow.ZoomIn)
        self.ac_ZoomOut.triggered.connect(MainWindow.ZoomOut)
        self.ac_ScreenShot.triggered.connect(MainWindow.ScreenShot)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuCustom.setTitle(_translate("MainWindow", "Custom"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.ac_import.setText(_translate("MainWindow", "import"))
        self.ac_export.setText(_translate("MainWindow", "export"))
        self.ac_ZoomIn.setText(_translate("MainWindow", "Zoom_in"))
        self.ac_ZoomOut.setText(_translate("MainWindow", "Zoom_out"))
        self.ac_ScreenShot.setText(_translate("MainWindow", "Screen_shot"))



#class MyScrollArea(QtWidgets.QScrollArea):
#    def cursor(cls, self):
#        print("a")
#        return super().cursor(self)

class MyLabel(QtWidgets.QLabel):
    IsShot = False
    global X
    global Y
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    pic = []
    #鼠标点击事件
    #def mousePressEvent(self,event):
    #    self.flag = True
    #    self.x0 = event.x()
    #    self.y0 = event.y()
    ##鼠标释放事件
    #def mouseReleaseEvent(self,event):
    #    self.flag = False
    #    if self.IsShot:
    #        reply = QMessageBox.question(self,'Message','Do you want to use this shot?',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
    #        if reply == QMessageBox.Yes:
    #            Mat = np.asarray(self.pic)
    #            print(Mat.shape)
    #            phero,Acc,th = RunAntColony(Mat)
    ##鼠标移动事件
    #def mouseMoveEvent(self,event):
    #    if self.flag:
    #        self.x1 = event.x()
    #        self.y1 = event.y()
    #        self.update()
    #绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        self.update()
        

        if self.IsShot:
            rect = QRect(min(self.x0,self.x1), min(self.y0,self.y1), abs(self.x1-self.x0), abs(self.y1-self.y0))
            painter = QPainter(self)
            painter.setPen(QPen(Qt.blue,1,Qt.SolidLine))
            painter.drawRect(rect)
            self.pic = ImageGrab.grab((X+min(self.x0,self.x1)+1.5, Y+min(self.y0,self.y1)+1.5, X+max(self.x0,self.x1), Y+max(self.y0,self.y1)))
            self.pic = self.pic.convert('L')           

class MyApp(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyApp,self).__init__(parent)
        self.setupUi(self)
        self.image = QPixmap()
        self.Imagelabel.X = self.x()
        self.Imagelabel.Y = self.y()
        self.update()

    def ScreenShot(self):
        self.Imagelabel.IsShot = not self.Imagelabel.IsShot

        if self.Imagelabel.IsShot:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("../ScreenShot_pressed.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ac_ScreenShot.setIcon(icon)
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("../ScreenShot.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ac_ScreenShot.setIcon(icon)

    def ZoomIn(self):
        if self.image.isNull():
            return

        scale = 1.2
        img = self.image.toImage()
        #img = QImage(self.imgName)
        self.image = QPixmap.fromImage(img.scaled(img.size()*scale, Qt.IgnoreAspectRatio))
        self.Imagelabel.setPixmap(self.image)

    def ZoomOut(self):
        if self.image.isNull():
            return

        scale = 0.8
        img = self.image.toImage()

        self.image = QPixmap.fromImage(img.scaled(img.size()*scale, Qt.IgnoreAspectRatio))
        self.Imagelabel.setPixmap(self.image)    

    def openImage(self):
        self.imgName,imgType= QFileDialog.getOpenFileName(self,
                                    "打开图片",
                                    "",
                                    " *.jpg;;*.png;;*.jpeg;;*.bmp;;All Files (*)")

        
        #利用qlabel显示图片
        self.image = QPixmap(self.imgName)
        self.Imagelabel.setPixmap(self.image)

        #self.Imagelabel.adjustSize()
        self.Imagelabel.setScaledContents(True)

def fun_timer():
    global timer
    global X,Y
    #截屏区域坐标为：窗口客户区相对于屏幕左上角的坐标+滚动区域相对于客户区的坐标+Label相对于滚动区域的坐标（y坐标还需考虑toolbar和menubar高度）-横/纵ScrollBar滚动距离
    X=window.geometry().x()+window.scrollArea.geometry().x()+window.Imagelabel.geometry().x()-window.scrollArea.horizontalScrollBar().value()
    Y=window.geometry().y()+window.scrollArea.geometry().y()+window.Imagelabel.geometry().y()+window.toolBar.height()+window.menubar.height()-window.scrollArea.verticalScrollBar().value()

    timer = threading.Timer(0.5, fun_timer)
    timer.start()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()

    #timer = threading.Timer(0.5, fun_timer)
    #timer.start()

    app.exec_()