from pyspark.sql import SparkSession
from config import HIVE_METASTORE_URI
def create_session():
    spark = SparkSession.builder.appName('Athena').getOrCreate()
    return spark

from pyspark.sql import SparkSession

def create_session_hive():
    # Initialize Spark session with Hive support
    spark = (
        SparkSession.builder
        .appName('Athena')
        .config('spark.sql.catalogImplementation', 'hive')
        .config('spark.sql.hive.metastore.uris', HIVE_METASTORE_URI)  # Metastore URI
        .config('spark.sql.warehouse.dir', '/user/hive/warehouse')  # HDFS or local path
        .enableHiveSupport()
        .getOrCreate()
    )
    return spark



