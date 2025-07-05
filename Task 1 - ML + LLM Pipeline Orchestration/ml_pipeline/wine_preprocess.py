import os
import pandas as pd

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

df = pd.read_csv(f'{DATA_PREFIX}/winequality-red.csv', sep=';')
df.to_csv(f'{DATA_PREFIX}/wine_preprocessed.csv', index=False)
print("Wine preprocessing done.")