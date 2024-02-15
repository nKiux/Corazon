#version v3.2: Light Engine
import os

camera_select = 2
print('Checking Program...')
try:
    import cv2
    import numpy as np
    from tqdm.rich import tqdm
except:
    os.system('pip install opencv-python')
    os.system('pip install tqdm')
    os.system('pip install rich')

print('Check Completed!')
print('Initializing Program...')
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

check, frm = cam.read()
if check:
    print('Initializing Camera...')
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    #cam.set(cv2.CAP_PROP_EXPOSURE, 4)
    cam.set(cv2.CAP_PROP_SHARPNESS, 5)
    cam.set(cv2.CAP_PROP_CONTRAST, 20.0)
    print('Camera Initialize Finished!')
    prog.update(30)
    cam.release()
    cam = cv2.VideoCapture(camera_select)
    prog.update(30)
    prog.close()
else:
    print('Camera Start Failed!')


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

    '''mosaic = frm[300::20, 300::20]
    cv2.namedWindow('mos', flags=cv2.WINDOW_NORMAL)
    cv2.resizeWindow('mos', 400, 200)
    cv2.imshow('mos', mosaic)'''

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
