from app.llm.base import BaseLLM
from openai import AzureOpenAI
from app.core.config import azure_settings

class OpenAILLM(BaseLLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.client = AzureOpenAI(
            api_version=azure_settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=azure_settings.AZURE_OPENAI_ENDPOINT,
            api_key=azure_settings.AZURE_OPENAI_API_KEY
        )
    
    def _raw_gen(
        self,
        messages,
        **kwargs
    ): 
        response = self.client.chat.completions.create(
            model=kwargs.get('model', "chat"),
            messages=messages,
            stream=kwargs.get('stream', False)
        )
        return response.choices[0].message.content
    
    
