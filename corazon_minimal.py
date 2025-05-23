print('[!] Please put your finger on the webcam before the camera window show up!')
print('[+] Starting up main...')
import cv2
import time
import numpy as np
from scipy.signal import find_peaks

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
            avg2.append(np.average(result[i:i+20]))

        peak, _ = find_peaks(np.array(avg), distance=(8.5*(datacount/200)), height=np.array(avg2))
        peaks = len(peak)
        Result2 = peaks * 6
        return Result2
    
    def polyfit(result):
        datacount = len(np.array(result))
        x = np.arange(len(result))
        p = np.poly1d(np.polyfit(x, result, 13))
        pfix = p(x)[:]
        for i in range(30):
            pfix[i] = np.average(pfix[i:i+15])
        for i in range(-25, 0, 1):
            pfix[i] = np.average(pfix[i-15:i])
        peak, _ = find_peaks(np.array(result), distance=(8.5*(datacount/200)), height=pfix)
        Result3 = (len(peak)*6)
        return Result3
    
cam = cv2.VideoCapture(0)
print('[+] Camera starting...')
FrameCount = 0
start_time = round(time.time())

bright_rec = []
while True:
    FrameCount += 1
    check, frame = cam.read()
    if check:
        System_Message.Camera_Success()
    else:
        System_Message.Camera_Failure()
    
    if cv2.waitKey(1) == ord('q'):
        print('[>] Exiting...')
        cv2.destroyAllWindows()
        break
    
    time_now = time.time()
    time_fixed = round(time_now)
    time_passed = time_fixed - start_time
    print(time_passed)
    if time_passed <= 10:
        avgB, avgG, avgR, avgA = cv2.mean(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bright = cv2.mean(gray)[0]
        bright_rec.append(bright)

    else:
        tmp = 0
        cv2.destroyAllWindows()
        lenBright = len(bright_rec)
        for i, x in enumerate(bright_rec[lenBright + 2:lenBright - 2]):
            print(i)
            bright_rec[i] = np.average(bright_rec[i-2:i+2])
        print(f'Subseq returned a BPM: {Algorithms.subseq(bright_rec)}')
        print(f'Avg_calc returned a BPM: {Algorithms.avg_calc(bright_rec)}')
        print(f'Polyfit returned a BPM: {Algorithms.polyfit(bright_rec)}')
        break
print(f'Total Frame Count = {FrameCount}')