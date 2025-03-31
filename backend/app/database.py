import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

MONGO_URI = os.getenv("MONGO_URI")
DATABAS_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGO_URI)
db = client[DATABAS_NAME] # type: ignore

applications_collection = db["applications"] 