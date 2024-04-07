# base version 0.6.8
import os
from datetime import datetime

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
    print(f'Checking Program... ({datetime.now()})')
    try:
        import cv2
        import numpy as np
        from tqdm.rich import tqdm
        from main import start
        import matplotlib.pyplot as plt
    except:
        os.system('pip install opencv-python')
        os.system('pip install tqdm')
        os.system('pip install rich')
        os.system('pip install matplotlib')

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
    start = start(skipDMX = skipDMX, camera_select = camera_select, mode = mode)
    if start == False:
        with open('test.txt', 'r', encoding='utf-8') as res:
            # result = [(32 * float(line.strip())) - 500 for line in res if line]
            result  = res.readlines()
            result = [float(data[:6]) for data in result]
            # peaks = scipy.signal.find_peaks(result)[0]
            res.close()
        with open('h_std.txt', 'r', encoding='utf-8') as tmp:
            avg = tmp.readlines()
            avg = [float(data[:6]) for data in avg]
            tmp.close()
        with open('peaks.txt', 'r', encoding='utf-8') as tmp:
            peaks = tmp.readline()
            peaks = peaks.split()
            peaks = [int(data) for data in peaks]
            tmp.close()

        plt.plot(result)
        plt.plot(avg)
        plt.plot(peaks, np.array(result)[peaks], "o")
        plt.title('Brightness Line Chart')
        plt.xlabel('Frame')
        plt.ylabel('Value w/ avg')
        plt.show()

        cv2.destroyAllWindows()

        # clear the data
        with open('test.txt', 'w', encoding='utf-8') as data:
            data.write('')
            data.close()
        
        return False
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