# Big Data Analytics Platform for COVID-19 Data

This project implements a Big Data Analytics Platform using Apache Hadoop, Apache Spark, and Apache Hive to process and visualize COVID-19 data. The platform integrates data ingestion, transformation, and querying for analyzing COVID-19 statistics across different countries over time.

## Project Overview

The project aims to create a scalable platform that:
- Ingests daily COVID-19 data into Hadoop.
- Uses Apache Spark for data processing and transformations.
- Stores structured data in Apache Hive for querying.
- Provides initial visualizations to gain insights from the data.

The platform is designed to handle large datasets, and it is capable of running on a local Hadoop cluster

## Setup Instructions

1. Install Hadoop and Hive
    Here is the guide to the installations - [Hadoop and hive](https://medium.com/@daibinraju/installing-hadoop-with-hive-on-mac-m1-using-homebrew-3505c6166e83)
2. Create a python virtual environment
   ```
   python3 -m venv <myenvpath>
   ```
4. Activate the virtual environment
    ```
   source venv/bin/activate
    ```
6. Install all the required dependecies
    ```
    pip install -r requirements.txt.
   ```
8. Create a file called `.env_dev` and include the following variables with their respective values
    ```
    HADOOP_FILE_PATH=<YOUR PATH> 
    HIVE_METASTORE_URI=<YOUR PATH>
    ```
9. Run the flask server
   Navigate to the folder where `run.py` exists
   ```
   python3 run.py
   ```
### ERD and Schema Design

The Entity Relationship Diagram (ERD) and schema design for storing COVID-19 data in Hive can be found in the /docs folder. The main tables include:

<img width="1103" alt="ERD" src="https://github.com/user-attachments/assets/2ba43d0a-25f0-4201-857b-877cbe60400f">

### Preprocessing Steps
1. Handling Missing Values:
    For critical numerical columns (Case_Fatality_Ratio, Confirmed, Deaths, etc.), missing values are filled with default values (0.0, 0).
    Rows where `Country_Region` is null are dropped as it is essential for country mapping.
2. Removing Duplicates:
    Duplicates based on `Country_Region` and `Last_Update` are removed.
3. Handling Negative or Implausible Values:
    Negative values in numerical columns like Confirmed, Deaths, Recovered, Active, and Incident_Rate are replaced with 0 or 0.0 to ensure data integrity.
4. Filling Missing Latitude and Longitude:
    Any missing latitude or longitude values are set to 0.0.
5. Country Mapping with Broadcast Variables:
    A broadcast variable is used to map Country_Region to country_id. This improves efficiency when working with large datasets.
### Data ingestion

### data types
1. Csv files
2. json data

### Serving the dashboard
1. Go to your terminal
2. Run the following command:
   ```
   panel serve <path_to_dashboard.py>
   ```
   Replace <path_to_dashboard.py> with the full filepath to your dashboard script.
   Example:
   ```
   panel serve /path/to/your/dashboard.py
   ```
   View your dashboard in the browser: By default, the dashboard will be served at http://localhost:5006/dashboard.

## Authors
[@RiddhiAthreya](https://github.com/RiddhiAthreya), [@emilyvngu](https://github.com/emilyvngu)

