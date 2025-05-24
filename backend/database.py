from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

class Database:
    _instance = None  # Singleton instance

    def __new__(cls):
        """Implement Singleton Pattern"""
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        """Establish MongoDB connection."""
        mongo_uri = os.getenv("MONGO_URI")

        if not mongo_uri:
            print("❌ Error: MONGO_URI is not set in the .env file!")
            self.db = None
            return

        try:
            self.client = MongoClient(mongo_uri)
            self.db = self.client["exam_system"]
            print("✅ Connected to MongoDB Atlas successfully!")
        except Exception as e:
            print("❌ Error connecting to MongoDB Atlas:", e)
            self.db = None

    def get_collection(self, collection_name):
        """Get a collection from the database."""
        if self.db is None:
            print("❌ Error: Database connection is not established!")
            return None
        return self.db[collection_name]

    def insert_one(self, collection_name, data):
        """Insert a single document."""
        collection = self.get_collection(collection_name)
        if collection is None:
            return None
        try:
            result = collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            print(f"❌ Error inserting data into {collection_name}: {e}")
            return None

    def find_one(self, collection_name, query):
        """Find a single document."""
        collection = self.get_collection(collection_name)
        if collection is None:
            return None
        return collection.find_one(query)

    def find_all(self, collection_name, query={}):
        """Find multiple documents."""
        collection = self.get_collection(collection_name)
        if collection is None:
            return []
        return list(collection.find(query))

    def update_one(self, collection_name, query, new_values):
        """Update a single document."""
        collection = self.get_collection(collection_name)
        if collection is None:
            return None
        return collection.update_one(query, {"$set": new_values})

    def delete_one(self, collection_name, query):
        """Delete a single document."""
        collection = self.get_collection(collection_name)
        if collection is None:
            return None
        return collection.delete_one(query)
    
    def insert_exam(self, subject, questions):
        """Insert a new exam into the database."""
        exam_data = {
            "subject": subject,
            "questions": questions,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        return self.insert_one("exams", exam_data)
    
    def get_all_exams(self):
        """Fetch all exams from the database."""
        return list(self.find_all("exams"))
    
    def get_all_results(self):
        """Fetch all exam results from the database."""
        return list(self.find_all("results"))
    
    def count_documents(self, collection_name, query):
        return self.db[collection_name].count_documents(query)
    
# Initialize database instance
db_instance = Database()
