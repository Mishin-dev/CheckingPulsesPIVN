import pandas as pd
from Cython.Compiler.MemoryView import memview_any_contiguous
from Cython.Shadow import sizeof
# from Cython.Shadow import sizeof
# from jeepney.io.blocking import timeout_to_deadline
from matplotlib import pyplot as plt
import numpy as np
from numpy.ma.extras import unique, average
from pandas.core.algorithms import nunique_ints
# from pytz import unicode

# df = pd.read_csv('data/03-06-2024 11-41-40.csv', delimiter=';')
# df = pd.read_csv('data/09-10-2024 15-06-33.csv', delimiter=';')
df = pd.read_csv('data/09-10-2024 15-19-18.csv', delimiter=';')
# df = pd.read_csv('data/09-10-2024 15-57-05.csv', delimiter=';')
# df = pd.read_csv('data/27-05-2024 16-38-07.csv', delimiter=';')

# print(len(df))
# print(df)

# plt.plot(df['t'], df['sum'])
# plt.step(df['t'], df['sum'], where='post')
# plt.show()

print("Number of changed trigger values: ", nunique_ints(df['tr']) - 1)

# Second way to define a pulse
# Критерий, при котором наличие импульса будет определяться по разнице между счетом в данную секунду и средним,
# превышающей 3 СКО выборки за предыдущие 14 секунд.

# Preparations
triggerValue = 0
prevTriggerValue = 0
isPulse = False # Probably will be useless
pulsesCounter = 0
pulsesTimings = []

timingArray = df['t']
countsArray = df['sum']
triggerArray = df['tr']
# triggerArray = np.zeros(len(df), dtype=int) # For testing
factor = 3 # Множитель для критерия 3-сигма

# Start
for i in timingArray[13:-1]:
    if triggerArray[i] > triggerArray[i - 1]:
        continue
        # isPulse = True
        # pulsesCounter += 1
    else:
        meanValueFor14sec = np.mean(countsArray[i - 13:i])
        stdValueFor14sec = np.std(countsArray[i - 13:i])
        if countsArray[i] > (meanValueFor14sec + factor * stdValueFor14sec):
            # isPulse = True
            pulsesCounter += 1
            pulsesTimings.append(i)
    # print(i)
# print(len(timingArray))
print("Number of counted pulses: ", pulsesCounter)
print("Pulses timings: ", pulsesTimings)

plt.step(df['t'], df['sum'], where='post')
plt.show()

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














