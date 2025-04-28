from retriever.base import BaseRetriever
from vectorstore.qdrant import VectorRetriever
from llm.openai import OpenAILLM


from utils.logging import get_logger

from app.retriever.query_expansion import query_expansion, docs_reranker
logger = get_logger("classic_rag")



class ClassicRAG(BaseRetriever):
    def __init__(
    self,
    question,
    # source,
    chat_history,
    prompt,
    chunks=9,
    token_limit=150,
    # gpt_model="docsgpt",
    # user_api_key=None,
    ):
        # self.vectorstore = source["active_docs"] if "active_docs" in source else None
        self.question = question
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
        
    async def _get_data(self, query):
        if self.chunks == 0:
            return []
        
        retriever = VectorRetriever()
        docs_temp = retriever.search(query, k=self.chunks)
        
        docs = [
            {
                # "title": doc.payload.get("platform", "Untitled").split("/")[-1],
                "title": doc.payload.get("section_title", "Untitled"),
                # "text": doc.payload.get("content", ""),
                "text": doc.payload.get("section_german_content", ""),
                "source": doc.payload.get("law_link", "local"),
            }
            for doc in docs_temp
        ]
        return docs

  
    
    async def gen(self):
        # docs = await self._get_data(self.question)
  
        docs = []
        list_query_expansion = query_expansion(self.question, 5, "|||")
        
        for i, query in enumerate(list_query_expansion):
            expansion_docs = await self._get_data(query)
            docs.extend(expansion_docs)
        
        # Convert docs to text format for reranking
        docs_text = [doc["text"] for doc in docs]
        logger.info(f"Original docs count: {len(docs_text)}")
        
        reranked_texts = docs_reranker(self.question, "|||", docs_text)
        logger.info(f"Reranked texts received: {len(reranked_texts)}")
        
        # # Map reranked texts back to full documents - with more robust matching
        reranked_docs = []
        for text in reranked_texts:
            if not text.strip():  # Skip empty strings
                continue
            # Try to find matching document
            for doc in docs:
                if text.strip() == doc["text"].strip():  # Use exact matching
                    reranked_docs.append(doc)
                    break
        
        # logger.info(f"Successfully mapped docs: {len(reranked_docs)}")
        
        if not reranked_docs:  # Fallback if no matches found
            logger.info("No matches found, using original docs")
            reranked_docs = docs  # Use all original docs as fallback
        
        docs_together = "\n\n\n".join([doc["text"] for doc in reranked_docs])
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
        
        # logger.info(f"messages_combine: {messages_combine[:-2]}")
        
        llm = OpenAILLM()
        


        completion = llm.gen(model="chat", messages=messages_combine[:-2])
        print(completion)
        print("\n\n")

        docs = reranked_docs

        return completion, docs

