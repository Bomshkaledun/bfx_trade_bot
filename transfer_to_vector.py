import pandas as pd
import sklearn

massive_to_vector = pd.read_csv('DataFrame\massive_h1.csv', sep = '\t')
value = massive_to_vector['MTS', 'HIGHT', 'LOW']
print (value)