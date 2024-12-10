import os
from dotenv import load_dotenv

# Load environment variables from .env_dev
load_dotenv(dotenv_path=".env_dev")

HADOOP_FILE_PATH = os.getenv("HADOOP_FILE_PATH")
HIVE_METASTORE_URI = os.getenv("HIVE_METASTORE_URI")

BASE_URL = os.getenv("BASE_URL")