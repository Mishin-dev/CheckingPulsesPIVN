from operator import index

import pandas as pd
from dulwich.index import read_index_dict
# from Cython.Compiler.MemoryView import memview_any_contiguous
# from Cython.Shadow import sizeof
# from Cython.Shadow import sizeof
# from jeepney.io.blocking import timeout_to_deadline
from matplotlib import pyplot as plt
import numpy as np
# from numpy.matlib import zeros
# from pandas import merge
# from numpy.ma.extras import unique, average
from pandas.core.algorithms import nunique_ints
# from pytz import unicode


path1 = 'data/03-06-2024 11-41-40.csv'
path2 = 'data/09-10-2024 15-06-33.csv'
path3 = 'data/09-10-2024 15-19-18.csv'
path4 = 'data/09-10-2024 15-57-05.csv'
path5 = 'data/27-05-2024 16-38-07.csv'

paths = [path1, path2, path3, path4, path5]
imageVariable = []

# df1 = pd.read_csv('data/03-06-2024 11-41-40.csv', delimiter=';')
# df2 = pd.read_csv('data/09-10-2024 15-06-33.csv', delimiter=';')
# df3 = pd.read_csv('data/09-10-2024 15-19-18.csv', delimiter=';')
# df4 = pd.read_csv('data/09-10-2024 15-57-05.csv', delimiter=';')
# df5 = pd.read_csv('data/27-05-2024 16-38-07.csv', delimiter=';')
# df1['number'] = np.ones(len(df1))
# df2['number'] = 2 * np.ones(len(df2))
# df3['number'] = 3 * np.ones(len(df3))
# df4['number'] = 4 * np.ones(len(df4))
# df5['number'] = 5 * np.ones(len(df5))

# df = pd.concat([df1, df2, df3, df4, df5], keys=['df1', 'df2', 'df3', 'df4', 'df5'], ignore_index=False, names =['Series name'])

# print(df.columns)
# print(len(df))
# print(df)

# plt.plot(df['t'], df['sum'])
# plt.step(df['t'], df['sum'], where='post')
# plt.show()

# print("Number of changes trigger values: ", '\n', nunique_ints(df['tr']) - 1)

# Second way to define a pulse
# Критерий, при котором наличие импульса будет определяться по разнице между счетом в данную секунду и средним,
# превышающей 3 СКО выборки за 14 секунд до первого превышения импульса.
# Конец импульса будет определяться как 30 секунд после начала импульса.

# # Preparations
# triggerValue = 0
# prevTriggerValue = 0
# isPulse = False
# pulsesCounter = 0
# pulsesTimings = []
#
# timingArray = df['t']
# countsArray = df['sum']
# triggerArray = df['tr']
# # triggerArray = np.zeros(len(df), dtype=int) # For testing
# triggerArrayChanges = []
# factor = 3 # Множитель для критерия 3-сигма
#
# meanValueFor14sec = 0
# stdValueFor14sec = 0

# fig = [1, 2, 3, 4, 5]
# ax = [1, 2, 3, 4, 5]

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
    triggerArray = df['tr']
    # triggerArray = np.zeros(len(df), dtype=int) # For testing
    triggerArrayChanges = []
    factor = 3  # Множитель для критерия 3-сигма

    meanValueFor14sec = 0
    stdValueFor14sec = 0

    for i in timingArray[13:-2]:
        # if triggerArray[i] > triggerArray[i - 1]:
        #     # continue
        #     triggerArrayChanges.append(i)
        #     # isPulse = True
        #     # pulsesCounter += 1
        # else:
        #     print(i, isPulse)
        #     print(i, meanValueFor14sec, stdValueFor14sec, countsArray[i], isPulse)
            if triggerArray[i] > triggerArray[i - 1]:
                # continue
                triggerArrayChanges.append(i)
                # isPulse = True
                # pulsesCounter += 1
            meanValueFor14sec = np.mean(countsArray[i - 13:i+1])
            stdValueFor14sec = np.std(countsArray[i - 13:i+1])
            # print(i, countsArray[i - 13:i])
            if (not isPulse) and (countsArray[i] > (meanValueFor14sec + factor * stdValueFor14sec)):
                # print(i, isPulse)
                isPulse = True
                # print(i, isPulse)
                pulsesCounter += 1
                pulsesTimings.append(i)
            if pulsesTimings != [] and i - pulsesTimings[-1] == 30:
                isPulse = False
                # print(i, isPulse)
            # print(i, meanValueFor14sec, stdValueFor14sec, countsArray[i], isPulse)
    # print('_______________________Файл_', read_index_dict(path), '_______________________')
    print('________________________________________________________________________________________________________')
    print("Number of changes trigger values: ", '\n', nunique_ints(df['tr']) - 1)
    print("Number of counted pulses: ", '\n', pulsesCounter)
    print("Pulses timings: ", '\n', pulsesTimings)
    print("Trigger array changes:", '\n', triggerArrayChanges)

    timeStampsList1 = [e for e in pulsesTimings if e not in triggerArrayChanges]
    timeStampsList2 = [e for e in triggerArrayChanges if e not in pulsesTimings]
    timeStampsList = timeStampsList1 + timeStampsList2
    timeStampsList = sorted(timeStampsList)
    print("Timestamps of missed counts or triggers: ", '\n', timeStampsList)

    # fig = plt.figure()

    # fig[index(path)], ax[index(path)] = plt.step(df['t'], df['sum'], where='post')

    plt.figure()
    plt.step(df['t'], df['sum'], where='post')
    plt.grid(visible=True, which='major', color='g', linestyle='-')
    plt.grid(visible=True, which='minor', color='g', linestyle='--')
    plt.yscale('log')
    plt.minorticks_on()
    # plt.show()
    # plt.draw()
    # continue
plt.show()

# print(len(timingArray))
# print("Number of changes trigger values: ", '\n', nunique_ints(df['tr']) - 1)
# print("Number of counted pulses: ", '\n', pulsesCounter)
# print("Pulses timings: ", '\n', pulsesTimings)
# print("Trigger array changes:", '\n', triggerArrayChanges)

# timeStampsArray = np.array(pulsesTimings)[np.array(pulsesTimings) != np.array(triggerArrayChanges)]
# timeStampsList = timeStampsArray.tolist()
# timeStampsList = list(filter(lambda x: x[0] != x[1], zip(pulsesTimings, triggerArrayChanges)))

# # Third way to define a pulse
# # критерий, при котором наличие импульса будет определяться по среднему, превышающему среднее + 3 СКО.
#
# # Preparations
# triggerValue = 0
# prevTriggerValue = 0
# isPulse = False # Probably will be useless
# pulsesCounter = 0
# pulsesTimings = []
#
# timingArray = df['t']
# countsArray = df['sum']
# triggerArray = df['tr']
# # triggerArray = np.zeros(len(df), dtype=int) # For testing
# factor = 2 # Множитель для критерия 3-сигма
#
# # Start
# for i in timingArray[13:-1]:
#     if triggerArray[i] > triggerArray[i - 1]:
#         continue
#         # isPulse = True
#         # pulsesCounter += 1
#     else:
#         meanValueFor14sec = np.mean(countsArray[i - 13:i])
#         stdValueFor14sec = np.std(countsArray[i - 13:i])
#         if countsArray[i] > (meanValueFor14sec + factor * stdValueFor14sec):
#             # isPulse = True
#             pulsesCounter += 1
#             pulsesTimings.append(i)
#     # print(i)
# # print(len(timingArray))
# print("Number of counted pulses: ", pulsesCounter)
# print("Pulses timings: ", pulsesTimings)
#
# plt.step(df['t'], df['sum'], where='post')
# plt.show()














