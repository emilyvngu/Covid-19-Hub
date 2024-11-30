# using hadoop and hive
from flask import Flask, jsonify
from pyspark.sql import SparkSession
from session import create_session_hive
from config import Config
from pyspark.sql.functions import sum, avg
from constants import *
from datetime import datetime
from news_api_response import *
# Initialize SparkSession with Hive Support
spark = create_session_hive()
app = Flask(__name__)
app.config.from_object(Config)


spark = create_session_hive()

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
    
    # Read CovidData table from Hive
    covid_data_df = spark.sql("SELECT * FROM database_name.CovidData")
    
    # Calculate Total Cases, Deaths, Recoveries, and Active Cases
    total_cases = covid_data_df.select(
        sum("Confirmed").alias("Total_Confirmed"),
        sum("Deaths").alias("Total_Deaths"),
        sum("Recovered").alias("Total_Recovered"),
        sum("Active").alias("Total_Active")
    )
    
    # Collect the result as a dictionary
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

    # Read CovidData table from Hive
    covid_data_df = spark.sql("SELECT * FROM database_name.CovidData")
    
    # Calculate Total Cases, Deaths, Recoveries, and Active Cases by Country
    total_cases_by_country = (
        covid_data_df
        .groupBy("country_id")  # Assuming 'country_id' corresponds to countries
        .agg(
            sum("Confirmed").alias("Total_Confirmed"),
            sum("Deaths").alias("Total_Deaths"),
            sum("Recovered").alias("Total_Recovered"),
            sum("Active").alias("Total_Active")
        )
        .orderBy("Total_Confirmed", ascending=False)
    )
    
    # Collect the result as a list of rows
    total_cases_list = total_cases_by_country.collect()
    
    # Map country_id back to country names (join with the Country table)
    country_df = spark.sql("SELECT * FROM database_name.Country")
    country_map = {row["id"]: row["Name"] for row in country_df.collect()}
    
    # Format the result
    result = {}
    for row in total_cases_list:
        country_id = row["country_id"]
        country_name = country_map.get(country_id, "Unknown")
        if country_name in COUNTRIES:  # Ensure it matches the COUNTRIES list
            result[country_name] = {
                'total_cases': row["Total_Confirmed"],
                'total_deaths': row["Total_Deaths"],
                'total_recovered': row["Total_Recovered"],
                'total_active': row["Total_Active"]
            }
    
 
    
    return result

def case_fatality_ratio():
   
    # Read CovidData table from Hive
    covid_data_df = spark.sql("SELECT * FROM database_name.CovidData")
    
    # Calculate average case fatality ratio by country_id
    cfr_by_country = (
        covid_data_df
        .groupBy("country_id")
        .agg(avg("Case_Fatality_Ratio").alias("Avg_Case_Fatality_Ratio"))
        .orderBy("Avg_Case_Fatality_Ratio", ascending=False)
    )
    
    # Read Country table to map country_id to country name, latitude, and longitude
    country_df = spark.sql("SELECT * FROM database_name.Country")
    country_map = {
        row["id"]: {
            "name": row["Name"],
            "latitude": row["latitide"],
            "longitude": row["longitude"]
        }
        for row in country_df.collect()
    }
    
    # Collect the results
    cfr_by_country_list = cfr_by_country.collect()
    
    # Format the result
    result = {}
    for row in cfr_by_country_list:
        country_id = row["country_id"]
        country_data = country_map.get(country_id, {})
        
        if country_data and country_data["name"] in COUNTRIES:
            country_name = country_data["name"]
            result[country_name] = {
                'case_fatality_ratio': row["Avg_Case_Fatality_Ratio"],
                'latitude': country_data["latitude"],
                'longitude': country_data["longitude"]
            }
    
    return result


def total_cases_over_time():

    # Read CovidData table from Hive
    covid_data_df = spark.sql("SELECT * FROM database_name.CovidData")
    
    # Convert 'Last_Update' to date type and aggregate total cases over time
    total_cases_over_time = (
        covid_data_df
        .withColumn("date")
        .groupBy("date")
        .agg(
            sum("Confirmed").alias("Total_Confirmed"),
            sum("Deaths").alias("Total_Deaths"),
            sum("Recovered").alias("Total_Recovered")
        )
        .orderBy("date")
    )
    
    # Collect the results
    total_cases_over_time_list = total_cases_over_time.collect()
    
    # Initialize lists to store the results
    dates = []
    total_cases = []
    total_deaths = []
    total_recovered = []
    
    # Populate the lists with data
    for row in total_cases_over_time_list:
        dates.append(row["date"])
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