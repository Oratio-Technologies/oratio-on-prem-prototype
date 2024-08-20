from abc import ABC, abstractmethod

from langchain.prompts import PromptTemplate
from pydantic import BaseModel


class BasePromptTemplate(ABC, BaseModel):
    @abstractmethod
    def create_template(self, *args) -> PromptTemplate:
        pass

class InferenceTemplate(BasePromptTemplate):
    simple_prompt: str = """You are an AI language model assistant. Your task is to generate a cohesive and concise response to the user question.
    Question: {question}
    """

    rag_prompt: str = """ You are a specialist in technical content writing. Your task is to create technical content based on a user query given a specific context 
    with additional information consisting of the user's previous writings and his knowledge.
    
    Here is a list of steps that you need to follow in order to solve this task:
    Step 1: You need to analyze the user provided query : {question}
    Step 2: You need to analyze the provided context and how the information in it relates to the user question: {context}
    Step 3: Generate the content keeping in mind that it needs to be as cohesive and concise as possible related to the subject presented in the query and similar to the users writing style and knowledge presented in the context.
    """

    def create_template(self, enable_rag: bool = True) -> PromptTemplate:
        if enable_rag is True:
            return PromptTemplate(
                template=self.rag_prompt, input_variables=["question", "context"]
            )

        return PromptTemplate(template=self.simple_prompt, input_variables=["question"])