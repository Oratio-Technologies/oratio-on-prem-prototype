import os
from pymongo import MongoClient


def insert_data_to_mongodb(uri, database_name, collection_name, data):
    """
    Insert data into a MongoDB collection.

    :param uri: MongoDB URI
    :param database_name: Name of the database
    :param collection_name: Name of the collection
    :param data: Data to be inserted (dict)
    """
    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]

    try:
        result = collection.insert_one(data)
        print(f"Data inserted with _id: {result.inserted_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    MONGODB_PWD = os.getenv("MONGODB_PWD")

    insert_data_to_mongodb(
        f"mongodb+srv://zoldyck:{MONGODB_PWD}@cluster0.kjantw5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        "production",
        "posts",
        {"platform": "linkedin", "content": "Test content"}
    )

