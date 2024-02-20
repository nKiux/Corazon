#version v0.4.3: Light Engine FiX!
import os
import datetime

camera_select = 0
bnhmrk = False #僅在 KernelSpeedUP! 開啟時可使用
spd_up_start = True

print('Checking Program...')
try:
    import cv2
    import numpy as np
    from tqdm.rich import tqdm
    from main import start, benchmark
except:
    os.system('pip install opencv-python')
    os.system('pip install tqdm')
    os.system('pip install rich')

if spd_up_start == False:
    print('Check Completed!')
    print('Initializing Program...')
    #initialize
    counting = 0
    chk_count = 0
    prog = tqdm(total=100)
    prog.update(20)
    cam = cv2.VideoCapture(camera_select)
    img = np.empty((300, 300, 3), np.uint8)
    mx = 0
    mn = 255
    FDetect = False
    prog.update(20)
    print('Initialize Completed!')
    print('Starting Camera...')
    #initial finished
    #start camera
    check, frm = cam.read()
    if check:
        print('Initializing Camera...')
        print('Camera Initialize Finished!')
        prog.update(30)
        cam.release()
        cam = cv2.VideoCapture(camera_select)
        prog.update(30)
        prog.close()
        print('Testing...')
        if benchmark(camera_select = camera_select) == True:
            start(camera_select=camera_select)
        else:
            print('Test Failed... Closing')
            exit()
    else:
        print('Camera Start Failed!')
else:
    if bnhmrk == True:
        benchmark(camera_select = camera_select)
    else:
        start(camera_select = camera_select)