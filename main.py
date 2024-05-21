#version 1.3.2
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
    start_t = int(time.time())
    cam = cv2.VideoCapture(camera_select)
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    counting = 0
    FDetect = False

    if_reset = False
    reset = False

    bright_rec = []
    h_std = [] # 高度標準
    h_mov = 0.200 # height vertical translating amount

    passed = False
    bpm = 0

    brit = -4
    bright_fail_count = 0
    britFailContrl = False
    autobrit = False

    global fatalError
    fatalError = 0
    aeset = False

    while True:
        time_now = time.time_ns()
        
        run_t = round(time.time())
        check, frm = cam.read()
        if check:
            cv2.imshow('Camera_Capture', frm)
        else:
            print('Camera Start Failed!')
            return False

        # Quit
        if cv2.waitKey(1) == ord('q'):
            print('Exiting...')
            cv2.destroyAllWindows()
            break
        
        frm = cv2.resize(frm,(600,420))
        avgB, avgG, avgR, avgA = cv2.mean(frm)
        
        gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        bright = cv2.mean(gray)[0]

        # fix brightness
        if str(bright)[1] == '.':
            bright_fixed = int(str(bright)[0])
        elif str(bright)[2] == '.':
            bright_fixed = int(str(bright)[0:2])
        else:
            bright_fixed = int(str(bright)[0:3])
        
        # Finger detection
        if avgR > 70 and avgR > (avgB + avgG) and counting <= 10:
            if counting > 6:
                if brit <= -3:
                    brit = -4 + bright_fail_count
                    cam.set(cv2.CAP_PROP_EXPOSURE, brit)
                elif brit > -3:
                    if aeset == False:
                        cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
                    autobrit = True
                    aeset = True
                cam.set(cv2.CAP_PROP_BRIGHTNESS, 100)
            FDetect = True
            counting += 0.2

        elif avgR > 70 and avgR > (avgB + avgG) and counting > 10 and aeset == False:
            if brit > -3:
                cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
                aeset = True
            else:
                cam.set(cv2.CAP_PROP_EXPOSURE, brit)
                cam.set(cv2.CAP_PROP_BRIGHTNESS, 100)
                aeset = True
            
        elif avgR > 70 and avgR > (avgB + avgG) and counting > 10 and aeset == True:
            pass
            
        else:
            if britFailContrl == False:
                bright_fail_count += 1
            
            britFailContrl = True
            
            if aeset == False:
                cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
                cam.set(cv2.CAP_PROP_BRIGHTNESS, 100)
                aeset = True
            
            FDetect = False
            passed = False
            bpm = 0
            if counting >= 0:
                counting -= 2
        
        if FDetect and counting >= 10 and reset == False:
            if passed == False:
                start_t = run_t
                passed = True
            
            # v0.6.7
            if run_t - start_t == 15:
                with open('h_std.txt', 'a', encoding='utf-8') as data:
                    with open('test.txt', 'r', encoding='utf-8') as tmp:
                        bright_rec = tmp.readlines()
                        bright_rec = [float(x) for x in bright_rec]
                        tmp.close()
                    
                    for i, bri in enumerate(bright_rec): # appending brightness avg of 15 sec
                        if i >= len(bright_rec)-16:
                            data.write(f'{avg_bri}\n')
                        else:
                            h_mov = 0.2*(max(bright_rec[i:i+15]) - min(bright_rec[i:i+15])) # height vertical translating amount
                            avg_bri = np.average(bright_rec[i:i+15]) + h_mov
                            data.write(f'{avg_bri}\n')
                    data.close()
                # beats = HR_monitor(h_std)
                # bpm = beats * 4 
                # open('result.txt', 'w', encoding='utf-8').write(str(bpm))
                # print(f"\nBeats: {beats}, BPM: {bpm}", flush=True)
                return True
            
            # Write the brightness values
            with open('test.txt', 'a', encoding='utf-8') as data:
                data.write(f'{str(bright)[:6]}\n')
                # data.close()

        else:
            if reset == True:
                reset = False
                counting = 7
            passed = False
            # clear data
            with open('test.txt', 'w', encoding='utf-8') as data:
                data.write('')
                data.close()
            with open('h_std.txt', 'w', encoding='utf-8') as data:
                data.write('')
                data.close()

        print(f"R: {str(avgR)[:6]}, G: {str(avgG)[:6]}, B: {str(avgB)[:6]}, A: {str(bright)[:6]}, FXL: {bright_fixed}, FD: {str(FDetect)}, S: {str(counting)[:6]}, TR: {10-(run_t - start_t)}, EXPO:{cam.get(cv2.CAP_PROP_EXPOSURE)} , ectrl: {britFailContrl}, {bright_fail_count}, {brit}, AE:{autobrit}, res:{if_reset} .....", end = "\r", flush=True)
        open('result.txt', 'w', encoding='utf-8').write(str(bpm))

        if_reset = DMX3(time_now = time_now, skipDMX=skipDMX)
        if if_reset == 102:
            reset = True
        elif if_reset == False:
            return False
        #檢測區塊


def DMX3(time_now, skipDMX):
    global fatalError
    time_then = time.time_ns()
    #window = win32gui.FindWindow(None, 'Camera_Capture')
    #win_rectNow = win32gui.GetWindowRect(window)
    #print(Pos[0], win_rectNow[0], Pos[1], win_rectNow[1], Pos[2], win_rectNow[2], Pos[3], win_rectNow[3])
    
    #if Pos[0] == win_rectNow[0] and Pos[1] == win_rectNow[1] and Pos[2] == win_rectNow[2] and Pos[3] == win_rectNow[3]:
    time_passed = time_then - time_now
    if fatalError >= 5:
        return False
        """
            if time_passed < 0:
            time_passed = time_passed*-1
            print(time_passed)
            if time_passed > 200000000:
            print(f'偵測到效能問題(err1, failCount = {4-fatalError})\ntime_now = {time_now}\ntime_then = {time_then}\ntime passed = {time_passed}')
            fatalError += 1
        """
    if time_passed > 200000000:
        print(f'fps = {10 / time_passed}')
        print(f'偵測到效能問題(failCount = {4-fatalError})\ntime_now = {time_now}\ntime_then = {time_then}\ntime passed = {time_passed}')
        fatalError += 1
        return 102
    elif time_passed == 0:
        print('fps >= 10')
    elif fatalError >= 0:
        fatalError -= 0.2
