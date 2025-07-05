import os
import pandas as pd
from sklearn.model_selection import train_test_split

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

df = pd.read_csv(f'{DATA_PREFIX}/wine_preprocessed.csv')

X = df.drop('quality', axis=1)
y = df['quality']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train.to_csv(f'{DATA_PREFIX}/wine_X_train.csv', index=False)
X_test.to_csv(f'{DATA_PREFIX}/wine_X_test.csv', index=False)
y_train.to_csv(f'{DATA_PREFIX}/wine_y_train.csv', index=False)
y_test.to_csv(f'{DATA_PREFIX}/wine_y_test.csv', index=False)
print("Wine feature engineering done.")