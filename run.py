import pyspark
import pandas as pd
from session import create_session
from pyspark.sql.functions import sum,avg,when
import os
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import shutil
spark = create_session()

def pre_process_data():
#     schema = StructType([
#     StructField("FIPS", StringType(), True),
#     StructField("Admin2", StringType(), True),
#     StructField("Province_State", StringType(), True),
#     StructField("Country_Region", StringType(), True),
#     StructField("Last_Update", StringType(), True),
#     StructField("Lat", DoubleType(), True),
#     StructField("Long_", DoubleType(), True),
#     StructField("Confirmed", IntegerType(), True),
#     StructField("Deaths", IntegerType(), True),
#     StructField("Recovered", IntegerType(), True),
#     StructField("Active", IntegerType(), True),
#     StructField("Combined_Key", StringType(), True),
#     StructField("Incident_Rate", DoubleType(), True),
#     StructField("Case_Fatality_Ratio", DoubleType(), True)
# ])
    expected_columns = [
    "FIPS", "Admin2", "Province_State", "Country_Region", "Last_Update", 
    "Lat", "Long_", "Confirmed", "Deaths", "Recovered", "Active", 
    "Combined_Key", "Incident_Rate", "Case_Fatality_Ratio"
]

 # Directory containing the CSV files
    # Directory containing the CSV files
    input_directory = '/Users/riddhiathreya/Desktop/DS5110/FinalProject/Athena/csse_covid_19_daily_reports/'

    # Get a list of all CSV files in the directory
    csv_files = [os.path.join(input_directory, f) for f in os.listdir(input_directory) if f.endswith('.csv')]

    for csv_file in csv_files:
        try:
            # Read the CSV file into a PySpark DataFrame
            df = spark.read.csv(csv_file, header=True, inferSchema=True)
            file_columns = df.columns
            # print(file_columns)
            # Compare file columns to expected schema
            missing_columns = [col for col in expected_columns if col not in file_columns]
            extra_columns = [col for col in file_columns if col not in expected_columns]
            if missing_columns!=[]:
                print(f"Missing columns: {missing_columns}")
            if extra_columns!=[]:
                print(f"Extra columns: {extra_columns}")
       
            # Rename the column
            # df = df.withColumnRenamed('Country/Region', 'Country_Region')
            # print(df.show())
            # # Save the modified DataFrame back to the original CSV file
            # temp_output_path = csv_file.replace('.csv', '_temp')
            # df.coalesce(1).write.csv(temp_output_path, header=True, mode='overwrite')
            
            # # Find the part file and rename it to the original CSV file name
            # part_file = [f for f in os.listdir(temp_output_path) if f.startswith('part-')][0]
            # os.rename(os.path.join(temp_output_path, part_file), csv_file)
            
            # # Remove the temporary directory and its contents
            # shutil.rmtree(temp_output_path)
    
        
        except Exception as e:
            print(f"Error processing file {csv_file}: {e}")


pre_process_data()

df_pyspark = spark.read.csv('file:///Users/riddhiathreya/Desktop/DS5110/FinalProject/Athena/csse_covid_19_daily_reports/*.csv',inferSchema=True,header=True)
# print(df_pyspark.printSchema())
# # Example: Total cases and deaths by country across all days

# Total Cases, Deaths, Recoveries, and Active Cases by Country
total_cases_by_country = (
    df_pyspark
    .groupBy("Country_Region")
    .agg(
        sum("Confirmed").alias("Total_Confirmed"),
        sum("Deaths").alias("Total_Deaths"),
        sum("Recovered").alias("Total_Recovered"),
        sum("Active").alias("Total_Active")
    )
    .orderBy("Total_Confirmed", ascending=False)
)

print(total_cases_by_country.show())
# # # Case Fatality Ratio (CFR) Comparison

cfr_by_country = (
    df_pyspark
    .groupBy("Country_Region")
    .agg(avg("Case_Fatality_Ratio").alias("Avg_Case_Fatality_Ratio"))
    .orderBy("Avg_Case_Fatality_Ratio", ascending=False)
)


print(cfr_by_country.show())



# # # Recovery Rate Comparison

recovery_rate_by_country = (
    df_pyspark
    .groupBy("Country_Region")
    .agg(
        (sum("Recovered") / when(sum("Confirmed") != 0, sum("Confirmed")).otherwise(1) * 100)
        .alias("Recovery_Rate_Percent")
    )
    .orderBy("Recovery_Rate_Percent", ascending=False)
)
print(recovery_rate_by_country.show())

# # # 5. Countries with High Active Case Counts
high_active_cases = (
    df_pyspark
    .groupBy("Country_Region")
    .agg(sum("Active").alias("Total_Active_Cases"))
    .filter("Total_Active_Cases > 1000")
    .orderBy("Total_Active_Cases", ascending=False)
)
print(high_active_cases.show())

# # print(type(df_pyspark))
# # df_pyspark2 = df_pyspark.withColumn('Experience after 2 years', df_pyspark['Experience']+2)
# # print(df_pyspark2.show())
# # df_py3=df_pyspark.drop('Experience after 2 years')
# # print(df_py3.show())
# # Data preprosession
# # 1. pySpark dataframe
# # 2.Reading the dataset
# # 3. checking the data types of the columns
# # 4. selecting columns and indexing
# # 5. check describe option similar to pandas
# # 6. Adding columns, dropping columns



def total_cases():
    return {'total_cases':500, 'total_deaths':100, 'total_recovered':200, 'total_active':200}

def country_total_cases():
    return {'US':{'total_cases':500, 'total_deaths':100, 'total_recovered':200, 'total_active':200}, 
            'India':{'total_cases':500, 'total_deaths':100, 'total_recovered':200, 'total_active':200}, 
            'Italy':{'total_cases':500, 'total_deaths':100, 'total_recovered':200, 'total_active':200}}

def case_fatality_raion():
  
    return {'US':{"latitude":23,"longitude":34,"case_fatality_ratio":45}, 
            'India':{"latitude":23,"longitude":34,"case_fatality_ratio":45}, 
            'Italy':{"latitude":23,"longitude":34,"case_fatality_ratio":45}}