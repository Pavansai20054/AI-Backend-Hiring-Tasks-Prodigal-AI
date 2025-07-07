import os
from pyspark.sql import SparkSession

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

spark = SparkSession.builder.appName("WineFeatureEngineering").getOrCreate()

df = spark.read.csv(f'{DATA_PREFIX}/wine_preprocessed.csv', header=True, inferSchema=True)

# Split into features (X) and target (y)
X = df.drop('quality')
y = df.select('quality')

# Train/test split
X_train, X_test = X.randomSplit([0.8, 0.2], seed=42)
y_train, y_test = y.randomSplit([0.8, 0.2], seed=42)

# Save features and targets as CSV (single file per split)
X_train.coalesce(1).write.csv(f'{DATA_PREFIX}/wine_X_train.csv', header=True, mode="overwrite")
X_test.coalesce(1).write.csv(f'{DATA_PREFIX}/wine_X_test.csv', header=True, mode="overwrite")
y_train.coalesce(1).write.csv(f'{DATA_PREFIX}/wine_y_train.csv', header=True, mode="overwrite")
y_test.coalesce(1).write.csv(f'{DATA_PREFIX}/wine_y_test.csv', header=True, mode="overwrite")
print("Wine feature engineering done (with Spark).")

spark.stop()