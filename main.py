#version 1.1: 
import os
try:
    import cv2
    import numpy as np
    import time
    #import win32gui
    from datetime import datetime
    from tqdm.rich import tqdm
    from UI_Beta2 import Ui_DefaultWindow
except:
    os.system('pip install opencv-python')
    os.system('pip install tqdm')
    os.system('pip install rich')
    os.system('pip install matplotlib')
    os.system('pip install scipy')

import cv2
import numpy as np
import time
#import win32gui
from datetime import datetime
from tqdm.rich import tqdm

def start(skipDMX, camera_select, mode):
    
    '''if mode == 0:
        print('mode is Fast')
        D_speed = "Fast"
    elif mode == 1:
        print('mode is Normal')
        D_speed = "Normal"
    else:
        print('mode is Slow')
        D_speed = "Slow"'''
    start_t = int(time.time())
    cam = cv2.VideoCapture(camera_select)
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    counting = 0
    chk_count = 0
    mx = 0
    mn = 255
    FDetect = False

    passed = False
    beats = 0
    bpm = 0
    brit = -4
    bright_fail_count = 0
    britFailContrl = False
    autobrit = False
    #v0.6.6
    #img = np.empty((300, 300, 3), np.uint8)
    #os.system('WCConfig.exe') #msvc120
    global fatalError
    fatalError = 0

    while True:
        time_now = time.time_ns()
        
        run_t = round(time.time())
        check, frm = cam.read()
        if check:
            cv2.imshow('Camera_Capture', frm)
        else:
            print('Camera Start Failed!')
            return False
        
        #window = win32gui.FindWindow(None, 'Camera_Capture')
        #win_rectPast = win32gui.GetWindowRect(window)
        
        if cv2.waitKey(1) == ord('q'):
            print('Exiting...')
            cv2.destroyAllWindows()
            break
        
        frm = cv2.resize(frm,(600,420))
        avgB, avgG, avgR, avgA = cv2.mean(frm)
        #v0.6.6
        gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        bright = cv2.mean(gray)[0]
        if str(bright)[1] == '.':
            bright_fixed = int(str(bright)[0])
        elif str(bright)[2] == '.':
            bright_fixed = int(str(bright)[0:2])
        else:
            bright_fixed = int(str(bright)[0:3])
        
        # Finger detection
        if avgR > 70 and avgR > (avgB + avgG) and counting <= 10:
            if counting > 6:
                britFailContrl = False
                if brit <= -3:
                    brit = -4 + bright_fail_count
                    cam.set(cv2.CAP_PROP_EXPOSURE, brit)
                elif brit > -3:
                    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
                    autobrit = True
                cam.set(cv2.CAP_PROP_BRIGHTNESS, 100)
            FDetect = True
            counting += 0.2
        elif avgR > 70 and avgR > (avgB + avgG) and counting > 10:
            if brit > -3:
                cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            else:
                cam.set(cv2.CAP_PROP_EXPOSURE, brit)
                cam.set(cv2.CAP_PROP_BRIGHTNESS, 100)
        else:
            if britFailContrl == False:
                bright_fail_count += 1
            britFailContrl = True
            cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            cam.set(cv2.CAP_PROP_BRIGHTNESS, 100)
            FDetect = False
            mx = 0
            mn = 255
            chk_count = 30
            passed = False
            beats = 0
            bpm = 0
            if counting >= 0:
                counting -= 2
        
        if FDetect:
            if passed == False and counting >= 10:
                start_t = run_t
                passed = True
            
            # v0.6.7
            if run_t - start_t == 10 and counting >= 10:
                return True
            
            # Write the brightness values
            if counting >= 10:
                with open('test.txt', 'a', encoding='utf-8') as data:
                    data.write(f'{str(bright)[:6]}\n')
                    data.close()
            # bright_rec.append(str(bright)[:6])

        else:
            with open('test.txt', 'w', encoding='utf-8') as data:
                data.write('')
                data.close()

        print(f"R: {str(avgR)[:6]}, G: {str(avgG)[:6]}, B: {str(avgB)[:6]}, A: {str(bright)[:6]}, FXL: {bright_fixed}, FD: {str(FDetect)}, S: {str(counting)[:6]}, TR: {10-(run_t - start_t)}, EXPO:{cam.get(cv2.CAP_PROP_EXPOSURE)} , ectrl: {britFailContrl}, {bright_fail_count}, {brit}, AE:{autobrit}", flush=True)
        open('result.txt', 'w', encoding='utf-8').write(str(bpm))

        if DMXi2(time_now = time_now, skipDMX=skipDMX) == False:
            return False
        #檢測區塊


def DMXi2(time_now, skipDMX):
    global fatalError
    time_then = time.time_ns()
    #window = win32gui.FindWindow(None, 'Camera_Capture')
    #win_rectNow = win32gui.GetWindowRect(window)
    #print(Pos[0], win_rectNow[0], Pos[1], win_rectNow[1], Pos[2], win_rectNow[2], Pos[3], win_rectNow[3])
    if skipDMX == False:
        #if Pos[0] == win_rectNow[0] and Pos[1] == win_rectNow[1] and Pos[2] == win_rectNow[2] and Pos[3] == win_rectNow[3]:
        time_passed = time_then - time_now
        if fatalError >= 5:
            return False
        if time_passed < 0:
            time_passed = time_passed*-1
            print(time_passed)
            if time_passed > 200000000:
                print(f'偵測到效能問題(err1, failCount = {4-fatalError})\ntime_now = {time_now}\ntime_then = {time_then}\ntime passed = {time_passed}')
                fatalError += 1
        elif time_passed > 200000000:
            print(f'fps = {10 / time_passed}')
            print(f'偵測到效能問題(err2, failCount = {4-fatalError})\ntime_now = {time_now}\ntime_then = {time_then}\ntime passed = {time_passed}')
            fatalError += 1
        elif time_passed == 0:
            print('fps >= 10')
        elif fatalError >= 0:
            fatalError -= 0.2

# v0.6.7
def HR_monitor(D_speed, mx, mn, start_t, run_t):
    with open('test.txt', 'r', encoding='utf-8') as data:
        bright_values =  data.readlines()
    # bright_values = [data[:6] for data in bright_values]
    Bump = False
    rest = True
    beats = 0
    chk_delay = 0

    for i in bright_values:
        i = i[:6]
        # if pow(i, 2) <= pow(0.3*(mx-mn)+mn, 2):
        # if float(i)*float(i) <= 0.3*(mx*mx-mn*mn)+mn*mn:
        if 5*float(i) <= 0.3*(5*mx-5*mn)+5*mn:
            Bump = True
            rest = False
            chk_delay += 1
        else:
            chk_delay = 0
        
        if Bump == True and rest == False:
            beats += 1
            rest = True

    return beats
