import os
import cv2
import numpy as np
from datetime import datetime
from tqdm.rich import tqdm

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
            check = check
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
    elif time_passed > 1:
        print('Test Failed')
        return False
    else:
        print('Test Passed')
        return True
    #10 frames in 3 secs

def start(camera_select):
    cam = cv2.VideoCapture(camera_select)
    check, frm = cam.read()
    counting = 0
    chk_count = 0
    mx = 0
    mn = 255
    FDetect = False
    img = np.empty((300, 300, 3), np.uint8)
    os.system('WCConfig.exe') #msvc120
    
    while(True):
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

        cv2.imshow('img', img)
        print(f"R: {str(avgR)[:6]}, G: {str(avgG)[:6]}, B: {str(avgB)[:6]}, A: {str(bright)[:6]}, MX: {str(mx)}, MN: {str(mn)} (reset in {30 - chk_count}), FXL: {bright_fixed}, Finger Detected: {FDetect}, score: {counting}")


        #print(frm)
