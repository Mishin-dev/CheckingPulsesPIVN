import pandas as pd
import Cython.Shadow
from matplotlib import pyplot as plt
import numpy as np
from pandas import Index
from pandas.core.algorithms import nunique_ints


path1 = 'data/03-06-2024 11-41-40.csv'
path2 = 'data/09-10-2024 15-06-33.csv'
path3 = 'data/09-10-2024 15-19-18.csv'
path4 = 'data/09-10-2024 15-57-05.csv'
path5 = 'data/27-05-2024 16-38-07.csv'

paths = [path1, path2, path3, path4, path5]
# paths = [path3]

# print(df.columns)
# print(len(df))
# print(df)

# plt.plot(df['t'], df['sum'])
# plt.step(df['t'], df['sum'], where='post')
# plt.show()

# First way to define a pulse___________________________________________________________________________________________

# Отслеживать изменение усредненного числа импульсов за N секунд. Суть заключается в том, что наличие нейтронного
# импульса приводит к резкому изменению (насколько резкому?) усредненного числа зарегистрированных импульсов.
# Недостаток заключается в том, что требуется задавать точное значение порога изменения, что может не определять
# нейтронный импульс в случае малых выходов нейтронов.

# Second way to define a pulse__________________________________________________________________________________________

# Критерий, при котором наличие импульса будет определяться по разнице между счетом в данную секунду и средним,
# превышающей 3 СКО выборки за 14 секунд до первого превышения импульса.
# Конец импульса будет определяться как 30 секунд после начала импульса.

# # Start
# path: str
# for path in paths:
#     df = pd.read_csv(path, delimiter=';')
#     # Preparations
#     triggerValue = 0
#     prevTriggerValue = 0
#     isPulse = False
#     pulsesCounter = 0
#     pulsesTimings = []
#
#     timingArray = df['t']
#     countsArray = df['sum']
#     triggerArray = df['tr']
#     # triggerArray = np.zeros(len(df), dtype=int) # For testing
#     triggerArrayChanges = []
#     factor = 3  # Множитель для критерия 3-сигма
#
#     meanValueFor14sec = 0
#     stdValueFor14sec = 0
#
#     for i in timingArray[13:-2]:
#         # if triggerArray[i] > triggerArray[i - 1]:
#         #     triggerArrayChanges.append(i)
#         #     # isPulse = True
#         #     # pulsesCounter += 1
#         # else:
#         #     print(i, isPulse)
#         #     print(i, meanValueFor14sec, stdValueFor14sec, countsArray[i], isPulse)
#             if triggerArray[i] > triggerArray[i - 1]:
#                 triggerArrayChanges.append(i)
#                 # isPulse = True
#                 # pulsesCounter += 1
#             meanValueFor14sec = np.mean(countsArray[i - 13:i+1])
#             stdValueFor14sec = np.std(countsArray[i - 13:i+1])
#             # print(i, countsArray[i - 13:i])
#             if (not isPulse) and (countsArray[i] > (meanValueFor14sec + factor * stdValueFor14sec)):
#                 # print(i, isPulse)
#                 isPulse = True
#                 # print(i, isPulse)
#                 pulsesCounter += 1
#                 pulsesTimings.append(i)
#             if pulsesTimings != [] and i - pulsesTimings[-1] == 30:
#                 isPulse = False
#                 # print(i, isPulse)
#             # print(i, meanValueFor14sec, stdValueFor14sec, countsArray[i], isPulse)
#     print('______________________________________ Файл', paths.index(path) + 1, '______________________________________')
#     # print('________________________________________________________________________________________________________')
#     print("Number of changes trigger values: ", '\n', nunique_ints(df['tr']) - 1)
#     print("Number of counted pulses: ", '\n', pulsesCounter)
#     print("Pulses timings: ", '\n', pulsesTimings)
#     print("Trigger array changes:", '\n', triggerArrayChanges)
#
#     timeStampsList1 = [e for e in pulsesTimings if e not in triggerArrayChanges]
#     timeStampsList2 = [e for e in triggerArrayChanges if e not in pulsesTimings]
#     timeStampsList = timeStampsList1 + timeStampsList2
#     timeStampsList = sorted(timeStampsList)
#     print("Timestamps of missed counts or triggers: ", '\n', timeStampsList)
#
#     plt.figure()
#     plt.step(df['t'], df['sum'], where='post')
#     plt.grid(visible=True, which='major', color='g', linestyle='-')
#     plt.grid(visible=True, which='minor', color='g', linestyle='--')
#     plt.yscale('log')
#     plt.minorticks_on()
# plt.show()

# Third way to define a pulse___________________________________________________________________________________________

# Вместо критерия второго варианта можно взять критерий, при котором наличие импульса будет определяться по среднему,
# превышающему среднее + 3 СКО. Момент начала импульса определяется как наибольшее число отсчетов за интервал усреднения

# З. Ы. Скорее всего работать не будет, но реализацию пропишу, это не долго
# upd: Действительно не работает.

# Start
path: str
for path in paths:
    df = pd.read_csv(path, delimiter=';')
    # Preparations
    triggerValue = 0
    prevTriggerValue = 0
    isPulse = False
    pulsesCounter = 0
    pulsesTimings = []

    timingArray = df['t']
    countsArray = df['sum']
    # print(typeof(countsArray)) # Series
    triggerArray = df['tr']
    # triggerArray = np.zeros(len(df), dtype=int) # For testing
    triggerArrayChanges = []
    factor = 0.0  # Множитель для критерия 3-сигма

    meanValueFor14sec = 0
    stdValueFor14sec = 0
    pulseTiming = 0

    for i in timingArray[29:-2]:
        # if triggerArray[i] > triggerArray[i - 1]:
        #     triggerArrayChanges.append(i)
        #     # isPulse = True
        #     # pulsesCounter += 1
        # else:
        #     print(i, isPulse)
        #     print(i, meanValueFor14sec, stdValueFor14sec, countsArray[i], isPulse)
            if triggerArray[i] > triggerArray[i - 1]:
                triggerArrayChanges.append(i)
                # isPulse = True
                # pulsesCounter += 1
            meanValueFor14secBefore14sec = np.mean(countsArray[i - 29:i-14])
            stdValueFor14secBefore14sec = np.std(countsArray[i - 29:i-14])
            meanValueFor14sec = np.mean(countsArray[i - 13:i+1])
            stdValueFor14sec = np.std(countsArray[i - 13:i+1])
            # print(i, countsArray[i - 13:i])
            if (not isPulse) and (meanValueFor14sec > (meanValueFor14secBefore14sec + factor * stdValueFor14secBefore14sec)):
                # print(i, isPulse)
                isPulse = True
                # print(i, isPulse)
                pulsesCounter += 1
                pulseStartValue = max(countsArray[i - 13:i + 1])
                # pulseTiming = Index(countsArray).get_loc(pulseStartValue)
                pulseTiming = i
                pulsesTimings.append(pulseTiming)
                print(type(pulseTiming))
                print(pulseTiming)
                # print(len(pulseTiming))
            if (i - pulseTiming == 30) and pulseTiming:
                isPulse = False
                # print(i, isPulse)
            # print(i, meanValueFor14sec, stdValueFor14sec, countsArray[i], isPulse)
    print('______________________________________ Файл', paths.index(path) + 1, '______________________________________')
    # print('________________________________________________________________________________________________________')
    print("Number of changes trigger values: ", '\n', nunique_ints(df['tr']) - 1)
    print("Number of counted pulses: ", '\n', pulsesCounter)
    print("Pulses timings: ", '\n', pulsesTimings)
    print("Trigger array changes:", '\n', triggerArrayChanges)

    timeStampsList1 = [e for e in pulsesTimings if e not in triggerArrayChanges]
    timeStampsList2 = [e for e in triggerArrayChanges if e not in pulsesTimings]
    timeStampsList = timeStampsList1 + timeStampsList2
    timeStampsList = sorted(timeStampsList)
    print("Timestamps of missed counts or triggers: ", '\n', timeStampsList)

    plt.figure()
    plt.step(df['t'], df['sum'], where='post')
    plt.grid(visible=True, which='major', color='g', linestyle='-')
    plt.grid(visible=True, which='minor', color='g', linestyle='--')
    plt.yscale('log')
    plt.minorticks_on()
# plt.show()


# ______________________________________________________________________________________________________________________

# Forth way to define a pulse
# Определять наличие нейтронного импульса по производной (по двум/трем/более точкам). Возникновение импульса приводит
# к скачку на временной гистограмме счета импульсов. Может плохо работать в области низких выходов, однако позволяет
# успешно разделять близкие по времени последовательные импульсы заметных амплитуд.