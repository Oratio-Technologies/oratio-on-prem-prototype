import pandas as pd
from llm.prompt_templates import InferenceTemplate
from rag.retriever import VectorRetriever
from config import settings

class RAG_Orchestrator:
    def __init__(self) -> None:
        self.template = InferenceTemplate()

    def retrieve(self, query: str, enable_rag: bool = True) -> dict:
        prompt_template = self.template.create_template(enable_rag=enable_rag)
        prompt_template_variables = {"question": query}

        if enable_rag:
            retriever = VectorRetriever(query=query)
            context = retriever.retrieve_top_k(9)  # Retrieves relevant context for the query
            prompt_template_variables["context"] = context
            prompt = prompt_template.format(question=query, context=context)
        else:
            prompt = prompt_template.format(question=query)

        return {"prompt": prompt, "context": context}
