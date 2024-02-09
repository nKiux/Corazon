import os
print('Checking Program...')
from tqdm.rich import tqdm
try:
    import cv2
    import numpy as np
    
except:
    os.system('pip install opencv-python')
    os.system('pip install tqdm')
    os.system('pip install rich')

print('Check Completed!')
print('Initializing Program...')
prog = tqdm(total=100)
prog.update(20)
cam = cv2.VideoCapture(0)
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
    #cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    cam.set(cv2.CAP_PROP_EXPOSURE, -4)
    cam.set(cv2.CAP_PROP_SHARPNESS, 5)
    cam.set(cv2.CAP_PROP_CONTRAST, 20.0)
    print('Camera Initialize Finished!')
    prog.update(30)
    cam.release()
    cam = cv2.VideoCapture(0)
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

    avgB, avgG, avgR, avgAlp = cv2.mean(frm)

    gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
    bright = cv2.mean(gray)[0]

    mosaic = frm[300::20, 300::20]
    cv2.namedWindow('mos', flags=cv2.WINDOW_NORMAL)
    cv2.resizeWindow('mos', 400, 200)
    cv2.imshow('mos', mosaic)

    for row in range(300):
        for col in range(300):
            img[row][col] = [avgB, avgG, avgR]
    

    if str(bright)[1] == '.':
        bright_fixed = int(str(bright)[0])
    elif str(bright)[2] == '.':
        bright_fixed = int(str(bright)[0:2])
    else:
        bright_fixed = int(str(bright)[0:3])
    
    if avgR > 100 and avgB < 50 and avgG < 50:
        if mx < bright_fixed:
            mx = bright_fixed
        if mn > bright_fixed:
            mn = bright_fixed
        FDetect = True
    else:
        FDetect = False

    cv2.imshow('img', img)
    print(f"R: {str(avgR)[:6]}, G: {str(avgG)[:6]}, B: {str(avgB)[:6]}, A: {str(bright)[:6]}, MX: {str(mx)}, MN: {str(mn)}, FXL: {bright_fixed}, Finger Detected: {FDetect}")


    #print(frm)
