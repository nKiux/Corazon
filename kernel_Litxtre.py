#version 13A3
import os
from datetime import datetime
import main

mode = 0
camera_select = 0
bnhmrk = False #僅在 KernelSpeedUP! 開啟時可使用
spd_up_start = True

import cv2
import numpy as np
from tqdm.rich import tqdm
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import find_peaks_cwt
from scipy.signal import iirfilter
from scipy.signal import sosfiltfilt



def start(skipDMX, camera_select, mode):
    import main
    print(f'Checking Program... ({datetime.now()})')
    try:
        import cv2
        import numpy as np
        from tqdm.rich import tqdm
        import matplotlib.pyplot as plt
        from scipy.signal import find_peaks
        from scipy.signal import find_peaks_cwt
        from scipy.signal import iirfilter
        from scipy.signal import sosfiltfilt
    except:
        """
        os.system('pip install opencv-python')
        os.system('pip install tqdm')
        os.system('pip install rich')
        os.system('pip install matplotlib')
        os.system('pip install scipy')
        """

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
    
    if main.start(skipDMX = skipDMX, camera_select = camera_select, mode = mode) == True:
        with open('test.txt', 'r', encoding='utf-8') as res:
            result = [float(line.strip()) for line in res if line]
            res.close()
        
        with open('test.txt', 'r', encoding='utf-8') as res:
            result = [float(line.strip()) for line in res if line]
            res.close()
            
        datacount = len(np.array(result))

        avg = []
        avg2 = []
        for i in range(datacount):
            avg.append(np.average(result[i:i+5]))
            avg2.append(np.average(result[i:i+20]))

        

        peak, _ = find_peaks(np.array(avg), distance=(8.5*(datacount/200)), height=np.array(avg2))
        peaks = len(peak)
        open("result.txt", 'w', encoding="utf-8").write(str(peaks*6))
        #peak2, _ = find_peaks(np.array(result), distance=(8.5*(datacount/200)), height=np.array(avg2))
        plt.plot(np.array(result))
        plt.plot(peak, np.array(avg)[peak], "o")
        #plt.plot(peak2, np.array(result)[peak2], "o")
        plt.plot(np.array(avg), label = "5 steps")
        plt.plot(np.array(avg2), label = "height (20 steps)")
        #plt.plot(np.array(avg2), label = "3 steps")
        plt.legend()
        plt.show()

        cv2.destroyAllWindows()
        return True
    else:
        cv2.destroyAllWindows()
        return False




#start(False, 0 , 0)
