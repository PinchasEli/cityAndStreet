import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["FastAPI"]
collection = db["user"]

# Define the update operation
update_operation = {
    "$set": {
        "is_superuser": False,
        "is_staff": False  # Define the fields and values you want to update
    }
}

# Update all documents in the collection
result = collection.update_many({}, update_operation)

# Print the number of documents updated
print("Number of documents updated:", result.modified_count)