from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from app.llm.openai import OpenAILLM
from app.core.config import mongodb_settings
# from app.core.custom_logging import get_logger

# from venv import logger

llm = OpenAILLM()



# MongoDB setup
MONGO_URI = mongodb_settings.MONGODB_URL
DATABASE_NAME = mongodb_settings.MONGODB_DB_NAME
COLLECTION_NAME = mongodb_settings.MONGODB_COLLECTION_NAME





client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
conversations_collection = db[COLLECTION_NAME]

# Define the feedback collection name
FEEDBACK_COLLECTION_NAME = "user_feedback_collection"
user_feedback_collection = db[FEEDBACK_COLLECTION_NAME]

MALICIOUS_PROMPT_COLLECTION_NAME = "Malicious_prompt_collections"
malicious_prompt_collection = db[MALICIOUS_PROMPT_COLLECTION_NAME]

# Add this function to your MongoDB class

async def get_last_message(conversation_id,
                           user_id
                           ):
    """Get the last message in a conversation"""
    try:
        # Convert string ID to ObjectId
        conversation_id = ObjectId(conversation_id)
        
        # Find the conversation
        conversation = await user_feedback_collection.find_one(
            {"_id": conversation_id, "user": user_id}
        )
        
        if not conversation or "queries" not in conversation:
            return None
        
        # Return the last query in the conversation
        queries = conversation.get("queries", [])
        return queries[-1] if queries else None
        
    except Exception as e:
        return None

# async def _ensure_beta_db_exists():
#     try:
#         # Check if collection exists
#         collection_names = await db.list_collection_names()
#         if COLLECTION_NAME not in collection_names:
#             await db.create_collection(COLLECTION_NAME)
#             logger.info(f"Created collection: {COLLECTION_NAME}")
        
#         # # Create indexes if needed
#         # await conversations_collection.create_index([("user", 1)])
#         # await conversations_collection.create_index([("date", -1)])
        
#         logger.info(f"Database and collection setup complete for {DATABASE_NAME}.{COLLECTION_NAME}")
#     except Exception as e:
#         logger.error(f"Error ensuring beta db exists: {str(e)}")
#         raise e


async def _ensure_collection_exists(collection_name, database=db):
    """
    Ensures that a collection exists in the database.
    
    Args:
        collection_name (str): Name of the collection to check/create
        database: Database connection, defaults to global db
        
    Returns:
        None: Function creates collection if needed
    """
    try:
        # Check if collection exists
        collection_names = await database.list_collection_names()
        if collection_name not in collection_names:
            await database.create_collection(collection_name)
        
    except Exception as e:
        raise e

async def save_conversation(conversation_id, question, response, source_log_docs, user_id):
    # await _ensure_beta_db_exists()
    
    await _ensure_collection_exists(COLLECTION_NAME)  # Use the generalized function

    
    if conversation_id is not None and conversation_id != "None":
        if source_log_docs is not None:
            await conversations_collection.update_one(
                {"_id": ObjectId(conversation_id), "user": user_id},
                {
                    "$push": {
                        "queries": {
                            "prompt": question,
                            "response": response,
                            "sources": source_log_docs,

                        }
                    }
                },
            )
        else:
            await conversations_collection.update_one(
                {"_id": ObjectId(conversation_id), "user": user_id},
                {
                    "$push": {
                        "queries": {
                            "prompt": question,
                            "response": response,
                        }
                    }
                },
            )
            
    else:
        # create new conversation
        # generate summary
        messages_summary = [
            {
                "role": "assistant",
                "content": "Summarise following conversation in no more than 3 "
                "words, respond ONLY with the summary, use the same "
                "language as the system",
            },
            {
                "role": "user",
                "content": "Summarise following conversation in no more than 3 words, "
                "respond ONLY with the summary, use the same language as the "
                "system \n\nUser: "
                + question
                + "\n\n"
                + "AI: "
                + response,
            },
        ]
        conversation_name = llm.gen(
            model="chat",
            messages=messages_summary,
            max_tokens=30
        )
        if source_log_docs is not None:

            conversation_id = (await conversations_collection.insert_one(
                {
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
                }
            )).inserted_id
        else:
            conversation_id = (await conversations_collection.insert_one(
                {
                    "user": user_id,
                    "date": datetime.utcnow(),
                    "name": conversation_name,
                    "queries": [
                        {
                            "prompt": question,
                            "response": response,
                        }
                    ],
                }
            )).inserted_id
    return conversation_id




async def save_user_feedback_answer(conversation_id, 
                                    user_id, 
                                    law_type,
                                    user_anwser,):
    """
    Save user feedback about unsupported law types to a dedicated collection
    
    Parameters:
    - conversation_id: ID of the conversation this feedback is related to
    - user_id: ID of the user providing feedback
    - law_type: Type of law the user was asking about
    - wants_notification: Boolean indicating if user wants to be notified when the law becomes available
    - additional_comment: Optional comment provided by the user
    - user_email: Optional email for notification purposes
    
    Returns:
    - ID of the created feedback document
    """
    await _ensure_collection_exists(FEEDBACK_COLLECTION_NAME)
    
    # Create feedback document
    feedback_doc = {
        "conversation_id": conversation_id,
        "user_id": user_id,
        "law_type": law_type,
        "user_answer": user_anwser,
        "date": datetime.utcnow(),
    }
    
    # Insert the document and return its ID
    result = await user_feedback_collection.insert_one(feedback_doc)
    
    return result.inserted_id


async def save_malicious_prompt(prompt_text, user_id=None, law_type=None, label=None, probabilities=None):
    """
    Ensures the Malicious_prompt_collections exists and writes the input prompt and metadata to it.
    Args:
        prompt_text (str): The prompt to be saved as potentially malicious.
        conversation_id (str or ObjectId, optional): Related conversation ID.
        user_id (str, optional): User ID.
        law_type (str, optional): Law type.
    Returns:
        The inserted document ID.
    """
    await _ensure_collection_exists(MALICIOUS_PROMPT_COLLECTION_NAME)
    doc = {
        "prompt": prompt_text,
        "user_id": user_id,
        "law_type": law_type,
        "label": label,
        "probabilities": probabilities,
        "date": datetime.utcnow(),
    }
    result = await malicious_prompt_collection.insert_one(doc)
    return result.inserted_id