#version 0.9
import os
from datetime import datetime
import main

mode = 0
camera_select = 0
bnhmrk = False #僅在 KernelSpeedUP! 開啟時可使用
spd_up_start = True

def pure_benchmark(camera_select):
    try:
        import cv2
        import numpy as np
        from tqdm.rich import tqdm
        from main import benchmark
        import matplotlib
        
    except:
        os.system('pip install opencv-python')
        os.system('pip install tqdm')
        os.system('pip install rich')
        os.system('pip install matplotlib')
    return benchmark(camera_select = camera_select)

def start(skipDMX, camera_select, mode):
    import main
    print(f'Checking Program... ({datetime.now()})')
    try:
        import cv2
        import numpy as np
        from tqdm.rich import tqdm
        import matplotlib.pyplot as plt
        from scipy.signal import find_peaks
    except:
        os.system('pip install opencv-python')
        os.system('pip install tqdm')
        os.system('pip install rich')
        os.system('pip install matplotlib')
        os.system('pip install scipy')

    prog = tqdm(total=100)
    prog.update(20)
    print(f'Check Completed! ({datetime.now()})')
    print(f'Initializing Program... ({datetime.now()})')
    prog.update(20)
    open('result.txt', 'a', encoding='utf-8').close()
    prog.update(10)
    open('result.txt', 'w', encoding='utf-8').close()
    prog.update(10)
    open('test.txt', 'a', encoding='utf-8').close()
    prog.update(10)
    open('test.txt', 'w', encoding='utf-8').close()
    prog.update(10)
    prog.close()
    
    if main.start(skipDMX = skipDMX, camera_select = camera_select, mode = mode) == False:
        with open('test.txt', 'r', encoding='utf-8') as res:
            result = [int((300 * float(line.strip()))) - 500 for line in res if line]
            res.close()
        datacount = len(np.array(result))
        peak, _ = find_peaks(np.array(result), distance = (11*(datacount/200)))
        #peak= find_peaks_cwt(np.array(result), widths=result)
        print(peak)
        plt.plot(np.array(result))
        plt.xlabel('frames')
        plt.ylabel('Brightness (300X)')
        plt.plot(peak, np.array(result)[peak], 'x')
        plt.show()
        finalResult = (len(peak)*6)
        print(finalResult)
        open('result.txt', 'w', encoding='utf-8').write(str(finalResult))
        cv2.destroyAllWindows()
        return False
    else:
        cv2.destroyAllWindows()

"""
    if kernel_speedUP == False:
        print(f'Check Completed! ({datetime.now()})')
        print(f'Initializing Program... ({datetime.now()})')
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
        print(f'Initialize Completed! ({datetime.now()})')
        print(f'Starting Camera... ({datetime.now()})')
        #initial finished
        #start camera
        check, frm = cam.read()
        if check:
            print(f'Camera Initialize Finished! ({datetime.now()})')
            prog.update(30)
            cam.release()
            cam = cv2.VideoCapture(camera_select)
            prog.update(30)
            prog.close()
            '''
            print(f'Testing... ({datetime.now()})')
            if benchmark(camera_select = camera_select) == True:
                open('result.txt', 'a', encoding='utf-8').close()
                open('result.txt', 'w').close()
                start(camera_select=camera_select, mode = mode)
            else:
                print(f'Test Failed... Closing ({datetime.now()})')
                exit()
            '''
            open('result.txt', 'a', encoding='utf-8').close()
            open('result.txt', 'w', encoding='utf-8').close()
            open('test.txt', 'a', encoding='utf-8').close()
            open('test.txt', 'w', encoding='utf-8').close()
            start(camera_select=camera_select, mode = mode)
            cv2.destroyAllWindows()
        else:
            print(f'Camera Start Failed! ({datetime.now()})')
            return False
        
    else:
        open('result.txt', 'a', encoding='utf-8').close()
        open('result.txt', 'w', encoding='utf-8').close()

        open('test.txt', 'a', encoding='utf-8').close()
        open('test.txt', 'w', encoding='utf-8').close()
        if start(camera_select = camera_select, mode = mode) == False:
            cv2.destroyAllWindows()
            return False
        

"""