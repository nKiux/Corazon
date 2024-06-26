#version 13S3
import os
import kernel_Litxtre
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except:
    os.system('pip install PyQt5')

from PyQt5 import QtCore, QtGui, QtWidgets

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
        print(f'正在以模式{mode}執行')
        self.label_2.setText(_translate("DefaultWindow", "測試中..."))
        start = kernel_Litxtre.start(kernel_Litxtre.bnhmrk, camera_select=cam, mode=mode)
        if start == False:    
            self.label_2.setText(_translate("DefaultWindow", "相機不存在或更新率過低(亮度不足)"))
        elif start == True:
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DefaultWindow = QtWidgets.QDialog()
    ui = Ui_DefaultWindow()
    ui.setupUi(DefaultWindow)
    DefaultWindow.show()
    sys.exit(app.exec_())