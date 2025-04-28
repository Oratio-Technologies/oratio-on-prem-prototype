from app.retriever.base import BaseRetriever
from app.vectorstore.qdrant import VectorRetriever
from app.llm.openai import OpenAILLM


from app.utils.custom_logging import get_logger

logger = get_logger("classic_rag")



class AccountantsRAG(BaseRetriever):
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
        
        docs = [
            {
                "title": doc.payload.get("platform", "Untitled").split("/")[-1],
                "text": doc.payload.get("content", ""),
                "source": doc.payload.get("link", "local"),
            }
            for doc in docs_temp
        ]
        return docs
    
    async def gen(self):
        docs = await self._get_data()
        docs_together = "\n".join([doc["text"] for doc in docs])
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
