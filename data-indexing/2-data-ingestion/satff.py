import json
import logging
import sys
from typing import List
from bson import json_util, ObjectId

from utils import generate_questions

# from queues.mq import RabbitMQConnection, RabbitMQMessageHandler
# from queues.azure_queue import AzureServiceBusConnection, AzureServiceBusMessageHandler
from mq import publish_to_rabbitmq

from config import settings, azure_settings
from db import MongoDatabaseConnector, connection

_database = connection.get_database(settings.MONGO_DATABASE_NAME)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def stream_process():
    try:
        # Setup MongoDB connection
        db = _database
        
        logging.info("Connected to MongoDB.")

        # Watch changes in a specific collection
        changes = db.watch([{"$match": {"operationType": {"$in": ["insert"]}}}])
        for change in changes:
            data_type = change["ns"]["coll"]
            entry_id = change["fullDocument"]["_id"]  # Get the document ObjectId
            doc = change["fullDocument"]
            document_title = doc.get("document_title", "Untitled Document")
            
            # Set the data_type in the document
            change["fullDocument"]["type"] = data_type
            
            # Generate questions as list of strings
            generated_questions = generate_questions(doc["extracted_text"], document_title=document_title)
            
            # Update the document in MongoDB with the processing results
            db[data_type].update_one(
                {"_id": entry_id},
                {"$set": {
                    "generated_questions": generated_questions
                }}
            )
            
            # Extract document name if not present
            document_name = doc.get("document_name")
            if not document_name:
                document_name = "Unknown Document"  # Removed extract_name_from_text call since it's commented out
            
            # Prepare document for messaging with the required schema
            queue_data = {
                "mongo_id": str(entry_id),  # Add the MongoDB ObjectId as string
                "extracted_text": doc.get("extracted_text", ""),
                "source": doc.get("source", ""),
                "num_pages": doc.get("num_pages", 1),
                "document_title": document_title,
                "document_name": document_name,
                "generated_questions": generated_questions,  # Keep as list of strings
                "data_type": data_type
            }

            # Convert to JSON string
            data = json.dumps(queue_data, ensure_ascii=False)

            # Log the document being sent to the queue
            logging.info(f"Document: {queue_data['document_name']} - Type: {data_type}")

            # Send data to rabbitmq
            publish_to_rabbitmq(queue_name=settings.RABBITMQ_QUEUE_NAME, data=data)
            logging.info("Data published to RabbitMQ.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    stream_process()