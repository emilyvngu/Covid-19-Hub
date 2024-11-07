from pyspark.sql import SparkSession

def create_session():
    spark = SparkSession.builder.appName('Practice').getOrCreate()
    return spark
