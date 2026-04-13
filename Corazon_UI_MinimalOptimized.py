# please pip install the following modules: numpy, scipy, opencv-python, PyQt6, matplotlib, pygrabber
import sys
import cv2
import time
import numpy as np
from scipy.signal import find_peaks

# PyQt6 Imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QImage, QPixmap, QFont


def list_cameras(max_test=5):
    """Return list of (index, name) tuples for available cameras."""
    cameras = []
    names_by_index = {}
    try:
        from pygrabber.dshow_graph import FilterGraph
        for i, n in enumerate(FilterGraph().get_input_devices()):
            names_by_index[i] = n
    except Exception:
        pass

    for i in range(max_test):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            name = names_by_index.get(i, f'Camera {i}')
            cameras.append((i, name))
            cap.release()
    if not cameras:
        cameras.append((0, 'Camera 0'))
    return cameras

# Matplotlib Integration
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Algorithms:
    @staticmethod
    def avg_calc(result):
        result_np = np.array(result)
        avg = []

        for i in range(len(result_np)):
            sub_data = result_np[i:i+10]
            if len(sub_data) > 0:
                avg.append(np.mean(sub_data))
            else:
                avg.append(result_np[i])
        
        avg = np.array(avg)
        peak = find_peaks(result_np, distance=4, height=avg)[0]
        
        peaks = len(peak)
        Result_avg = peaks * 6
        return Result_avg, peak, avg
    
    @staticmethod
    def polyfit(result):
        x = np.arange(len(result))
        if len(x) == 0: return 0, [], []
        
        try:
            p = np.poly1d(np.polyfit(x, result, 13))
        except:
            return 0, np.zeros(len(result)), []

        pfix = p(x)[:]
        limit = min(30, len(pfix))
        for i in range(limit):
            sub = pfix[i:i+15]
            if len(sub) > 0:
                pfix[i] = np.average(sub)
        
        peak = find_peaks(np.array(result), distance=4, height=pfix)[0]
        Result_ploy = len(peak) * 6
        return Result_ploy, pfix, peak

class WorkerThread(QThread):
    image_update = pyqtSignal(QImage)
    plot_update = pyqtSignal(dict)
    status_update = pyqtSignal(str)
    bpm_update = pyqtSignal(int)

    def __init__(self, cam_index=0):
        super().__init__()
        self.cam_index = cam_index
        self._switch_requested = False

    def set_camera(self, index):
        if index != self.cam_index:
            self.cam_index = index
            self._switch_requested = True

    def run(self):
        self.status_update.emit('[!] Please put your finger on the webcam')
        self.status_update.emit('[+] Starting up main...')

        cam = cv2.VideoCapture(self.cam_index)
        self.status_update.emit('[+] Camera starting...')
        
        FrameCount = 0
        start_time = round(time.time())
        time_ref = 0
        bright_rec = []
        FPS = 0
        FPS_P = 0
        peak = np.array([])
        stopped = False
        BPM_rec = []
        
        self.is_running = True

        while self.is_running:
            if self._switch_requested:
                cam.release()
                cam = cv2.VideoCapture(self.cam_index)
                self._switch_requested = False
                bright_rec = []
                BPM_rec = []
                FrameCount = 0
                start_time = round(time.time())
                self.plot_update.emit({'mode': 'clear'})
                self.status_update.emit(f'[+] Switched to camera {self.cam_index}')

            check, frame = cam.read()
            if not check:
                self.status_update.emit('[-] Camera Failed!')
                continue

            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)
            self.image_update.emit(qt_image)

            time_now = time.time()
            time_fixed = round(time_now)
            time_passed = time_fixed - start_time
            avgB, avgG, avgR, avgA = cv2.mean(frame)

            plot_data = {}
            should_plot = (FrameCount % 2 == 0)

            if time_passed <= 10 and avgR > 70 and avgR > (avgB + avgG):    # within 10sec / finger detection
                FrameCount += 1
                FPS += 1
                stopped = False

                if time_passed - time_ref >= 1:
                    plot_data['title'] = f'FPS: {FPS}'
                    self.status_update.emit(f'TP:{time_passed}, TR:{time_ref}, Diff:{time_passed - time_ref}, FPS:{FPS}')
                    FPS = 0
                    time_ref = time_passed
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                bright = cv2.mean(gray)[0]
                bright_rec.append(bright)

                if should_plot:
                    res, peak, avg = Algorithms.avg_calc(bright_rec)

                    plot_data['bright_rec'] = np.array(bright_rec)
                    plot_data['avg'] = np.array(avg)
                    plot_data['peak'] = peak

                    if FrameCount >= 31:    # ployfit activation
                        # self.status_update.emit("Polyfit Activated")
                        plyfit_res, pfix, peak2 = Algorithms.polyfit(bright_rec)
                        BPM_rec.append(np.average(res + plyfit_res)/2)

                        plot_data['title'] = f'avc:{res}, plf:{plyfit_res}, frames:{FrameCount}, fps:{FPS_P}/s'
                        plot_data['pfix'] = np.array(pfix)
                        plot_data['peak2'] = peak2
                        plot_data['mode'] = 'polyfit activated'
                    else:
                        plot_data['mode'] = 'normal'

                    self.plot_update.emit(plot_data)

            elif avgR > 70 and avgR > (avgB + avgG):    # after 10sec / finger detection
                FrameCount += 1
                stopped = False
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                bright = cv2.mean(gray)[0]
                bright_rec.append(bright)
                
                if time_passed - time_ref >= 1:
                    FPS_P = FPS 
                    time_ref = time_passed
                    FPS = 0
                else:
                    FPS += 1
                
                if len(bright_rec) > 0:
                    del bright_rec[0]
                
                if should_plot:
                    res, peak, avg = Algorithms.avg_calc(bright_rec)
                    plyfit_res, pfix, peak2 = Algorithms.polyfit(bright_rec)

                    BPM_rec.append(np.average(res + plyfit_res)/2)
                    if len(BPM_rec) > 0:
                        del BPM_rec[0]

                    avg_bpm = round(np.average(BPM_rec)) if BPM_rec else 0
                    self.bpm_update.emit(int(avg_bpm))
                    plot_data['title'] = f'avc:{res}, plf:{plyfit_res}, frames:{FrameCount}, 10s avg:{avg_bpm}, fps:{FPS_P}/s'
                    plot_data['bright_rec'] = np.array(bright_rec)
                    plot_data['avg'] = np.array(avg)
                    plot_data['pfix'] = np.array(pfix)
                    plot_data['peak2'] = peak2
                    plot_data['peak'] = peak
                    plot_data['mode'] = 'stable'

                    self.plot_update.emit(plot_data)

            elif stopped == False:
                FrameCount = 0
                self.status_update.emit("stopped")
                time_now = time.time()
                time_fixed = round(time_now)
                time_passed = time_fixed - start_time
                del bright_rec[:]
                stopped = True
                self.bpm_update.emit(0)
                self.plot_update.emit({'mode': 'clear'})

            else:
                FrameCount = 0
                start_time = round(time.time())
                time_passed = time_fixed - start_time


            time.sleep(0.01)

        cam.release()
        self.status_update.emit(f'Total Frame Count = {FrameCount}')

    def stop(self):
        self.is_running = False
        self.wait()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Corazon")
        self.resize(1200, 600)

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left: Webcam View + camera selector
        self.video_label = QLabel("Webcam Feed")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setMinimumSize(480, 360)

        self.camera_selector = QComboBox()
        self.cameras = list_cameras()
        for idx, name in self.cameras:
            self.camera_selector.addItem(f'{name} (#{idx})', idx)
        self.camera_selector.currentIndexChanged.connect(self.on_camera_changed)

        video_container = QVBoxLayout()
        video_container.addWidget(self.video_label, stretch=1)
        video_container.addWidget(self.camera_selector, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(video_container, stretch=2)

        # Right: Matplotlib Plot + BPM display
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(1, 1, 1)

        self.bpm_label = QLabel("BPM: --")
        bpm_font = QFont()
        bpm_font.setPointSize(18)
        bpm_font.setBold(True)
        self.bpm_label.setFont(bpm_font)
        self.bpm_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        plot_container = QVBoxLayout()
        plot_container.addWidget(self.canvas, stretch=1)
        plot_container.addWidget(self.bpm_label, alignment=Qt.AlignmentFlag.AlignRight)
        main_layout.addLayout(plot_container, stretch=3)

        # Start Worker Thread
        initial_idx = self.cameras[0][0] if self.cameras else 0
        self.worker = WorkerThread(cam_index=initial_idx)
        self.worker.image_update.connect(self.update_image)
        self.worker.plot_update.connect(self.update_plot)
        self.worker.status_update.connect(self.print_status)
        self.worker.bpm_update.connect(self.update_bpm)
        self.worker.start()

    def on_camera_changed(self, _):
        idx = self.camera_selector.currentData()
        if idx is not None:
            self.worker.set_camera(int(idx))

    def update_bpm(self, bpm):
        self.bpm_label.setText(f"BPM: {bpm}" if bpm > 0 else "BPM: --")

    def update_image(self, qt_image):
        pixmap = QPixmap.fromImage(qt_image)
        self.video_label.setPixmap(pixmap)

    def update_plot(self, data):
        self.ax.clear()
        
        mode = data.get('mode', '')
        if mode == 'clear':
            self.canvas.draw()
            return

        title = data.get('title', '')
        if title:
            self.ax.set_title(title)

        bright_rec = data.get('bright_rec')

        if mode == 'polyfit activated':
            pfix = data.get('pfix')
            peak2 = data.get('peak2')
            
            self.ax.plot(pfix, label="Polyfit Baseline")
            if bright_rec is not None and peak2 is not None:
                self.ax.plot(peak2, bright_rec[peak2], "o")
            
            self.ax.plot(bright_rec, label="Data")
            
            avg = data.get('avg')
            if avg is not None:
                self.ax.plot(avg, label="Avg Baseline")
                
            peak = data.get('peak')
            if peak is not None and len(peak) > 0 and avg is not None:
                self.ax.plot(peak, avg[peak], "x")

        elif mode == 'stable':
            self.ax.plot(bright_rec, label="Data")
            
            avg = data.get('avg')
            if avg is not None:
                self.ax.plot(avg, label="Avg Baseline")
                
            pfix = data.get('pfix')
            if pfix is not None:
                self.ax.plot(pfix, label="Polyfit Baseline")
            
            peak2 = data.get('peak2')
            if peak2 is not None and bright_rec is not None:
                self.ax.plot(peak2, bright_rec[peak2], "o")
                
            peak = data.get('peak')
            if peak is not None and len(peak) > 0 and bright_rec is not None:
                self.ax.plot(peak, bright_rec[peak], "x")

        elif mode == 'normal':
            # Initial phase
            if bright_rec is not None:
                self.ax.plot(bright_rec, label="Data")
            
            avg = data.get('avg')
            if avg is not None:
                self.ax.plot(avg, label="Avg Baseline")

            peak = data.get('peak')
            if peak is not None and len(peak) > 0 and avg is not None:
                self.ax.plot(peak, avg[peak], "x")

        self.ax.legend(loc='upper right')
        self.canvas.draw()

    def print_status(self, text):
        print(text)

    def closeEvent(self, event):
        self.worker.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
