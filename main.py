import pandas as pd
from matplotlib import pyplot as plt
from numpy.ma.extras import unique
from pandas.core.algorithms import nunique_ints
from pytz import unicode

# df = pd.read_csv('data/03-06-2024 11-41-40.csv', delimiter=';')
# df = pd.read_csv('data/09-10-2024 15-06-33.csv', delimiter=';')
# df = pd.read_csv('data/09-10-2024 15-19-18.csv', delimiter=';')
# df = pd.read_csv('data/09-10-2024 15-57-05.csv', delimiter=';')
df = pd.read_csv('data/27-05-2024 16-38-07.csv', delimiter=';')
print(df)
plt.plot(df['t'], df['sum'])
# plt.show()

print(nunique_ints(df['tr']))
















