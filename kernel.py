import cv2
import numpy as np
cam = cv2.VideoCapture(0)

img = np.empty((300, 300, 3), np.uint8)



while(True):
    check, frm = cam.read()
    if check:
        cv2.imshow('cap', frm)
    else:
        break
    if cv2.waitKey(1) == ord('q'):
        break
    avgR, avgG, avgB, avgAlp = cv2.mean(frm)
    for row in range(300):
        for col in range(300):
            img[row][col] = [avgR, avgG, avgB]
    cv2.imshow('img', img)
    print(f"R: {avgR}, G: {avgG}, B: {avgB}, A: {avgAlp}")
    #print(frm)
