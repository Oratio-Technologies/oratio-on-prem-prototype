# import sys
# sys.path.insert(0, "/home/mohamed-ayari/projects/oratio/oratio-on-prem-prototype/backend")


from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional, Dict
from bson import ObjectId
from app.core.config import mongodb_settings
from app.llm.openai import OpenAILLM  # Assuming you have an LLM class similar to OpenAILLM


llm = OpenAILLM()
class MongoDB:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._client = AsyncIOMotorClient(mongodb_settings.MONGODB_URL)
        self._db = self._client[mongodb_settings.MONGODB_DB_NAME]
        self.conversations = self._db[mongodb_settings.MONGODB_COLLECTION_NAME]

    async def _ensure_collection_exists(self):
        """Ensure the conversations collection exists"""
        try:
            collections = await self._db.list_collection_names()
            if mongodb_settings.MONGODB_COLLECTION_NAME not in collections:
                await self._db.create_collection(mongodb_settings.MONGODB_COLLECTION_NAME)
        except Exception as e:
            raise Exception(f"Error ensuring collection exists: {str(e)}")
   
    async def save_conversation(
        self, 
        conversation_id: Optional[str], 
        question: str, 
        response: str, 
        source_log_docs: List, 
        user_id: str
    ) -> str:
        """Save or update a conversation"""
        await self._ensure_collection_exists()
        
        if conversation_id and conversation_id != "None":
            # Update existing conversation
            await self.conversations.update_one(
                {"_id": ObjectId(conversation_id), "user": user_id},
                {
                    "$push": {
                        "queries": {
                            "prompt": question,
                            "response": response,
                            "sources": source_log_docs,
                        }
                    }
                }
            )
            return conversation_id
        else:
            # Generate conversation summary
            messages_summary = [
                {
                    "role": "assistant",
                    "content": "Summarise following conversation in no more than 3 "
                    "words, respond ONLY with the summary, use the same "
                    "language as the system",
                },
                {
                    "role": "user",
                    "content": f"Summarise following conversation in no more than 3 words, "
                    f"respond ONLY with the summary, use the same language as the "
                    f"system \n\nUser: {question}\n\nAI: {response}",
                },
            ]
            conversation_name = await llm.gen(
                model="chat",
                messages=messages_summary,
                max_tokens=30
            )

            # Create new conversation
            result = await self.conversations.insert_one({
                "user": user_id,
                "date": datetime.utcnow(),
                "name": conversation_name,
                "queries": [
                    {
                        "prompt": question,
                        "response": response,
                        "sources": source_log_docs,
                    }
                ],
            })
            return str(result.inserted_id)


    async def get_conversations(self, user_id: str, limit: int = 30) -> List[Dict]:
        """Retrieve the latest conversations for a user"""
        await self._ensure_collection_exists()
        
        conversations = await self.conversations.find(
            {"user": user_id}
        ).sort("date", -1).limit(limit).to_list(limit)
        
        return [
            {
                "id": str(conversation["_id"]),
                "name": conversation["name"]
            }
            for conversation in conversations
        ]

    async def get_single_conversation(self, conversation_id: str, user_id: str) -> Dict:
        """Retrieve a single conversation by ID"""
        await self._ensure_collection_exists()
        
        try:
            conversation = await self.conversations.find_one(
                {"_id": ObjectId(conversation_id), "user": user_id}
            )
            
            if not conversation:
                raise ValueError("Conversation not found")
                
            return conversation["queries"]
            
        except Exception as e:
            raise ValueError(f"Error retrieving conversation: {str(e)}")
        

import asyncio
   

async def read_mongo_data(collection_name, mongo_id):
    """
    Asynchronously retrieve document data from MongoDB collection based on mongo_id
    
    Args:
        collection_name: MongoDB collection name
        mongo_id: MongoDB document ID (can be string or ObjectId)
        
    Returns:
        Document data as dictionary or None if not found
    """
    try:
        # Connect to MongoDB using Motor
        client = AsyncIOMotorClient(mongodb_settings.MONGODB_URL)
        db = client[mongodb_settings.JUSTICE_DB_NAME]
        
        # Get the specified collection
        collection = db[collection_name]
        
        # Try to find the document with the string ID first
        document = await collection.find_one({"_id": mongo_id})
        
        return document
    
    except Exception as e:
        print(f"Error retrieving data from MongoDB: {e}")
        return None
    

# Example usage
async def main():
    # Example collection name and document ID
    collection = "labor_law_sections"
    doc_id = "6545936a-c536-4ace-8c4e-d0318bba1234"
    
    # 1. Try by _id directly
    document = await read_mongo_data(collection, doc_id)
    
    if document:
        print(f"Document found with _id: {document.get('paragraphs')}")


# Run the async function
if __name__ == "__main__":
    asyncio.run(main())