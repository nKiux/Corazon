#version 13S3
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
        global figure
        global axis
        figure, axis = plt.subplots(2, 2) # rows, columns
        subseq = subseq_algo() # Result1
        avgcalc = avg_calc() # Result2
        polft = polft_algorithm() # Result3
        plt.show()

        # check the results
        # 3 types of situation: all the same (x, x, x), one difference (x, x, y), two difference (x, y, z) 
        print(f"subseq: {subseq}, polft: {polft}, avgcalc: {avgcalc}")

        res_set = list(set([subseq, polft, avgcalc]))
        distinct_values = len(set([subseq, polft, avgcalc]))
        if distinct_values == 1: # [x, x, x] >> {x}
            print("通知：結果一致")
            finalResult = subseq
            print(finalResult)
            open('result.txt', 'w', encoding='utf-8').write(str(finalResult))
        elif distinct_values == 2: # [x, x, y] >> {x, y}
            print("通知：結果一致")
            if subseq == polft:
                finalResult = subseq
                print(finalResult)
                open('result.txt', 'w', encoding='utf-8').write(str(finalResult))
            elif subseq == avgcalc:
                finalResult = avgcalc
                print(finalResult)
                open('result.txt', 'w', encoding='utf-8').write(str(finalResult))
            elif polft == avgcalc:
                finalResult = polft
                print(finalResult)
                open('result.txt', 'w', encoding='utf-8').write(str(finalResult))
        else: # [x, y, z] >> {x, y, z}
            if abs(res_set[0] - res_set[2]) <= 12 and abs(res_set[0] - res_set[1]) <= 12:
                finalResult = (subseq + avgcalc + polft) / 3
                print(finalResult)
                open('result.txt', 'w', encoding='utf-8').write(str(finalResult))
                print("通知：結果一致")
                
            else:
                finalResult = 0
                print(finalResult)
                open('result.txt', 'w', encoding='utf-8').write(str(finalResult))
                print("警告：結果不一致")


        
        # if(abs(polft - avgcalc) > 12): 
        #     print("警告：結果不一致")
        # else:
        #     print("通知：結果一致")
        
        cv2.destroyAllWindows()
        return True
    else:
        cv2.destroyAllWindows()
        return False
    

# ----------- algorithms ----------- #

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
    # data smoothness
    for i, x in enumerate(bright_values):
        if i==0 or i==len(bright_values)-1:
            continue
        else:
            bright_values[i] = np.average(bright_values[i-1:i+1])
    
    for i, x in enumerate(height_standard):
        if i==len(height_standard)-1: # last digit
            break
        else:
            height_standard[i] = np.average(height_standard[i:i+1]) # avg of current and next one
    
    peak_idx = find_peaks(bright_values, height=height_standard, distance=7)[0] # peak indexes
    
    # # hand-made peak finder BETA
    # peak_idx = []
    # for i, x in enumerate(bright_values):
    #     if i == 0 or i == len(bright_values)-1: # first & last
    #         continue
    #     else:
    #         if x > bright_values[i-1] and x > bright_values[i+1]: # peak == True
    #             if x >= height_standard[i] and i > peak_idx[len(peak_idx)-1]+7: # the peak we want
    #                 peak_idx.append(i) # write the peak

    axis[0, 0].plot(bright_values)
    axis[0, 0].plot(height_standard)
    axis[0, 0].plot(peak_idx, np.array(bright_values)[peak_idx], "o")
    axis[0, 0].set_title('Subsequence Algorithm')

    Result1 = (len(peak_idx)*6)
    return Result1


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
    Result2 = peaks * 6
    # open("result.txt", 'w', encoding="utf-8").write(str(Result2))
    #peak2, _ = find_peaks(np.array(result), distance=(8.5*(datacount/200)), height=np.array(avg2))
    
    axis[0, 1].set_title("Average Calculation")
    axis[0, 1].plot(np.array(result), label = "Orig. Data")
    axis[0, 1].plot(peak, np.array(avg)[peak], "o")
    #plt.plot(peak2, np.array(result)[peak2], "o")
    axis[0, 1].plot(np.array(avg), label = "[avg] 5 steps")
    axis[0, 1].plot(np.array(avg2), label = "[avg] height (20 steps)")
    #plt.plot(np.array(avg2), label = "3 steps")
    return Result2


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
    axis[1, 0].set_title("Ployfit Algorithms")
    # axis[1, 0].xlabel('frames')
    # axis[1, 0].ylabel('Brightness')
    axis[1, 0].plot(np.array(result), label = "Orig. Data")
    axis[1, 0].plot(peak, np.array(result)[peak], 'x', label = "[polft] peak")
    axis[1, 0].plot(x, pfix - 0.02, '-', label = "[polft] height")
    
    Result3 = (len(peak)*6)
    # print(Result3)
    # open('result.txt', 'w', encoding='utf-8').write(str(Result3))
    return Result3

#start(False, 0 , 0)