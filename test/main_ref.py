from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, cv2, threading
import cv2

class Ui_Form(object):
    def setupUi(self, Form):
        self.camera_open = True

        Form.setObjectName("Form")
        self.lcdNumber = QtWidgets.QLCDNumber(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(493, 400, 101, 61)) #QtCore.QRect(493, 332, 101, 61)
        self.lcdNumber.setObjectName("lcdNumber")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 400, 471, 51)) #QtCore.QRect(10, 339, 471, 51)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")

        

        self.camera = QtWidgets.QLabel(Form)
        self.camera.setGeometry(0,0,600,400)
        self.camera.setObjectName("camera")

        self.widget = QPainter() #Form
        #self.widget.setGeometry(QtCore.QRect(0, 290, 601, 41))
        #self.widget.setObjectName("widget")
        self.widget.paintEvent = self.draw

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "請將手指放在鏡頭上"))

    def opencv(self):
        cap = cv2.VideoCapture(0)      # 設定攝影機鏡頭
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while self.camera_open:
            ret, frame = cap.read()    # 讀取攝影機畫面
            if not ret:
                print("Cannot receive frame")
                break
            frame = cv2.resize(frame, (600, 400))   # 改變尺寸和視窗相同
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 轉換成 RGB
            height, width, channel = frame.shape    # 讀取尺寸和 channel數量
            bytesPerline = channel * width          # 設定 bytesPerline ( 轉換使用 )
            # 轉換影像為 QImage，讓 PyQt5 可以讀取
            img = QImage(frame, width, height, bytesPerline, QImage.Format_RGB888)
            self.camera.setPixmap(QPixmap.fromImage(img)) # QLabel 顯示影像
    
    def close_cam(self,s):
        self.camera_open = False

    def draw(self,s):
        qpainter = QPainter()
        qpainter.begin(self.widget)

        # 左邊的正方形
        qpainter.setPen(QPen(QColor('#000000'), 5, Qt.DotLine, Qt.FlatCap, Qt.MiterJoin))
        qpainter.drawRect(30,50,100,100)

        # 右邊的正方形
        qpainter.setPen(QPen(QColor('#ff0000'), 10, Qt.DashDotDotLine, Qt.RoundCap, Qt.RoundJoin))
        qpainter.drawRect(160,50,100,100)

        qpainter.end()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    Form.setWindowTitle('HRMonitor Beta')
    #Form.resize(600, 400)
    ui = Ui_Form()
    ui.setupUi(Form)
    video = threading.Thread(target=ui.opencv)
    video.start()
    Form.closeEvent = ui.close_cam
    Form.show()
    sys.exit(app.exec_())
