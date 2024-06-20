from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import cv2
import threading
import time

running = True

def close(e):
    global running
    running = False

class MainPage(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("main_page")
        self.setWindowTitle("HRMonitor v2.0")
        self.resize(1080,820)

        self.camera_open = True

        self.frame = None

        self.setup_camera()
        self.setup_instruction()
        self.setup_LCD_display()
        self.translate()

        self.fingerControl = FingerControl(self)
        

    # Camera
    def setup_camera(self) -> None:
        self.camera = QtWidgets.QLabel(self)
        self.camera.setObjectName("camera")
        self.camera.setGeometry(0,0,1080,720)
        camera_thread = threading.Thread(target=self.camera_control)
        camera_thread.start()
    
    def camera_control(self):
        cap = cv2.VideoCapture(0)      # 設定攝影機鏡頭
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while running:
            ret, self.frame = cap.read()    # 讀取攝影機畫面
            self.fingerControl.fingercontrol()
            if not ret:
                print("Cannot receive frame")
                break
            frame = cv2.resize(self.frame, (1080, 720))   # 改變尺寸和視窗相同
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 轉換成 RGB
            height, width, channel = frame.shape    # 讀取尺寸和 channel數量
            bytesPerline = channel * width          # 設定 bytesPerline ( 轉換使用 )
            # 轉換影像為 QImage，讓 PyQt5 可以讀取
            img = QImage(frame, width, height, bytesPerline, QImage.Format_RGB888)
            self.camera.setPixmap(QPixmap.fromImage(img))

    # Instruction
    def setup_instruction(self):
        self.instruction = QtWidgets.QLabel(self)
        self.instruction.setObjectName("insturction")
        self.instruction.setGeometry(0,720,500,100)
        self.instruct_font = QFont()
        self.instruct_font.setPointSize(20)
        self.instruction.setFont(self.instruct_font)

    # LCD Display
    def setup_LCD_display(self):
        self.lcd = QtWidgets.QLCDNumber(self)
        self.lcd.setObjectName("LCD")
        self.lcd.setGeometry(880,720,200,100)
        self.lcd.display(0)

    # Translate
    def translate(self):
        self._translate = QCoreApplication.translate
        self.instruction.setText(self._translate("HRMonitor","請將手指放在鏡頭上"))


class FingerControl:
    def __init__(self,page:MainPage) -> None:
        self.page = page

    def fingercontrol(self) -> None:
        frame = self.page.frame
        frame = cv2.resize(frame,(600,420))
        avgB, avgG, avgR, avgA = cv2.mean(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bright = int(cv2.mean(gray)[0])
        if avgR > (avgB + avgG):#avgR > 70 and 
            if bright >= 50:
                self.page.instruction.setText(self.page._translate("HRMonitor","正在紀錄..."))
                self.page.instruction.setStyleSheet("color: green;")
            else:
                self.page.instruction.setText(self.page._translate("HRMonitor","請提高背景亮度!"))
                self.page.instruction.setStyleSheet("color: red;")
        else:
            self.page.instruction.setText(self.page._translate("HRMonitor","請將手指放在鏡頭上!"))
            self.page.instruction.setStyleSheet("color: black;")
        print(f"R={avgR}, G={avgG}, B={avgB}, bright={bright}, if={avgR > (avgB + avgG)}...",end="\r",flush=True)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = MainPage()

    Form.closeEvent = close

    Form.show()
    sys.exit(app.exec_())