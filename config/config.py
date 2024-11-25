import os
from dotenv import load_dotenv

# Load environment variables from .env_dev
load_dotenv(dotenv_path=".env_dev")

class Config:
    HADOOP_FILE_PATH = os.getenv("HADOOP_FILE_PATH")


