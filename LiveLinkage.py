#version 20
from PyQt5 import QtCore, QtGui, QtWidgets
import kernel_Litxtre as kernel

class UI_Start():
    global mode
    global cam
    cam = 0
    mode = 0

    class Ui_DefaultWindow:
        def setupUi(self, DefaultWindow):
            DefaultWindow.setObjectName("DefaultWindow")
            DefaultWindow.resize(411, 160)
            self.pushButton = QtWidgets.QPushButton(DefaultWindow)
            self.pushButton.setGeometry(QtCore.QRect(10, 50, 161, 61))
            self.pushButton.setObjectName("pushButton")
            self.pushButton.clicked.connect(self.call_Kernel)

            self.lcdNumber = QtWidgets.QLCDNumber(DefaultWindow)
            self.lcdNumber.setGeometry(QtCore.QRect(180, 30, 221, 81))
            self.lcdNumber.setObjectName("lcdNumber")


            self.label = QtWidgets.QLabel(DefaultWindow)
            self.label.setGeometry(QtCore.QRect(180, 10, 221, 16))
            self.label.setObjectName("label")

            self.label_2 = QtWidgets.QLabel(DefaultWindow)
            self.label_2.setGeometry(QtCore.QRect(150, 130, 250, 21))
            self.label_2.setObjectName("label_2")


            self.camSpin = QtWidgets.QSpinBox(DefaultWindow)
            self.camSpin.setGeometry(QtCore.QRect(70, 20, 31, 22))
            self.camSpin.setObjectName("camSpin")
            self.camSpin.valueChanged.connect(self.camChange)

            self.label_3 = QtWidgets.QLabel(DefaultWindow)
            self.label_3.setGeometry(QtCore.QRect(10, 20, 61, 21))
            self.label_3.setObjectName("label_3")


            self.retranslateUi(DefaultWindow)
            QtCore.QMetaObject.connectSlotsByName(DefaultWindow)

        def retranslateUi(self, DefaultWindow):
            _translate = QtCore.QCoreApplication.translate
            DefaultWindow.setWindowTitle(_translate("DefaultWindow", "HRMonitor Beta"))
            self.pushButton.setText(_translate("DefaultWindow", "Start"))
            self.label.setText(_translate("DefaultWindow", "BPM"))
            #self.checkBox.setText(_translate("DefaultWindow", "略過動態效能追蹤"))
            #self.pushButton_2.setText(_translate("DefaultWindow", "Benchmark"))
            self.label_2.setText(_translate("DefaultWindow", ""))
            self.label_3.setText(_translate("DefaultWindow", "選擇相機"))
            #self.label_4.setText(_translate("DefaultWindow", "測試模式：0 = Fast | 1 = Normal | 2 = Slow"))
        
        def call_Kernel(self):
            global mode
            _translate = QtCore.QCoreApplication.translate
            self.pushButton.setGeometry(QtCore.QRect(10, 10, 0, 0))
            #self.pushButton_2.setGeometry(QtCore.QRect(290, 140, 0, 0))
            self.label_2.setText(_translate("DefaultWindow", "測試中..."))
            print('[+] Handing Over To Kernel...')
            TestStatus = kernel.PreStart(cam)
            print('[+] Kernel Handed back! Rendering results...')
            if TestStatus == False:    
                self.label_2.setText(_translate("DefaultWindow", "相機不存在或更新率過低(亮度不足)"))
            elif TestStatus == True:
                self.label_2.setText(_translate("DefaultWindow", "測試完成"))
                result = open('result.txt', 'r', encoding='utf-8').readline()
                print(f'BPM = {result}')
                self.lcdNumber.display(result)
            self.pushButton.setGeometry(QtCore.QRect(10, 50, 161, 61))
            #self.pushButton_2.setGeometry(QtCore.QRect(290, 140, 101, 23))

        def camChange(self):
            global cam
            cam = self.camSpin.value()
            print(f'cam has been set to {cam}')

class Kernel_massage:
    def UIcalling():
        print('[+] UI Start Calling...')
    
    def UI_Show():
        print('[+] Generating UI...')

    def CMCimport():
        print('[+] Importing CamMainCtl...')

    def cvimport():
        print('[+] Importing cv2...')

    def npimport():
        print('[+] Importing numpy...')

    def scipyimport():
        print('[+] Importing scipy...')

    def defaultimport():
        print('[+] Importing Module....')

def oncall_start():
        import sys
        Kernel_massage.UIcalling()
        app = QtWidgets.QApplication(sys.argv)
        DefaultWindow = QtWidgets.QDialog()
        ui = UI_Start.Ui_DefaultWindow()
        ui.setupUi(DefaultWindow)
        DefaultWindow.show()
        Kernel_massage.UI_Show()
        sys.exit(app.exec_())


class main:
    def LLStart():
        try:
            Kernel_massage.CMCimport()
            import CamMainCtl
            Kernel_massage.cvimport()
            import cv2
            Kernel_massage.npimport()
            import numpy as np
            Kernel_massage.scipyimport()
            import scipy
            Kernel_massage.defaultimport()
            import time
            from datetime import datetime
        except:
            print('Import Failed! Please install all requirements!')
            PreventFailing = input()

        print('[+] LiveLinkage Starting...')
        status = oncall_start()
        if status == True:
            print('[+] UI Started...')
        else:
            print('[-] UI Failed, Please Check The Code...')
            PreventFailing = input()


main.LLStart()