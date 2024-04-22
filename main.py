# base version 0.6.7:
import os
import cv2
import numpy as np
import scipy.signal
import time
import win32gui
from datetime import datetime
from tqdm.rich import tqdm
from UI_Beta2 import Ui_DefaultWindow

def benchmark(camera_select):
    fps = 0
    updates = 0
    cam = cv2.VideoCapture(camera_select)
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
        updates += 1
        check, frm = cam.read()
        if check:
            pass
        else:
            return False
        '''
        if cv2.waitKey(1) == ord('q'):
            print('Exiting...')
            cv2.destroyAllWindows()
            exit()
        '''
        frm = cv2.resize(frm,(600,420))
        avgB, avgG, avgR, avgAlp = cv2.mean(frm)
        gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        bright = cv2.mean(gray)[0]
        #v0.6.6
        '''
        for row in range(300):
            for col in range(300):
                img[row][col] = [avgB, avgG, avgR]
        '''
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
    print(f'updates =  {updates}')
    #fps = updates / time_passed
    #print(f'fps = {fps}')
    if time_passed < 0:
        time_passed = 60 + time_passed
        if time_passed > 1:
            print(f'fps = {10 / time_passed}')
            print('Test Failed')
            return False
        else:
            return True
    elif time_passed > 1:
        print(f'fps = {10 / time_passed}')
        print('Test Failed')
        return False
    else:
        if time_passed == 0:
            print('fps >= 10')
        print('Test Passed')
        return True
    #10 frames in 3 secs


def start(skipDMX, camera_select, mode):
    
    start_t = int(time.time())
    cam = cv2.VideoCapture(camera_select)
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    counting = 0
    chk_count = 0
    mx = 0
    mn = 255
    FDetect = False
    
    bright_rec = []
    h_std = [] # 高度標準
    h_mov = 0.200 # height vertical translating amount

    passed = False
    beats = 0
    bpm = 0
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
        
        window = win32gui.FindWindow(None, 'Camera_Capture')
        win_rectPast = win32gui.GetWindowRect(window)
        
        if cv2.waitKey(1) == ord('q'):
            print('Exiting...')
            cv2.destroyAllWindows()
            break
        
        frm = cv2.resize(frm,(600,420))
        avgB, avgG, avgR, avgA = cv2.mean(frm)
        #v0.6.6
        gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        bright = cv2.mean(gray)[0]
        '''
        blur = cv2.blur(gray, (10,5))
        cv2.imshow('denoise', blur)
        for row in range(300):
            for col in range(300):
                img[row][col] = [avgB, avgG, avgR]
        '''

        if str(bright)[1] == '.':
            bright_fixed = float(str(bright)[0:2])
        elif str(bright)[2] == '.':
            bright_fixed = float(str(bright)[0:3])
        else:
            bright_fixed = float(str(bright)[0:4])
        # bright_fixed = float(np.round(bright, 1))
        
        # Finger detection
        if avgR > 60 and avgR > (avgB+avgG)*2 and counting <= 10:
            FDetect = True
            counting += 0.20
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
            passed = False
            beats = 0
            bpm = 0
            h_std = []
            h_mov = 0.200
            bright_rec = []
            if counting >= 0:
                counting -= 2
        
        if FDetect and counting >= 10:
            if passed == False:
                start_t = run_t
                passed = True
            
            # if run_t - start_t <= 5:
            #     bright_rec.append(bright)

            # else: # run_t - start_t > 5

            if run_t - start_t == 15:
                with open('h_std.txt', 'a', encoding='utf-8') as data:
                    for i, bri in enumerate(bright_rec): # appending brightness avg
                        if i >= len(bright_rec)-16:
                            h_std.append(avg_bri)
                        else:
                            h_mov = 0.2*(max(bright_rec[i:i+15]) - min(bright_rec[i:i+15]))
                            avg_bri = np.average(bright_rec[i:i+15]) + h_mov
                            h_std.append(avg_bri)
                        data.write(f'{avg_bri}\n')
                    
                    data.close()

                beats = HR_monitor(h_std)
                bpm = beats * 4 
                open('result.txt', 'w', encoding='utf-8').write(str(bpm))
                print(f"\nBeats: {beats}, BPM: {bpm}", flush=True)
                return True
            
            # Write the brightness values
            with open('test.txt', 'a', encoding='utf-8') as data:
                data.write(f'{str(bright)[:6]}\n')
                data.close()
            
            bright_rec.append(bright)

            # avg_bri = str(np.average(bright_rec))[:6] # delete l8r
            # h_std.append(float(avg_bri)) # delete l8r
            # with open('h_std.txt', 'a', encoding='utf-8') as data:
            #     data.write(f'{avg_bri}\n')
            #     data.close() # delete l8r

            # h_std.append(0.8*(mx-mn)+mn)
            
        else:
            with open('test.txt', 'w', encoding='utf-8') as data:
                data.write('')
                data.close()
            with open('h_std.txt', 'w', encoding='utf-8') as data:
                data.write('')
                data.close()

        print(f"R: {str(avgR)[:6]}, G: {str(avgG)[:6]}, B: {str(avgB)[:6]}, A: {str(bright)[:6]}, MX: {mx}, MN: {mn} (reset in {30 - chk_count}), FXL: {bright_fixed}, Finger Detected: {str(FDetect)}, score: {str(counting)[:6]} .....", end="\r", flush=True)
        open('result.txt', 'w', encoding='utf-8').write(str(bpm))

        if DMXi2(time_now = time_now, skipDMX=skipDMX, Pos=win_rectPast) == False:
            return False
        #檢測區塊


def DMXi2(time_now, skipDMX, Pos):
    global fatalError
    time_then = time.time_ns()
    window = win32gui.FindWindow(None, 'Camera_Capture')
    win_rectNow = win32gui.GetWindowRect(window)
    #print(Pos[0], win_rectNow[0], Pos[1], win_rectNow[1], Pos[2], win_rectNow[2], Pos[3], win_rectNow[3])
    if skipDMX == False:
        if Pos[0] == win_rectNow[0] and Pos[1] == win_rectNow[1] and Pos[2] == win_rectNow[2] and Pos[3] == win_rectNow[3]:
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


def HR_monitor(height_standard):
    # read file
    with open('test.txt', 'r', encoding='utf-8') as data:
        bright_values =  data.readlines()
    
    bright_values = [float(data[:6]) for data in bright_values]
    
    peak_idx = scipy.signal.find_peaks(bright_values, height=np.array(height_standard), distance=7)[0] # peak indexes
    with open('peaks.txt', 'w', encoding='utf-8') as data:
        for i in peak_idx:
            data.write(f'{i} ')
        data.close()

    return len(peak_idx)