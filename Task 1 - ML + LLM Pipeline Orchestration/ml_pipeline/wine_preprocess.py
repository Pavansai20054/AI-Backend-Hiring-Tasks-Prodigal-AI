import os
from pyspark.sql import SparkSession

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

spark = SparkSession.builder.appName("WinePreprocess").getOrCreate()

# Read Wine Quality CSV as Spark DataFrame (semicolon separator)
df = spark.read.csv(f'{DATA_PREFIX}/winequality-red.csv', header=True, inferSchema=True, sep=';')

# (No missing value handling needed unless you want to add it)

# Save as preprocessed CSV
df.write.csv(f'{DATA_PREFIX}/wine_preprocessed.csv', header=True, mode="overwrite")
print("Wine preprocessing done (with Spark).")

spark.stop()