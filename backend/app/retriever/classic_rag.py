from app.retriever.base import BaseRetriever
from app.vectorstore.qdrant import VectorRetriever
from app.llm.openai import OpenAILLM

from app.core.config import mongodb_settings
from app.core.mongo import  read_mongo_data
from app.utils.custom_logging import get_logger

logger = get_logger("classic_rag")



class AccountantsRAG(BaseRetriever):
    def __init__(
    self,
    question,
    # source,
    chat_history,
    prompt,
    chunks=18,
    token_limit=150,
    # gpt_model="docsgpt",
    # user_api_key=None,
    ):
        self.question = question
        # self.vectorstore = source["active_docs"] if "active_docs" in source else None
        self.chat_history = chat_history
        self.prompt = prompt
        self.chunks = chunks
        self.token_limit = token_limit
        # self.token_limit = (
        #     token_limit
        #     if token_limit
        #     < settings.MODEL_TOKEN_LIMITS.get(
        #         self.gpt_model, settings.DEFAULT_MAX_HISTORY
        #     )
        #     else settings.MODEL_TOKEN_LIMITS.get(
        #         self.gpt_model, settings.DEFAULT_MAX_HISTORY
        #     )
        # self.gpt_model = gpt_model
        
        # self.user_api_key = user_api_key
        
    async def _get_data(self):
        if self.chunks == 0:
            return []
        
        retriever = VectorRetriever()
        docs_temp = retriever.search(self.question, k=self.chunks)
        

        mongo_ids = [doc.payload.get("mongo_id") for doc in docs_temp]
        mongo_docs = []

        # Determine which collection to use based on law type
        collection_name = mongodb_settings.mongodb_settings
        
        # Fetch documents from MongoDB
        for doc_id in mongo_ids:
            fetched_doc = await read_mongo_data(collection_name, doc_id)
            if fetched_doc:  # Only append if document was found
                mongo_docs.append(fetched_doc)

        
        docs = [
            {
                "title": doc.payload.get("document_title", "Untitled").split("/")[-1],
                "text": doc.payload.get("extracted_text", ""),
                "source": doc.payload.get("source", "local"),
            }
            for doc in docs_temp
        ]
        return docs
    
    async def gen(self):
        docs = await self._get_data()
        docs_together = "\n\n\n".join([doc["text"] for doc in docs])
        p_chat_combine = self.prompt.replace("{summaries}", docs_together)
        messages_combine = [{"role": "system", "content": p_chat_combine}]
        
        # for doc in docs:
        #     yield doc
        # processed_history = process_history(self.chat_history)
        # if len(processed_history)>0:
        #     for i in processed_history:
        #         messages_combine.extend([
        #             {"role": "user", "content": i[0]},
        #             {"role": "system", "content": i[1]},
        #         ])

        messages_combine.append({"role": "user", "content": self.question})
        logger.info(f"messages_combine: {messages_combine[:-2]}")
        llm = OpenAILLM()
        
        # llm = GoogleLLM()
        # google_completion = llm.gen(messages=messages_combine[:-2])
        # print(google_completion)
        # print("\n\n")

        completion = llm.gen(model="chat", messages=messages_combine)
        print(completion)
        print("\n\n")

        return completion, docs
