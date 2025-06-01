from typing import List, Dict, Tuple, Any, Set, Optional

from app.retriever.base import BaseRetriever
from app.vectorstore.qdrant import VectorRetriever
from app.llm.openai import OpenAILLM
from app.core.config import mongodb_settings
from app.core.mongo import read_mongo_data
from app.utils.custom_logging import get_logger
from app.utils.helpers import process_history
logger = get_logger("classic_rag")


def docs_reranker(question: str, separator: str, document_titles: List[str]) -> list[str]:
    llm = OpenAILLM()
    titles_text = separator.join(document_titles)
    
    messages_combine = [{"role": "system", 
                         "content":f"""You are analyzing Business Registration document titles to find the most relevant ones needed to answer this question: "{question}"

                                        Your task is simple:
                                        1. Read each document title carefully
                                        2. Ask yourself: "Can this document help to answer the question?"
                                        3. If yes, keep it. If no, remove it.

                                        Keep a document title if:
                                        - The document contains key legal information needed for the answer
                                        - The document provides essential context or conditions relevant to the question
                                        - The document title indicates it covers the topic being asked about

                                        Remove a document title if:
                                        - The document is not needed to answer the question
                                        - The document title indicates it's about a different topic

                                        Technical Requirements:
                                        - Return document titles exactly as they appear in the input
                                        - Separate titles with '{separator}'
                                        - Don't add any comments or explanations
                                        - Don't modify the titles in any way

                                        Input document titles:
                                        {titles_text}
                                        """}]
    messages_combine.append({"role": "user", "content": "Return only the document titles that are essential for answering the question, exactly as they appear."})
    
    completion = llm.gen(model="chat", messages=messages_combine)
    list_output = [text.strip() for text in completion.split(separator) if text.strip()]
    
    # Ensure we're getting exact matches from original document titles
    validated_output = []
    seen_titles = set()  # To prevent duplicates
    for title in list_output:
        title_stripped = title.strip()
        if title_stripped in seen_titles:
            continue
        for original in document_titles:
            if title_stripped == original.strip():
                validated_output.append(original)
                seen_titles.add(title_stripped)
                break
    
    # If no valid matches found, return original document titles
    if not validated_output:
        return document_titles
    
    return validated_output


def query_expansion(question: str,
                    to_expand_to_n: int,
                    target_language: str = "English") -> list[str]:
    llm = OpenAILLM()
    
    messages_combine = [{"role": "system", 
                         "content": f"""You are a Business Registration Expert with extensive expertise in:
                         - Business entity formation and registration procedures
                         - Corporate law, commercial law, and association law
                         - RNE (Registre National des Entreprises) operations and requirements
                         - Legal terminology for business creation, modification, and dissolution
                         - Administrative procedures for companies, associations, and professional entities
                         
                         Your task: Generate {to_expand_to_n} different English versions of the received query while MAINTAINING THE EXACT SAME COMPLEXITY AND KNOWLEDGE LEVEL as the original question.
                         
                         CRITICAL: PRESERVE THE ORIGINAL QUESTION'S LEVEL:
                         - If the original is a beginner question → generate beginner-level variations
                         - If the original is an expert question → generate expert-level variations  
                         - If the original uses simple language → keep variations simple
                         - If the original uses technical terms → maintain technical complexity
                         - If the original is basic/general → keep variations basic/general
                         - If the original is detailed/specific → maintain detailed/specific level
                         
                         Requirements:
                         - Use varied business and legal terminology while preserving exact meaning AND complexity level
                         - Apply different phrasing styles appropriate to the original question's sophistication level
                         - Incorporate terminology that matches the original question's expertise level
                         - Maintain the precision, specificity, AND complexity of the original business inquiry
                         - Ensure each variation captures all business and legal nuances at the same level
                         - Match the formality level of the original question (casual vs. professional)
                         
                         Constraints:
                         - Do NOT change the core business or legal meaning
                         - Do NOT add new business information or requirements
                         - Do NOT alter the scope of the business inquiry
                         - Do NOT make a simple question complex or a complex question simple
                         - Do NOT change the target audience level (beginner/intermediate/expert)
                         
                         YOU MUST PROVIDE ALL TRANSLATED QUERIES IN ENGLISH.
                         
                         Provide these level-appropriate alternative questions separated by |||.
                                    """}]
    messages_combine.append({"role": "user", "content": question})
    
    completion = llm.gen(model="chat", messages=messages_combine)
    list_output = completion.split('|||')
    return list_output


class AccountantsRAG(BaseRetriever):
    """
    RAG (Retrieval-Augmented Generation) system for accountants.
    Retrieves relevant documents and generates responses using LLM with query expansion and document reranking.
    """
    
    def __init__(
        self,
        question: str,
        chat_history: List[Dict[str, str]],
        prompt: str,
        chunks: int = 18,
        token_limit: int = 150,
        expand_queries: int = 3,
    ):
        self.question = question
        self.chat_history = chat_history
        self.prompt = prompt
        self.chunks = chunks
        self.token_limit = token_limit
        self.expand_queries = expand_queries

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

    async def _expand_query(self) -> List[str]:
        """Expand the original query into multiple variations."""
        expanded_queries = query_expansion(self.question, self.expand_queries)
        # Clean up the expanded queries and add the original question
        cleaned_queries = [query.strip() for query in expanded_queries if query.strip()]
        
        # Always include the original question
        all_queries = [self.question] + cleaned_queries
        
        logger.info(f"Expanded queries: {all_queries}")
        return all_queries

    async def _retrieve_vector_documents(self) -> List[str]:
        """Retrieve documents from vector store using expanded queries and extract MongoDB IDs."""
        if self.chunks == 0:
            return []
        
        # Get expanded queries
        expanded_queries = await self._expand_query()
        
        retriever = VectorRetriever()
        all_mongo_ids = []
        
        # Calculate chunks per query to maintain total chunk limit
        chunks_per_query = max(1, self.chunks // len(expanded_queries))
        
        # Retrieve documents for each expanded query
        for query in expanded_queries:
            docs_temp = retriever.search(query, k=chunks_per_query)
            
            mongo_ids = [
                doc.payload.get("mongo_id") 
                for doc in docs_temp 
                if doc.payload.get("mongo_id")
            ]
            all_mongo_ids.extend(mongo_ids)
        
        return self._deduplicate_mongo_ids(all_mongo_ids)

    async def _fetch_mongodb_documents(self, mongo_ids: List[str]) -> List[Dict[str, Any]]:
        """Fetch documents from MongoDB using provided IDs."""
        mongo_docs = []
        
        for doc_id in mongo_ids:
            fetched_doc = await read_mongo_data(mongodb_settings.JUSTICE_COLLECTION_NAME, doc_id)
            if fetched_doc:
                mongo_docs.append(fetched_doc)
                
        return mongo_docs

    async def _rerank_mongo_documents(self, mongo_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rerank MongoDB documents using document titles for comparison."""
        if not mongo_docs:
            return mongo_docs
        
        # Extract document titles for reranking
        document_titles = []
        title_to_doc_mapping = {}  # Map document_title to original mongo_doc
        
        for doc in mongo_docs:
            document_title = doc.get("document_title", "").strip()
            if document_title:
                document_titles.append(document_title)
                title_to_doc_mapping[document_title] = doc
        
        if not document_titles:
            return mongo_docs
        
        separator = "|||DOCUMENT_SEPARATOR|||"
        
        # Rerank document titles
        reranked_titles = docs_reranker(self.question, separator, document_titles)
        
        logger.info(f"Original mongo docs count: {len(mongo_docs)}, Reranked count: {len(reranked_titles)}")
        
        # Reconstruct mongo_docs list with reranked order based on titles
        reranked_mongo_docs = []
        for title in reranked_titles:
            if title in title_to_doc_mapping:
                reranked_mongo_docs.append(title_to_doc_mapping[title])
        
        return reranked_mongo_docs

    async def _get_data(self) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        """Retrieve and process all necessary data for RAG with query expansion and reranking."""
        mongo_ids = await self._retrieve_vector_documents()
        
        if not mongo_ids:
            return [], []
        
        mongo_docs = await self._fetch_mongodb_documents(mongo_ids)
        
        if not mongo_docs:
            return [], []
        
        # Apply reranking to the mongo documents first
        reranked_mongo_docs = await self._rerank_mongo_documents(mongo_docs)
        
        # Now process both lists from the same reranked mongo_docs
        metaprompt_list = []
        docs = []
        docs_link = "https://home.registre-entreprises.tn/wp-content/uploads/2022/10/orders/fr/"
        
        for doc in reranked_mongo_docs:
            extracted_text = doc.get("extracted_text", "")
            if extracted_text.strip():
                metaprompt_list.append({"extracted_text": extracted_text})
            
            document_title = doc.get("document_title", "Untitled")
            docs.append({
                "title": document_title.split("/")[-1],
                "text": document_title,
                "source": docs_link + doc.get("source", "local"),
            })
        
        return self._deduplicate_docs(docs), metaprompt_list

    async def gen(self) -> Tuple[str, List[Dict[str, str]]]:
        """Generate response using retrieved documents and LLM with query expansion and reranking."""
        docs, metaprompt_list = await self._get_data()
        
        if not metaprompt_list:
            return "No relevant documents found to answer your question.", []
        
        docs_together = "\n\n\n".join([doc["extracted_text"] for doc in metaprompt_list])
        
        logger.info(f"docs_together: {docs_together[:1000]}...")
        logger.info(f"Final document count after reranking: {len(metaprompt_list)}")
        
        p_chat_combine = self.prompt.replace("{summaries}", docs_together)
        messages_combine = [{"role": "system", "content": p_chat_combine}]
       
        # Process history
        processed_history = process_history(self.chat_history)
        if processed_history:
            for user_msg, bot_msg in processed_history:
                messages_combine.extend([
                    {"role": "user", "content": user_msg},
                    {"role": "system", "content": bot_msg},
                ])
       
       
       
        messages_combine.append({"role": "user", "content": self.question})
        
        logger.info(f"messages_combine: {messages_combine[:-2]}")
        
        llm = OpenAILLM()
        completion = llm.gen(model="chat", messages=messages_combine)
        
        return completion, docs