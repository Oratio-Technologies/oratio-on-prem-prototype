from typing import List, Dict, Tuple, Any, Set, Optional

from app.retriever.base import BaseRetriever
from app.vectorstore.qdrant import VectorRetriever
from app.llm.openai import OpenAILLM
from app.core.config import mongodb_settings
from app.core.mongo import read_mongo_data
from app.utils.custom_logging import get_logger

logger = get_logger("classic_rag")


class AccountantsRAG(BaseRetriever):
    """
    RAG (Retrieval-Augmented Generation) system for accountants.
    Retrieves relevant documents and generates responses using LLM.
    """
    
    def __init__(
        self,
        question: str,
        chat_history: List[Dict[str, str]],
        prompt: str,
        chunks: int = 18,
        token_limit: int = 150,
    ):
        self.question = question
        self.chat_history = chat_history
        self.prompt = prompt
        self.chunks = chunks
        self.token_limit = token_limit

    def _deduplicate_mongo_ids(self, mongo_ids: List[str]) -> List[str]:
        """Remove duplicate MongoDB IDs while preserving order."""
        seen_ids: Set[str] = set()
        deduplicated_ids = []
        
        for doc_id in mongo_ids:
            if doc_id and doc_id not in seen_ids:
                seen_ids.add(doc_id)
                deduplicated_ids.append(doc_id)
                
        return deduplicated_ids

    def _deduplicate_docs(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate documents based on their text content."""
        seen_texts: Set[str] = set()
        deduplicated_docs = []
        
        for doc in docs:
            text = doc.get("text", "").strip()
            if not text or text in seen_texts:
                continue
                
            seen_texts.add(text)
            deduplicated_docs.append(doc)
            
        return deduplicated_docs

    async def _retrieve_vector_documents(self) -> List[str]:
        """Retrieve documents from vector store and extract MongoDB IDs."""
        if self.chunks == 0:
            return []
        
        retriever = VectorRetriever()
        docs_temp = retriever.search(self.question, k=self.chunks)
        
        mongo_ids = [
            doc.payload.get("mongo_id") 
            for doc in docs_temp 
            if doc.payload.get("mongo_id")
        ]
        
        return self._deduplicate_mongo_ids(mongo_ids)

    async def _fetch_mongodb_documents(self, mongo_ids: List[str]) -> List[Dict[str, Any]]:
        """Fetch documents from MongoDB using provided IDs."""
        mongo_docs = []
        
        for doc_id in mongo_ids:
            fetched_doc = await read_mongo_data(mongodb_settings.JUSTICE_COLLECTION_NAME, doc_id)
            if fetched_doc:
                mongo_docs.append(fetched_doc)
                
        return mongo_docs

    async def _get_data(self) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        """Retrieve and process all necessary data for RAG."""
        mongo_ids = await self._retrieve_vector_documents()
        
        if not mongo_ids:
            return [], []
        
        mongo_docs = await self._fetch_mongodb_documents(mongo_ids)
        
        if not mongo_docs:
            return [], []
        
        metaprompt_list = []
        docs = []
        docs_link = "https://home.registre-entreprises.tn/wp-content/uploads/2022/10/orders/fr/"
        for doc in mongo_docs:
            extracted_text = doc.get("extracted_text", "")
            if extracted_text.strip():
                metaprompt_list.append({"extracted_text": extracted_text})
            
            document_title = doc.get("document_title", "Untitled")
            docs.append({
                "title": document_title.split("/")[-1],
                "text": document_title,
                "source": docs_link + doc.get("source", "local"), # TODO: updata the link in frontend to lead to pdf : https://home.registre-entreprises.tn/wp-content/uploads/2022/10/orders/fr
            })
        
        return self._deduplicate_docs(docs), metaprompt_list

    async def gen(self) -> Tuple[str, List[Dict[str, str]]]:
        """Generate response using retrieved documents and LLM."""
        docs, metaprompt_list = await self._get_data()
        
        if not metaprompt_list:
            return "No relevant documents found to answer your question.", []
        
        docs_together = "\n\n\n".join([doc["extracted_text"] for doc in metaprompt_list])
        
        logger.info(f"docs_together: {docs_together[:1000]}...")
        
        p_chat_combine = self.prompt.replace("{summaries}", docs_together)
        messages_combine = [{"role": "system", "content": p_chat_combine}]
        messages_combine.append({"role": "user", "content": self.question})
        
        logger.info(f"messages_combine: {messages_combine[:-2]}")
        
        llm = OpenAILLM()
        completion = llm.gen(model="chat", messages=messages_combine)
        
        return completion, docs
