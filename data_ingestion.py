from pyspark.sql import SparkSession
from session import create_session_hive
from config import Config
from pyspark.sql.functions import col, lit, to_date, monotonically_increasing_id, when
from pyspark.sql.types import IntegerType, FloatType

# Initialize SparkSession with Hive Support
spark = create_session_hive()

# Load CSV Files into a DataFrame
covid_raw_df = spark.read.csv(Config.HADOOP_FILE_PATH, header=True, inferSchema=True)

# Data Preprocessing
# 1. Handle missing values in critical columns by filling with appropriate default values.
covid_raw_df = covid_raw_df.fillna({
    "Case_Fatality_Ratio": 0.0,
    "Confirmed": 0,
    "Deaths": 0,
    "Recovered": 0,
    "Active": 0,
    "Incident_Rate": 0.0
})

# 2. Handle missing or malformed country names by dropping rows where 'Country_Region' is null.
covid_raw_df = covid_raw_df.filter(covid_raw_df["Country_Region"].isNotNull())

# 3. Handle duplicate rows based on key columns (e.g., Country_Region, Last_Update).
covid_raw_df = covid_raw_df.dropDuplicates(["Country_Region", "Last_Update"])

# Process Country Data
country_df = covid_raw_df.select(
    col("Country_Region").alias("Name"),
    col("Lat").alias("latitude").cast(FloatType()),
    col("Long_").alias("longitude").cast(FloatType())
).distinct()

# Handle missing latitude or longitude by setting them to 0 (or another placeholder)
country_df = country_df.fillna({"latitude": 0.0, "longitude": 0.0})

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

# 4. Handle negative or implausible values in numerical columns by replacing them with default values.
covid_data_df = covid_data_df.withColumn(
    "Confirmed", when(col("Confirmed") < 0, 0).otherwise(col("Confirmed"))
).withColumn(
    "Deaths", when(col("Deaths") < 0, 0).otherwise(col("Deaths"))
).withColumn(
    "Recovered", when(col("Recovered") < 0, 0).otherwise(col("Recovered"))
).withColumn(
    "Active", when(col("Active") < 0, 0).otherwise(col("Active"))
).withColumn(
    "Incident_Rate", when(col("Incident_Rate") < 0, 0.0).otherwise(col("Incident_Rate"))
)

# Map Country Names to IDs
def map_country_id(country_name):
    return broadcast_country_map.value.get(country_name, None)

map_country_udf = spark.udf.register("map_country_id", map_country_id, IntegerType())
covid_data_df = covid_data_df.withColumn(
    "country_id", map_country_udf(col("Country_Region"))
).drop("Country_Region")

# Handle rows with missing or invalid country IDs by setting them to None (or another placeholder)
covid_data_df = covid_data_df.fillna({"country_id": None})

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

# Stop the Spark session
spark.stop()
