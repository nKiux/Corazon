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
        subseq = subseq_algo()

        finalResult = (polft + subseq) / 2
        print(finalResult)
        open('result.txt', 'w', encoding='utf-8').write(str(finalResult))
        cv2.destroyAllWindows()
        return True
    else:
        cv2.destroyAllWindows()
        return False
#start(False, 0 , 0)

# ----------- algorithms ----------- #
figure, axis = plt.subplots(1, 2) # rows, columns
def subseq_algo():
    # read file
    with open('test.txt', 'r', encoding='utf-8') as data:
        bright_values =  data.readlines()

    with open('h_std.txt', 'r', encoding='utf-8') as tmp:
        avg = tmp.readlines()
        avg = [float(data[:6]) for data in avg]
        height_standard = np.array(avg)
        tmp.close()
    
    bright_values = np.array([float(data[:6]) for data in bright_values])
    # height_standard = np.array(height_standard)
    
    peak_idx = find_peaks(bright_values, height=np.array(height_standard), distance=7)[0] # peak indexes
    
    # # hand-made peak finder BETA
    # peak_idx = []
    # for i, x in enumerate(bright_values):
    #     if i == 0 or i == len(bright_values)-1: # first & last
    #         continue
    #     else:
    #         if x > bright_values[i-1] and x > bright_values[i+1]: # peak == True
    #             if x >= height_standard[i] and i > peak_idx[len(peak_idx)-1]+7: # the peak we want
    #                 peak_idx.append(i) # write the peak

    axis[0].plot(bright_values)
    axis[0].plot(height_standard)
    axis[0].plot(peak_idx, np.array(bright_values)[peak_idx], "o")
    axis[0].set_title('Brightness Line Chart')

    Result1 = (len(peak_idx)*4)

    return Result1


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
    
    axis[1].plot(np.array(result))
    # plt.xlabel('frames')
    # plt.ylabel('Brightness')
    axis[1].plot(peak, np.array(result)[peak], 'x')
    axis[1].plot(x, pfix - 0.02, '-')
    plt.show()
    
    Result2 = (len(peak)*4)
    # print(finalResult)
    # open('result.txt', 'w', encoding='utf-8').write(str(finalResult))
    return Result2