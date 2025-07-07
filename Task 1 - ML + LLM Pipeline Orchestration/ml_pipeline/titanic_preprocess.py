import os
from pyspark.sql import SparkSession

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

spark = SparkSession.builder.appName("TitanicPreprocess").getOrCreate()

# Read Titanic CSV as Spark DataFrame
df = spark.read.csv(f'{DATA_PREFIX}/titanic.csv', header=True, inferSchema=True)

# Fill missing Age with median
age_median = df.approxQuantile("Age", [0.5], 0.001)[0]
df = df.fillna({"Age": age_median})

# Fill missing Embarked with mode
embarked_mode = df.groupBy("Embarked").count().orderBy("count", ascending=False).first()["Embarked"]
df = df.fillna({"Embarked": embarked_mode})

# Save as preprocessed CSV
df.write.csv(f'{DATA_PREFIX}/titanic_preprocessed.csv', header=True, mode="overwrite")
print("Titanic preprocessing done (with Spark).")

spark.stop()