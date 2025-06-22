import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Get MongoDB credentials
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Establish MongoDB connection
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# Dependency function to access DB
def get_mongo_db():
    return db
