import os
import cv2
import numpy as np
import time
from datetime import datetime
from tqdm.rich import tqdm

beats = 0

def benchmark(camera_select):
    cam = cv2.VideoCapture(camera_select)
    check, frm = cam.read()
    counting = 0
    chk_count = 0
    mx = 0
    mn = 255
    FDetect = False
    img = np.empty((300, 300, 3), np.uint8)
    print(str(datetime.now()))
    time_now = int(str(datetime.now())[17:19])
    print(time_now)
    prog = tqdm(total=100)
    for i in range(10):
        
        check, frm = cam.read()
        if check:
            cv2.imshow('cap', frm)
        else:
            print('Camera Start Failed!')
            break

        if cv2.waitKey(1) == ord('q'):
            print('Exiting...')
            break
        frm = cv2.resize(frm,(600,420))
        avgB, avgG, avgR, avgAlp = cv2.mean(frm)
        gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        bright = cv2.mean(gray)[0]

        blur = cv2.blur(gray, (10,5))
        cv2.imshow('denoise', blur)
        for row in range(300):
            for col in range(300):
                img[row][col] = [avgB, avgG, avgR]
        
        if str(bright)[1] == '.':
            bright_fixed = int(str(bright)[0])
        elif str(bright)[2] == '.':
            bright_fixed = int(str(bright)[0:2])
        else:
            bright_fixed = int(str(bright)[0:3])
        
        
        if avgR > 100 and avgB < 50 and avgG < 50 and counting <= 10:
            FDetect = True
            counting += 0.2
        elif avgR > 100 and avgB < 50 and avgG < 50 and counting > 10:
            if mx < bright_fixed:
                mx = bright_fixed
            if mn > bright_fixed:
                mn = bright_fixed
            if chk_count == 30:
                chk_count = 0
                mx = 0
                mn = 255
            else:
                chk_count += 1
        else:
            FDetect = False
            mx = 0
            mn = 255
            chk_count = 30
            if counting >= 0:
                counting -= 2
        prog.update(10)
        #print(f"R: {str(avgR)[:6]}, G: {str(avgG)[:6]}, B: {str(avgB)[:6]}, A: {str(bright)[:6]}, MX: {str(mx)}, MN: {str(mn)} (reset in {30 - chk_count}), FXL: {bright_fixed}, Finger Detected: {FDetect}, score: {counting}")
    time_then = int(str(datetime.now())[17:19])
    print(time_then)
    time_passed = time_then - time_now
    if time_passed < 0:
        time_passed = 60 + time_passed
        if time_passed > 3:
            print('Test Failed')
    elif time_passed > 3:
        print('Test Failed')
    else:
        print('Test Passed')
    #10 frames in 3 secs

def start(camera_select):
    global beats
    start_t = int(time.time())
    cam = cv2.VideoCapture(camera_select)
    check, frm = cam.read()
    os.system("cam.exe")
    # os.system("cam.exe --savedev")

    counting = 0
    chk_count = 0
    mx = 0
    mn = 255
    FDetect = False
    bright_rec = []

    D_speed = "Fast" # Detection speed
    passed = False
    beats = 0
    bpm = 0
    img = np.empty((300, 300, 3), np.uint8)

    # cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    # cam.set(cv2.CAP_PROP_SHARPNESS, 5)
    # cam.set(cv2.CAP_PROP_CONTRAST, 20.0)
    
    while(True):
        blank = "....."
        run_t = round(time.time())
        check, frm = cam.read()
        if check:
            cv2.imshow('cap', frm)
        else:
            print('Camera Start Failed!')
            break

        if cv2.waitKey(1) == ord('q'):
            print('Exiting...')
            break
        frm = cv2.resize(frm,(600,420))
        avgB, avgG, avgR, avgAlp = cv2.mean(frm)
        gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        bright = cv2.mean(gray)[0]

        '''mosaic = frm[300::20, 300::20]
        cv2.namedWindow('mos', flags=cv2.WINDOW_NORMAL)
        cv2.resizeWindow('mos', 400, 200)
        cv2.imshow('mos', mosaic)'''

        blur = cv2.blur(gray, (10,5))
        cv2.imshow('denoise', blur)
        for row in range(300):
            for col in range(300):
                img[row][col] = [avgB, avgG, avgR]
        

        # Brightness config
        if str(bright)[1] == '.':
            bright_fixed = int(str(bright)[0])
        elif str(bright)[2] == '.':
            bright_fixed = int(str(bright)[0:2])
        else:
            bright_fixed = int(str(bright)[0:3])
        
        # Finger Detection
        # if avgR > 100 and avgB < 50 and avgG < 50 and counting <= 10: # original
        # if avgR > 90 and avgB < 50 and avgG < 100 and counting <= 10: # fixed ver.1
        if avgR > 60 and avgR > (avgB+avgG)*2 and counting <= 10: # fixed ver.2
            FDetect = True
            counting += 0.2
        # elif avgR > 90 and avgB < 50 and avgG < 100 and counting > 10:
        elif avgR > 60 and avgR > (avgB+avgG)*2 and counting > 10:
            if mx < bright_fixed:
                mx = bright_fixed
            if mn > bright_fixed:
                mn = bright_fixed
            if chk_count == 30:
                chk_count = 0
                mx = 0
                mn = 255
            else:
                chk_count += 1
        else:
            FDetect = False
            mx = 0
            mn = 255
            chk_count = 30
            bright_rec = []
            passed = False
            if counting >= 0:
                counting -= 2

        # 找出低峰
        # mean_brightness = np.mean(brightness_rec)
        # std_brightness = np.std(brightness_rec)
        # threshold = mean_brightness - std_brightness  # 這裡以平均值減去標準差作為低峰的標準
            # 只要值低於 平均_標準差，則視為低峰 <-- 待測試
        
        # low_peaks_indices = np.where(brightness_rec < threshold)[0]
        # low_peaks_rec = brightness_rec[low_peaks_indices]

        if FDetect:
            if passed == False:
                start_t = run_t
                passed = True
            
            bright_rec.append(bright)
            if (run_t-start_t) >= 5:
                # bright_rec.pop(0)
                print("bimbimbambam")
            
            beats = HR_monitor(D_speed, bright_rec, mx, mn, start_t, run_t)
            # print(f"bright_rec: {len(bright_rec)}")
            if D_speed == "Fast":
                bpm = beats * 12
            elif D_speed == "Normal":
                bpm = beats * 6
            else: # D_speed == "Slow"
                bpm = beats * 4

        cv2.imshow('img', img)
        
        print("\rR: %s, G: %s, B: %s, A: %s, MX: %d, MN: %d (reset in %d), FXL: %d, Finger Detected: %s, score: %d, Beats: %d, BPM: %d, Stored Frames: %d %s" %( (str(avgR)[:6]), str(avgG)[:6], (str(avgB)[:6]), str(bright)[:6], mx, mn, (30 - chk_count), bright_fixed, str(FDetect), counting, beats, bpm, len(bright_rec), blank ), end="")
        # print(f"R: {str(avgR)[:6]}, G: {str(avgG)[:6]}, B: {str(avgB)[:6]}, A: {str(bright)[:6]}, MX: {mx}, MN: {mn} (reset in {30 - chk_count}), FXL: {bright_fixed}, Finger Detected: {FDetect}, score: {counting}")

# To-Do List
    # 找出最佳算法 (what if mean w/ std)
    # 解決劇烈波動所產生影響 (How to ignore or skip)
    # make it work

def HR_monitor(D_speed, bright_values, mx, mn, start_t, run_t):
    global beats
    Bump = False
    rest = True
    # beats = 0
    chk_delay = 0

    for i in bright_values:
        # if pow(i, 2) <= 0.3*(pow(mx, 2)-pow(mn, 2))+pow(mn, 2):
        if pow(i, 2) <= pow(0.3*(mx-mn)+mn, 2):
        # if i*i <= 0.3*(mx*mx-mn*mn)+mn*mn:
            Bump = True
            rest = False    
            chk_delay += 1
        else:
            chk_delay = 0
        
        if Bump == True and rest == False and chk_delay == 3:
            beats += 1
            rest = True
        
        if D_speed == "Fast":
            if (run_t-start_t)%5 == 0 and (run_t-start_t) >= 5:
                beats = 0
                return beats
        elif D_speed == "Normal":
            if (run_t-start_t)%10 == 0 and (run_t-start_t) >= 10:
                return beats
        else: # D_speed == "Slow"
            if (run_t-start_t)%15 == 0 and (run_t-start_t) >= 15:
                return beats
    
    return beats


        # print(frm)