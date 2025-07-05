import os
import pandas as pd

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

df = pd.read_csv(f'{DATA_PREFIX}/titanic.csv')
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
df.to_csv(f'{DATA_PREFIX}/titanic_preprocessed.csv', index=False)
print("Titanic preprocessing done.")