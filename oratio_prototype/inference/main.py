from fastapi import FastAPI, Request
from inference_pipeline import RAG_Orchestrator
from utils.logging import get_logger

# Initialize logger and orchestrator
logger = get_logger(__name__)
retriever = RAG_Orchestrator()

# Create FastAPI instance
app = FastAPI()

@app.post("/process_query")
async def process_query(request: Request):
    data = await request.json()
    query = data.get("query")
    
    if not query:
        logger.error("Query is missing from the request")
        return {"error": "Query is required"}

    # Retrieve information based on the query
    response = retriever.retrieve(query)
    
    return response  # This will now return both the prompt and the context
