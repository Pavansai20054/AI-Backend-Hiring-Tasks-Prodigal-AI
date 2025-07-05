import os
import pandas as pd
from sklearn.model_selection import train_test_split

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

df = pd.read_csv(f'{DATA_PREFIX}/titanic_preprocessed.csv')

# Encode categorical variables
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
df = pd.get_dummies(df, columns=['Embarked', 'Pclass'])

# Split data
X = df.drop(['Survived', 'Name', 'Ticket', 'Cabin'], axis=1)
y = df['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train.to_csv(f'{DATA_PREFIX}/titanic_X_train.csv', index=False)
X_test.to_csv(f'{DATA_PREFIX}/titanic_X_test.csv', index=False)
y_train.to_csv(f'{DATA_PREFIX}/titanic_y_train.csv', index=False)
y_test.to_csv(f'{DATA_PREFIX}/titanic_y_test.csv', index=False)
print("Titanic feature engineering done.")