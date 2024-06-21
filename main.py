from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import cv2
import threading
import logging

logging.basicConfig(filename="log.log",encoding="utf-8",level=logging.DEBUG)

running = True

checking = 0

def close(e):
    global running
    running = False

def average(l):
    return sum(l)/len(l)

class MainPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("main_page")
        self.setWindowTitle("HRMonitor v2.0")
        self.resize(1080,820)

        self.camera_open = True

        self.frame = None
        self.plot = [0]

        self.setup_camera()
        self.setup_instruction()
        self.setup_LCD_display()
        self.translate()

        self.fingerControl = FingerControl(self)
        

    # Camera
    def setup_camera(self) -> None:
        self.camera = QLabel(self)
        self.camera.setObjectName("camera")
        self.camera.setGeometry(0,0,1080,720)
        camera_thread = threading.Thread(target=self.camera_control)
        camera_thread.start()

    def set_camera_image(self,image:QPixmap):
        self.camera.setPixmap(image)
        self.update()
    
    def camera_control(self):
        global checking
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
            pixmap = QPixmap.fromImage(img)
            if checking != 0:
                painter = QPainter(pixmap)
                painter.setPen(QPen(QColor("#dcdcdc"),10,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
                painter.drawArc(490,310,100,100,90*16,checking*-16)

                plotted_samples = 100
                plot = self.plot[-1*plotted_samples-5:][1:] if len(self.plot[-1*plotted_samples-5:]) > 1 else [0]
                scale = 100/(max(plot)-min(plot)) if (max(plot)-min(plot)) != 0 else 0
                avg = average(plot)
                for i in range(len(plot)-1):
                    painter.drawLine(int((1080/plotted_samples)*i), int((plot[i]-avg)*scale+670), int((1080/plotted_samples)*(i+1)), int((plot[i+1]-avg)*scale+670))
                painter.end()
            self.set_camera_image(pixmap)

    # Instruction
    def setup_instruction(self):
        self.instruction = QLabel(self)
        self.instruction.setObjectName("insturction")
        self.instruction.setGeometry(0,720,500,100)
        self.instruct_font = QFont()
        self.instruct_font.setPointSize(20)
        self.instruction.setFont(self.instruct_font)

    def set_instruction(self,text,color="black"):
        self.instruction.setText(self._translate("HRMonitor",text))
        #self.instruction.setStyleSheet(f"color: {color};")

    # LCD Display
    def setup_LCD_display(self):
        self.lcd = QLCDNumber(self)
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
        global checking
        frame = self.page.frame
        frame = cv2.resize(frame,(600,420))
        avgB, avgG, avgR, avgA = cv2.mean(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bright = cv2.mean(gray)[0]
        bright_fix = int(bright)
        if avgR > (avgB + avgG)*0.8:#avgR > 70 and 
            if checking < 360:
                checking += 9
                self.page.set_instruction("正在確定...","black")
            else:
                if bright_fix >= 40:
                    self.page.set_instruction("正在紀錄...","green")
                    self.page.plot.append(bright)
                else:
                    self.page.set_instruction("請提高背景亮度!","red")
        else:
            checking = 0
            self.page.plot = [0]
            self.page.set_instruction("請將手指放在鏡頭上!","black")
        print(bright_fix)
        #print(f"R={avgR}, G={avgG}, B={avgB}, bright={bright}, if={avgR > (avgB + avgG)}...",end="\r",flush=True)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Form = MainPage()

    Form.closeEvent = close

    Form.show()
    sys.exit(app.exec_())