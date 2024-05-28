#version 13US1 (13A4 Merge)
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
        avgcalc = avg_calc()
        if(abs(polft - avgcalc) > 12):
             print(f"polft : {polft}, avgcalc : {avgcalc}")
             print("警告：結果不一致")
        else:
             print(f"polft : {polft}, avgcalc : {avgcalc}")
             print("通知：結果一致")
        cv2.destroyAllWindows()
        return True
    else:
        cv2.destroyAllWindows()
        return False
    

def avg_calc():
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
        result = peaks * 6
        open("result.txt", 'w', encoding="utf-8").write(str(result))
        #peak2, _ = find_peaks(np.array(result), distance=(8.5*(datacount/200)), height=np.array(avg2))
        
        plt.plot(np.array(result), label = "Orig. Data")
        plt.plot(peak, np.array(avg)[peak], "o")
        #plt.plot(peak2, np.array(result)[peak2], "o")
        plt.plot(np.array(avg), label = "[avg] 5 steps")
        plt.plot(np.array(avg2), label = "[avg] height (20 steps)")
        #plt.plot(np.array(avg2), label = "3 steps")
        plt.legend()
        plt.show()
        return result

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
    
    #plt.plot(np.array(result))
    plt.xlabel('frames')
    plt.ylabel('Brightness')
    plt.plot(np.array(result), label = "Orig. Data")
    plt.plot(peak, np.array(result)[peak], 'x', label = "[polft] peak")
    plt.plot(x, pfix - 0.02, '-', label = "[polft] height")
    plt.show()
    
    finalResult = (len(peak)*6)
    print(finalResult)
    open('result.txt', 'w', encoding='utf-8').write(str(finalResult))
    return finalResult

#start(False, 0 , 0)