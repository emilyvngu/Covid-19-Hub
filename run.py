import pyspark
import pandas as pd
from session import create_session

spark = create_session()



df_pyspark = spark.read.csv('test1.csv',inferSchema=True,header=True)

# print(df_pyspark.show())
print(type(df_pyspark))
df_pyspark2 = df_pyspark.withColumn('Experience after 2 years', df_pyspark['Experience']+2)
print(df_pyspark2.show())
df_py3=df_pyspark.drop('Experience after 2 years')
print(df_py3.show())
# Data preprosession
# 1. pySpark dataframe
# 2.Reading the dataset
# 3. checking the data types of the columns
# 4. selecting columns and indexing
# 5. check describe option similar to pandas
# 6. Adding columns, dropping columns


