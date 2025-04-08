import pandas as pd
import scipy.optimize.elementwise
# import Cython.Shadow
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.pyplot import xlabel
# from pandas import Index
from pandas.core.algorithms import nunique_ints
from scipy import optimize
from scipy.optimize import least_squares
from sympy.codegen.cnodes import sizeof

from sympy.solvers import solve
from sympy import var, Eq


# def find_nearest(array, value):
#     array = np.asarray(array)
#     idx = (np.abs(array - value)).argmin()
#     return array[idx]

def find_nearest_index(array, value, ref_idx):
    idx_arr = []
    array = np.asarray(array)
    for idxElement in range(0, len(array) - 1):
        if np.abs(array[idxElement] - value) == 0:
            idx_arr.append(idxElement)
    idx_arr = np.asarray(idx_arr)
    idx = (np.abs(idx_arr - ref_idx)).argmin()
    return idx

path1 = 'data/03-06-2024 11-41-40.csv'
path2 = 'data/09-10-2024 15-06-33.csv'
path3 = 'data/09-10-2024 15-19-18.csv'
path4 = 'data/09-10-2024 15-57-05.csv'
path5 = 'data/27-05-2024 16-38-07.csv'
path6 = 'data/12-03-2025 sensitive channel.csv'
path7 = 'data/12-03-2025 rough channel.csv'

# paths = [path1, path2, path3, path4, path5, path6, path7]
paths = [path7]

# print(df.columns)
# print(len(df))
# print(df)

# plt.plot(df['t'], df['sum'])
# plt.step(df['t'], df['sum'], where='post')
# plt.show()

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

    countsArrayOfPulse = [] # Измеренная скорость счета
    deadTime = 100 # Первое приближение
    realCountRate = np.ones(30) # Истинная скорость счета

    factor = 3.0  # Множитель для критерия 3-сигма (по умолчанию должен быть равен 3.0)

    meanValueFor14sec = 0
    stdValueFor14sec = 0
    pulseTiming = 0

    # First way to define a pulse___________________________________________________________________________________________
    # Отслеживать изменение усредненного числа импульсов за N секунд. Суть заключается в том, что наличие нейтронного
    # импульса приводит к резкому изменению (насколько резкому?) усредненного числа зарегистрированных импульсов.
    # Недостаток заключается в том, что требуется задавать точное значение порога изменения, что может не определять
    # нейтронный импульс в случае малых выходов нейтронов.

    # Здесь пока ничего

    # __________________________________________________________________________________________________________________
    print('\n')

    # Second way to define a pulse______________________________________________________________________________________
    # Критерий, при котором наличие импульса будет определяться по разнице между счетом в данную секунду и средним,
    # превышающей 3 СКО выборки за 14 секунд до первого превышения импульса.
    # Конец импульса будет определяться как 30 секунд после начала импульса.

    for i in timingArray[13:-2]:
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
        meanValueFor14sec = np.mean(countsArray[i - 13:i+1])
        stdValueFor14sec = np.std(countsArray[i - 13:i+1])
        # print(i, countsArray[i - 13:i])
        if (not isPulse) and (countsArray[i] > (meanValueFor14sec + factor * stdValueFor14sec)):
            # print(i, isPulse)
            isPulse = True
            # print(i, isPulse)
            pulsesCounter += 1
            pulsesTimings.append(i)
            # countsArrayOfPulse = []
        if isPulse: # Внимание на это условие
            countsArrayOfPulse.append(countsArray[i])
            # print(countsArray[i])
            # print(countsArrayOfPulse)
        if pulsesTimings != [] and i - pulsesTimings[-1] == 30:
            isPulse = False
            # Вариант 1 поиска значения мертвого времени _______________________________________________________________
            def equations(vars, m):
                n = vars[:-1]
                t = vars[-1]
                return n * np.exp(-n * t) - m

            m = countsArrayOfPulse
            # print(m)
            t_initial = 1 / (np.e * np.max(m))
            n_initial = m.copy()
            initial_guess = np.append(n_initial, t_initial)

            result = least_squares(equations, initial_guess, args=(m,), bounds=(0, np.inf))

            n_solution = result.x[:-1]
            t_solution = result.x[-1]

            deadTime = t_solution
            realCountRate = n_solution

            # print("Solution:")
            # print("n =", n_solution)
            # print("t =", t_solution * 10 ** 6)
            print(t_solution * 10 ** 6)
            # print("Residuals:", np.sum(result.fun ** 2))

            # countsArrayOfPulse = []
            # print(i, isPulse)

            # Вариант 2 поиска мертвого времени ________________________________________________________________________
            # def equations(vars, m):
            #     t = vars[-1]
            #     # denominator = 1 - m * t
            #     denominator = 1 - np.multiply(m, t)
            #     denominator = np.where(np.abs(denominator) < 1e-12, 1e-12, denominator)
            #     predicted_n = m / denominator
            #     return predicted_n - vars[:-1]
            #
            # m = countsArrayOfPulse
            # m = m / sum(m)
            #
            # t_initial = 0.1
            # n_initial = m.copy()
            # n_initial = []
            # # test = []
            # for k in range(1, 32):
            #     n_initial.append(np.log(2) / 14.2 * np.exp(-np.log(2) / 14.2 * k))
            #
            #     # test.append(k)
            # # print(test)
            # # print(m) # Содержит 32 элемента
            #
            # initial_guess = np.append(n_initial, t_initial)
            #
            # result = least_squares(equations, initial_guess, args=(m,), bounds=(0, np.inf))
            #
            # # Extract solution
            # n_solution = result.x[:-1]
            # t_solution = result.x[-1]
            #
            # # print("Solution:")
            # print(f"t = {t_solution:.6f}")
            # # print("n =", n_solution)
            # # print(f"Residual norm: {np.linalg.norm(result.fun):.2e}")

            plt.figure()

            # plt.plot(realCountRate)
            # plt.plot(countsArrayOfPulse)
            # plt.plot(m)
            # plt.plot(n_solution)
            plt.step(range(1, 32), m, where='post')
            plt.step(range(1, 32), n_solution, where='post')
            plt.xlabel('Время, с')
            plt.ylabel('Число импульсов, ед.')
            plt.legend(['Измеренная скорость счета', 'Прогнозируемая истинная скорость счета'])
            # text
            # plt.text('Мертвое время: ', t_solution)
            plt.grid(visible=True, which='major', color='g', linestyle='-')
            plt.grid(visible=True, which='minor', color='g', linestyle='--')
            plt.yscale('log')
            # plt.show()
            countsArrayOfPulse = []

        # print(i, meanValueFor14sec, stdValueFor14sec, countsArray[i], isPulse)

        # ______________________________________________________________________________________________________________
    print('\n')
    # Third way to define a pulse_______________________________________________________________________________________
    # Вместо критерия второго варианта можно взять критерий, при котором наличие импульса будет определяться по
    # среднему, превышающему среднее + 3 СКО. Момент начала импульса определяется как наибольшее число отсчетов за
    # интервал усреднения
    # З. Ы. Скорее всего работать не будет, но реализацию пропишу, это не долго
    # upd: Действительно не работает.

    # for i in timingArray[29:-2]:
    #     # if triggerArray[i] > triggerArray[i - 1]:
    #     #     triggerArrayChanges.append(i)
    #     #     # isPulse = True
    #     #     # pulsesCounter += 1
    #     # else:
    #     #     print(i, isPulse)
    #     #     print(i, meanValueFor14sec, stdValueFor14sec, countsArray[i], isPulse)
    #         if triggerArray[i] > triggerArray[i - 1]:
    #             triggerArrayChanges.append(i)
    #             # isPulse = True
    #             # pulsesCounter += 1
    #         meanValueFor14secBefore14sec = np.mean(countsArray[i - 30:i-15])
    #         stdValueFor14secBefore14sec = np.std(countsArray[i - 30:i-15])
    #         meanValueFor14sec = np.mean(countsArray[i - 14:i])
    #         stdValueFor14sec = np.std(countsArray[i - 14:i])
    #         # print(i, countsArray[i - 13:i])
    #         if (not isPulse) and (meanValueFor14sec > (meanValueFor14secBefore14sec + factor * stdValueFor14secBefore14sec)):
    #             # print(i, isPulse)
    #             isPulse = True
    #             # print(i, isPulse)
    #             pulsesCounter += 1
    #             pulseStartValue = max(countsArray[i - 30:i])
    #             # pulseTiming = Index(countsArray).get_loc(pulseStartValue) # Это bool массив
    #             pulseTiming = list(countsArray[i - 30:i]).index(pulseStartValue)
    #             # print(type(pulseTiming))
    #             # print(i, pulseTiming)
    #             # equalIndexesArrayForPulseStartValue = find_nearestIndex(countsArray, pulseStartValue)
    #             # print(equalIndexesArrayForPulseStartValue)
    #             # pulseTiming = find_nearestIndex(equalIndexesArrayForPulseStartValue, pulseStartValue, i-13)
    #             # pulseTiming = find_nearest_index(countsArray, pulseStartValue, i-13)
    #             # print(pulseTiming)
    #             # pulseTiming = i
    #             pulsesTimings.append(pulseTiming)
    #             # print(type(pulseTiming))
    #             # print(i, pulseTiming)
    #             # print(len(pulseTiming))
    #         if isPulse:
    #             if i - pulseTiming == 30:
    #                 isPulse = False
    #                 # print(i, isPulse)
    #         # print(i, meanValueFor14sec, stdValueFor14sec, countsArray[i], isPulse)
    # # __________________________________________________________________________________________________________________
    print('\n')

    # Forth way to define a pulse ______________________________________________________________________________________
    # Определять наличие нейтронного импульса по производной (по двум/трем/более точкам). Возникновение импульса приводит
    # к скачку на временной гистограмме счета импульсов. Может плохо работать в области низких выходов, однако позволяет
    # успешно разделять близкие по времени последовательные импульсы заметных амплитуд.

    # Здесь пока ничего

    # __________________________________________________________________________________________________________________
    print('\n')

    print('______________________________________ Файл', paths.index(path) + 1, '_____________________________________')
    # print('________________________________________________________________________________________________________')
    print("Number of changes trigger values: ", '\n', nunique_ints(df['tr']) - 1)
    print("Number of counted pulses: ", '\n', pulsesCounter)
    print('\n', "Pulses timings: ", '\n', pulsesTimings)
    print("Trigger array changes:", '\n', triggerArrayChanges)

    timeStampsList1 = [e for e in pulsesTimings if e not in triggerArrayChanges]
    timeStampsList2 = [e for e in triggerArrayChanges if e not in pulsesTimings]
    timeStampsList = timeStampsList1 + timeStampsList2
    timeStampsList = sorted(timeStampsList)
    print('\n', "Timestamps of missed counts or triggers: ", '\n', timeStampsList, '\n')

    plt.figure()
    plt.step(df['t'], df['sum'], where='post')
    plt.xlabel('Время, с')
    plt.ylabel('Число импульсов, ед.')
    plt.grid(visible=True, which='major', color='g', linestyle='-')
    plt.grid(visible=True, which='minor', color='g', linestyle='--')
    plt.yscale('log')
    plt.minorticks_on()
plt.show()