from flask import Flask, jsonify
from pyspark.sql import SparkSession
from config import Config
from pyspark.sql.functions import sum, avg
from constants import *
from datetime import datetime
from news_api_response import *
# Create a Spark session at the start of your application
spark = SparkSession.builder.appName("CovidDataAnalysis").getOrCreate()
# 172.17.0.2
df_pyspark = spark.read.csv('hdfs://localhost:9000/user/riddhi/data/*.csv',inferSchema=True,header=True)
app = Flask(__name__)
app.config.from_object(Config)


def is_valid_date_format(date_string):
    try:
        # Attempt to parse the date string with the specified format
        datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
        return True
    except ValueError:
        return False

def covid_news():
    return news


def total_cases():
    # Total Cases, Deaths, Recoveries, and Active Cases
    total_cases = df_pyspark.select(
    sum("Confirmed").alias("Total_Confirmed"),
    sum("Deaths").alias("Total_Deaths"),
    sum("Recovered").alias("Total_Recovered"),
    sum("Active").alias("Total_Active")
)
    # print(total_cases.show())
    total_cases_dict = total_cases.collect()[0].asDict()
    
    # Format the dictionary to match the desired output
    result = {
        'total_cases': total_cases_dict['Total_Confirmed'],
        'total_deaths': total_cases_dict['Total_Deaths'],
        'total_recovered': total_cases_dict['Total_Recovered'],
        'total_active': total_cases_dict['Total_Active']
    }
    
    return result

def country_total_cases():
    
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
    # print(total_cases_by_country.show())
    total_cases_list = total_cases_by_country.collect()
    result = {}
    for row in total_cases_list:
        country = row["Country_Region"]
        if country in COUNTRIES:
            result[str(country)] = {
                'total_cases': row["Total_Confirmed"],
                'total_deaths': row["Total_Deaths"],
                'total_recovered': row["Total_Recovered"],
                'total_active': row["Total_Active"]
            }
    
    return result

def case_fatality_ratio():
    # case fatality ration of each country
    cfr_by_country = (
    df_pyspark
    .groupBy("Country_Region")
    .agg(avg("Case_Fatality_Ratio").alias("Avg_Case_Fatality_Ratio"))
    .orderBy("Avg_Case_Fatality_Ratio", ascending=False)
)
    cfr_by_country_list = cfr_by_country.collect()
    result = {}
    for row in cfr_by_country_list:
        country = row["Country_Region"]
        if country in COUNTRIES:
            result[str(country)] = {
                'case_fatality_ratio': row["Avg_Case_Fatality_Ratio"],
                'latitude': COUNTRIES[country]['latitude'],
                'longitude': COUNTRIES[country]['longitude']
            }
    return result

def total_cases_over_time():
    # Total cases over time
    total_cases_over_time = (
        df_pyspark
        .groupBy("Last_Update")
        .agg(
            sum("Confirmed").alias("Total_Confirmed"),
            sum("Deaths").alias("Total_Deaths"),
            sum("Recovered").alias("Total_Recovered")
        )
        .orderBy("Last_Update")
    )
    
    total_cases_over_time_list = total_cases_over_time.collect()
    
    # Initialize lists to store the results
    dates = []
    total_cases = []
    total_deaths = []
    total_recovered = []
    
    # Populate the lists with data
    for row in total_cases_over_time_list:
        if row["Last_Update"] is not None and row["Total_Confirmed"] is not None and row["Total_Deaths"] is not None and row["Total_Recovered"] is not None and row["Last_Update"] is not None and is_valid_date_format(row["Last_Update"]):
            dates.append(row["Last_Update"])
            total_cases.append(row["Total_Confirmed"])
            total_deaths.append(row["Total_Deaths"])
            total_recovered.append(row["Total_Recovered"])
    
    # Format the result as a dictionary
    result = {
        'date': dates,
        'total_cases': total_cases,
        'total_deaths': total_deaths,
        'total_recovered': total_recovered
    }
    
    return result
@app.route('/total_cases_by_country', methods=['GET'])
def get_total_cases_by_country():
    result = country_total_cases()
    return jsonify(result)

@app.route('/total_cases', methods=['GET'])
def get_total_cases():
    result = total_cases()
    return jsonify(result)

@app.route('/case_fatality_ratio', methods=['GET'])
def get_case_fatality_ratio():
    result = case_fatality_ratio()
    return jsonify(result)
@app.route('/total_cases_over_time', methods=['GET'])
def get_total_cases_over_time():
    result = total_cases_over_time()
    return jsonify(result)

@app.route('/news', methods=['GET'])
def get_news():
    result = covid_news()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001)