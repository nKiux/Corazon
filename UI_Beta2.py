#version 0.6.1 HotFix
import os
import kernel_LightEngine
from kernel_LightEngine import pure_benchmark
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except:
    os.system('pip install PyQt5')

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DefaultWindow(object):
    def setupUi(self, DefaultWindow):
        DefaultWindow.setObjectName("DefaultWindow")
        DefaultWindow.resize(482, 171)
        self.pushButton = QtWidgets.QPushButton(DefaultWindow)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 161, 101))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.call_Kernel)

        self.lcdNumber = QtWidgets.QLCDNumber(DefaultWindow)
        self.lcdNumber.setGeometry(QtCore.QRect(180, 30, 291, 81))
        self.lcdNumber.setObjectName("lcdNumber")


        self.label = QtWidgets.QLabel(DefaultWindow)
        self.label.setGeometry(QtCore.QRect(180, 10, 101, 16))
        self.label.setObjectName("label")

        self.checkBox = QtWidgets.QCheckBox(DefaultWindow)
        self.checkBox.setGeometry(QtCore.QRect(10, 120, 73, 16))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.clicked.connect(self.KernelSpeedUP)

        self.pushButton_2 = QtWidgets.QPushButton(DefaultWindow)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 140, 101, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.benchmark)

        self.label_2 = QtWidgets.QLabel(DefaultWindow)
        self.label_2.setGeometry(QtCore.QRect(120, 140, 70, 21))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(DefaultWindow)
        QtCore.QMetaObject.connectSlotsByName(DefaultWindow)

    def retranslateUi(self, DefaultWindow):
        _translate = QtCore.QCoreApplication.translate
        DefaultWindow.setWindowTitle(_translate("DefaultWindow", "HRMonitor Beta"))
        self.pushButton.setText(_translate("DefaultWindow", "Start"))
        self.label.setText(_translate("DefaultWindow", "BPM(目前不可運作)"))
        self.checkBox.setText(_translate("DefaultWindow", "Fast Start"))
        self.pushButton_2.setText(_translate("DefaultWindow", "Benchmark"))
        self.label_2.setText(_translate("DefaultWindow", "Result:"))
    
    def call_Kernel(self):
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 0, 0))
        kernel_LightEngine.start(kernel_LightEngine.bnhmrk)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 161, 101))

    def benchmark(self):
        self.pushButton_2.setGeometry(QtCore.QRect(10, 140, 0, 0))
        if pure_benchmark(camera_select=0): #目前只能選擇相機 0
            title = "Passed"
        else:
            title = "Failed"
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("DefaultWindow", f"Result: {title}"))
        self.pushButton_2.setGeometry(QtCore.QRect(10, 140, 101, 23))

    def KernelSpeedUP(self):
        if self.checkBox.isChecked():
            kernel_LightEngine.bnhmrk = True
            print('Kernel SpeedUP! is set to true')
        else:
            kernel_LightEngine.bnhmrk = False
            print('Kernel SpeedUP! is set to false')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DefaultWindow = QtWidgets.QDialog()
    ui = Ui_DefaultWindow()
    ui.setupUi(DefaultWindow)
    DefaultWindow.show()
    sys.exit(app.exec_())
