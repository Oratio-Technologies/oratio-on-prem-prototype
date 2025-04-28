import os
import logging

from fastapi import APIRouter, HTTPException, Depends, Request

# from app.dependencies.auth import verify_jwt
from schemas.answer import AnswerRequest, AnswerResponse, Source
# from app.schemas.token import TokenUsage
# from app.retriever.rag import LLMOnly
# from app.core.mongo import MongoDB
# from app.dependencies.db import save_conversation
# from app.dependencies.token import verify_token_usage, TokenUsage

from retriever.classic_rag import AccountantsRAG


# Initialize logger
logger = logging.getLogger(__name__)

# Load prompt template
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(CURRENT_DIR, "../prompts")

try:
    with open(os.path.join(PROMPTS_DIR, "chat_combine_default.txt"), "r") as file:
        CHAT_COMBINE = file.read()
except FileNotFoundError as e:
    raise FileNotFoundError("Prompt file is missing. Please ensure it is in the 'prompts' directory.")




answer_router = APIRouter()
# mongo = MongoDB()



@answer_router.post("/api/answer", response_model=AnswerResponse)
async def answer_endpoint(
    request: Request,
    answer_request: AnswerRequest,
    # token_usage: TokenUsage = Depends(verify_token_usage),
    # user = Depends(verify_jwt)
):
    try:
        # # Count input tokens before processing
        # token_manager = request.state.token_manager
        # input_tokens = token_manager.count_tokens(answer_request.question)
        
        # # Check if we can process this many input tokens
        # await token_manager.check_limits(
        #     request.state.token_usage,
        #     input_tokens=input_tokens,
        #     output_tokens=0  # We don't know output tokens yet
        # )
        
        # Get the answer
        retriever = AccountantsRAG(
            question=answer_request.question,
            chat_history=answer_request.history,
            prompt=CHAT_COMBINE
        )
        answer, docs = await retriever.gen()
        


        return AnswerResponse(
            answer=answer,
            sources=[
                Source(
                    source=str(doc.get("source", "")),
                    text=str(doc.get("text", "")),
                    metadata=doc.get("metadata", {})
                ) for doc in docs
            ],
            conversation_id="fake_conversation_id",  # Placeholder for conversation ID
        )
        
    except HTTPException as e:
        # Re-raise HTTP exceptions (like token limits) as-is
        raise e
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
