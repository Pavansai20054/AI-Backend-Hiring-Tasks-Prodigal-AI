import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, size
from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.ml import Pipeline
from pyspark.ml.functions import vector_to_array

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

spark = SparkSession.builder.appName("TitanicFeatureEngineering").getOrCreate()

df = spark.read.csv(f'{DATA_PREFIX}/titanic_preprocessed.csv', header=True, inferSchema=True)

# Encode 'Sex', 'Embarked', 'Pclass' as numeric
indexer_sex = StringIndexer(inputCol="Sex", outputCol="SexIndex")
indexer_embarked = StringIndexer(inputCol="Embarked", outputCol="EmbarkedIndex")
indexer_pclass = StringIndexer(inputCol="Pclass", outputCol="PclassIndex")

# One-hot encode categorical columns
encoder = OneHotEncoder(inputCols=["EmbarkedIndex", "PclassIndex"], outputCols=["EmbarkedVec", "PclassVec"])

pipeline = Pipeline(stages=[indexer_sex, indexer_embarked, indexer_pclass, encoder])
model = pipeline.fit(df)
df = model.transform(df)

# Convert vectors to arrays then to columns
df = df.withColumn("EmbarkedVecArr", vector_to_array("EmbarkedVec"))
df = df.withColumn("PclassVecArr", vector_to_array("PclassVec"))

# Dynamically determine the number of categories
# OneHotEncoder output array size = numCategories - 1, unless dropLast=False is set (default is True)
# So we determine length by inspecting the size of the array in a row
embarked_vec_len = df.select(size(col("EmbarkedVecArr"))).first()[0]
pclass_vec_len = df.select(size(col("PclassVecArr"))).first()[0]

for i in range(embarked_vec_len):
    df = df.withColumn(f"EmbarkedVec_{i}", col("EmbarkedVecArr")[i])
for i in range(pclass_vec_len):
    df = df.withColumn(f"PclassVec_{i}", col("PclassVecArr")[i])

# Select features for ML (drop string columns and unused features)
feature_cols = [
    "SexIndex", "Age", "SibSp", "Parch", "Fare"
] + [f"EmbarkedVec_{i}" for i in range(embarked_vec_len)] \
  + [f"PclassVec_{i}" for i in range(pclass_vec_len)]

X = df.select(*feature_cols)
y = df.select(col("Survived").cast("double").alias("Survived"))

# Train/test split (using randomSplit)
X_train, X_test = X.randomSplit([0.8, 0.2], seed=42)
y_train, y_test = y.randomSplit([0.8, 0.2], seed=42)

# Save features and targets as CSV
X_train.coalesce(1).write.csv(f'{DATA_PREFIX}/titanic_X_train.csv', header=True, mode="overwrite")
X_test.coalesce(1).write.csv(f'{DATA_PREFIX}/titanic_X_test.csv', header=True, mode="overwrite")
y_train.coalesce(1).write.csv(f'{DATA_PREFIX}/titanic_y_train.csv', header=True, mode="overwrite")
y_test.coalesce(1).write.csv(f'{DATA_PREFIX}/titanic_y_test.csv', header=True, mode="overwrite")
print("Titanic feature engineering done (with Spark).")

spark.stop()