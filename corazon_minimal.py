print('[!] Please put your finger on the webcam before the camera window show up!')
print('[+] Starting up main...')
import cv2
import time
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

class System_Message:
    def Camera_Success():
        cv2.imshow('If you see this window without fingr on it, please restart program', frame)
        
    def Camera_Failure():
        print('[-] Camera Failed!')

class Algorithms:
    def subseq(bright_rec):
        h_std = []
        # height standard calculation
        for i, x in enumerate(bright_rec):
            if i >= len(bright_rec)-16:
                h_std.append(avg_bri)
            else:
                v_offset = 0.2*(max(bright_rec[i:i+15]) - min(bright_rec[i:i+15])) # height vertical offset amount
                avg_bri = np.average(bright_rec[i:i+15]) + v_offset
                h_std.append(avg_bri)

        peak_idx = find_peaks(bright_rec, height=np.array(h_std), distance=7)[0]
        return((len(peak_idx)*6))
    
    def avg_calc(result):
        datacount = len(np.array(result))

        avg = []
        avg2 = []
        for i in range(datacount):
            avg.append(np.average(result[i:i+5]))
            #avg2.append(np.average(result[i:i+20]))

        peak, _ = find_peaks(np.array(result), distance=(4), height=np.array(avg))
        
        peaks = len(peak)
        Result2 = peaks * 6
        return Result2, peak, avg, avg2

    def polyfit(result):
        datacount = len(np.array(result))
        x = np.arange(len(result))
        p = np.poly1d(np.polyfit(x, result, 13))
        pfix = p(x)[:]
        for i in range(30):
            pfix[i] = np.average(pfix[i:i+15])
        #for i in range(-25, 0, 1):
        #    pfix[i] = np.average(pfix[i-15:i])
        peak, _ = find_peaks(np.array(result), distance=(4), height=pfix)
        Result3 = (len(peak)*6)
        return Result3, pfix, peak
    
cam = cv2.VideoCapture(0)
print('[+] Camera starting...')
FrameCount = 0
start_time = round(time.time())
time_ref = 0
bright_rec = []
FPS = 0
FPS_P = 0
peak = np.array([])
stopped = False
BPM_rec = []
while True:
    check, frame = cam.read()
    if check:
        System_Message.Camera_Success()
    else:
        System_Message.Camera_Failure()
    
    if cv2.waitKey(1) == ord('q'):
        print('[>] Exiting...')
        cv2.destroyAllWindows()
        break
    plt.plot(bright_rec)

    time_now = time.time()
    time_fixed = round(time_now)
    time_passed = time_fixed - start_time
    avgB, avgG, avgR, avgA = cv2.mean(frame)
    if time_passed <= 10 and avgR > 70 and avgR > (avgB + avgG) :
        FrameCount += 1
        FPS += 1
        stopped = False
        if time_passed - time_ref >= 1:
            plt.title(f'FPS: {FPS}')
            print(f'TP:{time_passed}, TR:{time_ref}, Diff:{time_passed - time_ref}, FPS:{FPS}')
            FPS = 0
            time_ref = time_passed
        avgB, avgG, avgR, avgA = cv2.mean(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bright = cv2.mean(gray)[0]
        bright_rec.append(bright)
        res, peak, avg, avg2 = Algorithms.avg_calc(bright_rec)
        print(FrameCount)
        if FrameCount >= 31:
            print("Polyfit Activated")
            plyfit_res, pfix, peak2 = Algorithms.polyfit(bright_rec)
            plt.clf()
            plt.title(f'avc:{res}, plf:{plyfit_res}, frames:{FrameCount}, fps:{FPS_P}/s')
            plt.plot(np.array(pfix), label="Polyfit Baseline")
            plt.plot(peak2, np.array(bright_rec)[peak2], "o")
            BPM_rec.append(np.average(res+plyfit_res)/2)
        
        plt.plot(np.array(bright_rec), label="Data")
        plt.plot(np.array(avg), label="Avg Baseline")
        if peak is not None and len(peak) > 0:
            plt.plot(peak, np.array(avg)[peak], "x")
        plt.pause(0.0001)

    elif avgR > 70 and avgR > (avgB + avgG) :
        
        FrameCount += 1
        stopped = False
        avgB, avgG, avgR, avgA = cv2.mean(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bright = cv2.mean(gray)[0]
        bright_rec.append(bright)
        if time_passed - time_ref >= 1:
            FPS_P = FPS
            time_ref = time_passed
            FPS = 0
        else:
            FPS += 1
        
        del bright_rec[0]
        res, peak, avg, avg2 = Algorithms.avg_calc(bright_rec)
        plyfit_res, pfix, peak2 = Algorithms.polyfit(bright_rec)
        BPM_rec.append(np.average(res+plyfit_res)/2)
        plt.clf()
        del BPM_rec[0]
        plt.title(f'avc:{res}, plf:{plyfit_res}, frames:{FrameCount}, 10s avg:{round(np.average(BPM_rec))}, fps:{FPS_P}/s')
        plt.plot(np.array(bright_rec), label="Data")
        plt.plot(np.array(avg), label="Avg Baseline")
        plt.plot(np.array(pfix), label="Polyfit Baseline")
        plt.plot(peak2, np.array(bright_rec)[peak2], "o")
        if peak is not None and len(peak) > 0:
            plt.plot(peak, np.array(bright_rec)[peak], "x")
        plt.pause(0.0001)
    elif stopped == False:
        FrameCount = 0
        print("stopped")
        FrameCount += 1
        time_now = time.time()
        time_fixed = round(time_now)
        time_passed = time_fixed - start_time
        del bright_rec[:]
        stopped = True
    else:
        FrameCount = 0
        start_time = round(time.time())
        time_passed = time_fixed - start_time

        
print(f'Total Frame Count = {FrameCount}')
with open('CoraOutput.txt', 'w', encoding='utf-8') as f:
    for i in bright_rec:
        f.write(f'{i}\n')