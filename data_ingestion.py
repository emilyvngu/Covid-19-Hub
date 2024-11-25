from pyspark.sql import SparkSession
from session import create_session_hive
from config.config import Config
from pyspark.sql.functions import col, lit, to_date, monotonically_increasing_id
from pyspark.sql.types import IntegerType, FloatType

# Initialize SparkSession with Hive Support
spark = create_session_hive()
spark.sql("show tables")
# Load CSV Files into a DataFrame
covid_raw_df = spark.read.csv(Config.HADOOP_FILE_PATH, header=True, inferSchema=True)

# Process Country Data
country_df = covid_raw_df.select(
    col("Country_Region").alias("Name"),
    col("Lat").alias("latitude").cast(FloatType()),
    col("Long_").alias("longitude").cast(FloatType())
).distinct()

# Add Unique IDs to Countries
country_df = country_df.withColumn("id", monotonically_increasing_id().cast(IntegerType()))

# Create Country Table in Hive
spark.sql("""
    CREATE TABLE IF NOT EXISTS Country (
        id INT,
        Name STRING,
        latitude FLOAT,
        longitude FLOAT
    )
""")

# Populate Country Table
country_df.write.mode("overwrite").insertInto("Country")

# Create a Broadcast Variable for Country Mapping
country_mapping = {row["Name"]: row["id"] for row in country_df.collect()}
broadcast_country_map = spark.sparkContext.broadcast(country_mapping)

# Process CovidData
covid_data_df = covid_raw_df.select(
    lit(None).cast(IntegerType()).alias("country_id"),  # Placeholder for country_id
    to_date(col("Last_Update"), "yyyy-MM-dd HH:mm:ss").alias("date"),
    col("Case_Fatality_Ratio").cast(FloatType()),
    col("Confirmed").cast(IntegerType()),
    col("Deaths").cast(IntegerType()),
    col("Recovered").cast(IntegerType()),
    col("Active").cast(IntegerType()),
    col("Incident_Rate").cast(FloatType()),
    col("Country_Region")
)

# Map Country Names to IDs
def map_country_id(country_name):
    return broadcast_country_map.value.get(country_name, None)

map_country_udf = spark.udf.register("map_country_id", map_country_id, IntegerType())
covid_data_df = covid_data_df.withColumn(
    "country_id", map_country_udf(col("Country_Region"))
).drop("Country_Region")

# Create CovidData Table in Hive
spark.sql("""
    CREATE TABLE IF NOT EXISTS database_name.CovidData (
        country_id INT,
        date DATE,
        Case_Fatality_Ratio FLOAT,
        Confirmed INT,
        Deaths INT,
        Recovered INT,
        Active INT,
        Incident_Rate FLOAT
    )
""")

# Populate CovidData Table
covid_data_df.write.mode("overwrite").insertInto("database_name.CovidData")

spark.stop()