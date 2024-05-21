#version 1.3.2
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
    
    if main.start(skipDMX = skipDMX, camera_select = camera_select, mode = mode) == True:
        polft = polft_algorithm()
        cv2.destroyAllWindows()
        return True
    else:
        cv2.destroyAllWindows()
        return False

def polft_algorithm():
    with open('test.txt', 'r', encoding='utf-8') as res:
            result = [float(line.strip()) for line in res if line]
            res.close()
    datacount = len(np.array(result))
    #peak = find_peaks_cwt(np.array(result), widths=np.arange(5,11))
    #peak= find_peaks_cwt(np.array(result), widths=result)
    x = np.arange(len(result))
    p = np.poly1d(np.polyfit(x, result, 13))
    pfix = p(x)[:]
    for i in range(30):
        pfix[i] = np.average(pfix[i:i+15])
    for i in range(-25, 0, 1):
        pfix[i] = np.average(pfix[i-15:i])
    peak, _ = find_peaks(np.array(result), distance=(8.5*(datacount/200)), height=pfix)
    print(peak)
    
    plt.plot(np.array(result))
    plt.xlabel('frames')
    plt.ylabel('Brightness')
    plt.plot(peak, np.array(result)[peak], 'x')
    plt.plot(x, pfix - 0.02, '-')
    plt.show()
    
    finalResult = (len(peak)*6)
    print(finalResult)
    open('result.txt', 'w', encoding='utf-8').write(str(finalResult))
    return finalResult

#start(False, 0 , 0)
