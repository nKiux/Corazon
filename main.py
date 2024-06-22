from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from scipy.signal import find_peaks
import sys
import cv2
import threading
import logging
import time
import os

running = True # 以視窗關閉鏡頭未關

checking = 0 # 「確認中...」用

def resource_path(relative_path): # pyinstaller用
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def find_antipeak(l) -> list: # 找心跳點
    l2 = l
    #avg = average(l2)
    #r = max(l2)-min(l2) #range
    return find_peaks(l2, distance=7)[0] #,height=avg+0.2*r

def get_bpm(index:list,times:list) -> float: # 計算BPM
    """
    `index` is the list of indexes of the peaks

    `times` is the time record of the data
    """
    time_list = [times[i] for i in index] 
    dt_list = []
    for i in range(len(time_list)-1):
        dt_list.append(time_list[i+1] - time_list[i])
    dt = average(dt_list)
    return round(60/(dt/1000000000),1) if dt != 0 else 0 #9個0

def close(e): # 關閉視窗動作
    global running
    running = False

def average(l): # 計算用
    return sum(l)/len(l) if len(l)>0 else 0

class MainPage(QWidget): # 視窗
    def __init__(self) -> None:
        super().__init__()
        # 一些設定
        self.setObjectName("main_page")
        self.setWindowTitle("HRMonitor v2.0.0")
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        self.resize(1080,820)
        self.setFixedSize(1080,820)

        # 設定基本數值
        self.frame = None # 現在的影像
        self.plot = [0] # 亮度紀錄
        self.plot_time = [0] # 亮度對應的時間記錄

        # 視窗啟動
        self.setup_camera()
        self.setup_instruction()
        self.setup_LCD_display()
        self.translate()

        self.fingerControl = FingerControl(self)
        

    # Camera
    def setup_camera(self) -> None:
        """
        設定影像顯示器、開啟相機
        """
        self.camera = QLabel(self)
        self.camera.setObjectName("camera")
        self.camera.setGeometry(0,0,1080,720)
        camera_thread = threading.Thread(target=self.camera_control)
        camera_thread.start()

    def set_camera_image(self,image:QPixmap):
        """
        更新影像顯示器圖片
        """
        self.camera.setPixmap(image)
        self.update()
    
    def camera_control(self):
        """
        管鏡頭的東西
        """
        global checking
        loop = 0
        cap = cv2.VideoCapture(0)      # 設定攝影機鏡頭
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while running:
            ret, self.frame = cap.read()    # 讀取攝影機畫面
            if not ret:
                print("Cannot receive frame")
                self.set_instruction("無法開啟相機!!!")
                break
            self.fingerControl.fingercontrol() # 呼叫確認有無手指
            frame = cv2.resize(self.frame, (1080, 720))   # 改變尺寸和視窗相同
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 轉換成 RGB
            height, width, channel = frame.shape    # 讀取尺寸和 channel數量
            bytesPerline = channel * width          # 設定 bytesPerline ( 轉換使用 )
            # 轉換影像為 QImage，讓 PyQt5 可以讀取
            img = QImage(frame, width, height, bytesPerline, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            if checking != 0: # 在確認時
                painter = QPainter(pixmap) # 繪製工具
                painter.setPen(QPen(QColor("#dcdcdc"),10,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap)) # 設定筆刷
                painter.drawArc(490,310,100,100,90*16,checking*-16) # 繪製進度條

                plotted_samples = 100 # 設定取樣數
                plot = self.plot[-1*plotted_samples-1:][1:] if len(self.plot[-1*plotted_samples-1:]) > 1 else [0] # 取樣
                plot_time = self.plot_time[-1*plotted_samples-1:][1:] if len(self.plot_time[-1*plotted_samples-1:]) > 1 else [0]
                scale = 100/(max(plot)-min(plot)) if (max(plot)-min(plot)) != 0 else 0
                avg = average(plot)
                peaks = find_antipeak(plot)
                for i in range(len(plot)-1):
                    painter.drawLine(int((1080/plotted_samples)*i), int((plot[i]-avg)*scale+670), int((1080/plotted_samples)*(i+1)), int((plot[i+1]-avg)*scale+670)) # 繪製心跳圖
                for i in peaks:
                    painter.drawLine(int((1080/plotted_samples)*i), 620, int((1080/plotted_samples)*(i)), 720) # 繪製心跳點
                painter.end()

                if loop > 50: # 一段時間後
                    self.set_LCD_display(get_bpm(peaks,plot_time)) # 更新LCD
                    loop = 0
                loop += 1
            self.set_camera_image(pixmap) # 更新顯示器顯示影像

    # Instruction
    def setup_instruction(self):
        """
        增加告示
        """
        self.instruction = QLabel(self)
        self.instruction.setObjectName("insturction")
        self.instruction.setGeometry(0,720,500,100)
        self.instruct_font = QFont()
        self.instruct_font.setPointSize(20)
        self.instruction.setFont(self.instruct_font)

    def set_instruction(self,text,color="black"):
        """
        更新告示
        """
        self.instruction.setText(self._translate("HRMonitor",text))
        #self.instruction.setStyleSheet(f"color: {color};")

    # LCD Display
    def setup_LCD_display(self):
        """
        新增LCD顯示
        """
        self.lcd = QLCDNumber(self)
        self.lcd.setObjectName("LCD")
        self.lcd.setGeometry(880,720,200,100)
        self.lcd.display(0)
    
    def set_LCD_display(self,number):
        """
        更新LCD顯示數字
        """
        self.lcd.display(number)

    # Translate
    def translate(self):
        """
        單純translate，也不知道真的有什麼用
        """
        self._translate = QCoreApplication.translate
        self.instruction.setText(self._translate("HRMonitor","請將手指放在鏡頭上"))

class FingerControl:
    """
    管你手指的一個東西
    """
    def __init__(self,page:MainPage) -> None:
        """
        初始化
        """
        self.page = page # 連結到視窗

    def fingercontrol(self) -> None:
        global checking
        frame = self.page.frame # 複製目前的畫面
        frame = cv2.resize(frame,(600,420)) # 重設大小
        avgB, avgG, avgR, avgA = cv2.mean(frame) # 擷取顏色
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 轉成灰階(用來看亮度)
        bright = cv2.mean(gray)[0] # 擷取亮度
        bright_fix = int(bright) # 修正成好看的亮度
        if avgR > (avgB + avgG)*0.8: # 如果紅色佔大多數
            if checking < 360: # 確認進度條使用
                checking += 9 # 進度條速度
                self.page.set_instruction("正在確定...","black") # 更新告示文字
            else:
                if bright_fix >= 40: # 如果夠亮
                    self.page.set_instruction("正在紀錄...","green") # 更新告示文字
                    self.page.plot.append(bright) # 紀錄亮度
                    self.page.plot_time.append(time.time_ns()) # 紀錄時間
                else:
                    self.page.set_instruction("請提高背景亮度!","red") # 更新告示文字
        else: # 沒有手指
            if checking > 1:
                checking -= 20 # 重設進度條
            else:
                checking = 0
            self.page.plot = [0] # 重設紀錄
            self.page.plot_time = [0] # 重設時間紀錄
            self.page.set_instruction("請將手指放在鏡頭上!","black") # 更新告示文字

if __name__ == "__main__":
    """
    本來就要得一些東西
    """
    app = QApplication(sys.argv)
    Form = MainPage()

    Form.closeEvent = close # 設定關閉時執行的

    Form.show()
    sys.exit(app.exec_())