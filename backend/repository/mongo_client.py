"""
MongoDB client initialization for Personal AI Assistant.
Loads configuration from environment variables only.
"""
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    raise RuntimeError("MONGO_URL environment variable must be set in your .env file.")

client = AsyncIOMotorClient(MONGO_URL)
db = client["personal_ai"]
documents_collection = db["documents"]
