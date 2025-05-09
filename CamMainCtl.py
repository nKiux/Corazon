#version 20
import cv2
import numpy as np
import time
from datetime import datetime
from tqdm.rich import tqdm

def start(camera_select):
    
    start_t = int(time.time())
    cam = cv2.VideoCapture(camera_select)
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    counting = 0
    FDetect = False
    if_reset = False
    reset = False
    passed = False
    global fatalError
    fatalError = 0
    while True:
        time_now = time.time_ns()
        
        run_t = round(time.time())
        check, frm = cam.read()
        if check:
            cv2.imshow('Camera_Capture', frm)
        else:
            print('[-] Camera Start Failed!')
            return False

        if cv2.waitKey(1) == ord('q'):
            print('[>] Exiting...')
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
            FDetect = True
            counting += 0.2
        elif avgR > 70 and avgR > (avgB + avgG) and counting > 10:
            FDetect = True
        else:
            FDetect = False
            passed = False
            if counting >= 0:
                counting -= 2

        
        if FDetect == True and reset == False:
            if passed == False and counting >= 10:
                start_t = run_t
                passed = True
            
            if run_t - start_t == 10 and counting >= 10:
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
                return True
            
            # Write the brightness values
            if counting >= 10:
                with open('test.txt', 'a', encoding='utf-8') as data:
                    data.write(f'{str(bright)[:6]}\n')
                    data.close()

        else:
            if reset == True:
                reset = False
                counting = 7
            passed = False
            with open('test.txt', 'w', encoding='utf-8') as data:
                data.write('')
                data.close()
            
            with open('h_std.txt', 'w', encoding='utf-8') as data:
                data.write('')
                data.close()

        #print(f"R: {str(avgR)[:6]}, G: {str(avgG)[:6]}, B: {str(avgB)[:6]}, A: {str(bright)[:6]}, FXL: {bright_fixed}, FD: {str(FDetect)}, S: {str(counting)[:6]}, TR: {10-(run_t - start_t)}, EXPO:{cam.get(cv2.CAP_PROP_EXPOSURE)} , ectrl: {britFailContrl}, {bright_fail_count}, {brit}, AE:{autobrit}, res:{if_reset} .....", end = "\r", flush=True)

        if_reset = DMX3(time_now = time_now)
        if if_reset == 102:
            reset = True
        elif if_reset == False:
            return False
        #檢測區塊


def DMX3(time_now):
    global fatalError
    time_then = time.time_ns()
    time_passed = time_then - time_now
    if fatalError >= 5:
        return False
    if time_passed > 200000000:
        print(f'fps = {10 / time_passed}')
        print(f'偵測到效能問題(failCountdown = {4-fatalError})')
        #print(f'偵測到效能問題(failCount = {4-fatalError})\ntime_now = {time_now}\ntime_then = {time_then}\ntime passed = {time_passed}')
        fatalError += 1
        return 102
    elif time_passed == 0:
        print('fps >= 10')
    elif fatalError >= 0:
        fatalError -= 0.2
