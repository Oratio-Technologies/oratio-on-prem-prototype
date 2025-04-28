from typing import List
import requests
import numpy as np




from openai import AzureOpenAI
from typing import List, Union

# # text-embedding-3-large:
# os.environ["AZURE_OPENAI_API_KEY"] = "Bnr9Ii0tTFR2CY34yQsKVhY2f31OpaooWaeHCc7Da8RkMgKxiJvuJQQJ99BCACYeBjFXJ3w3AAAAACOGIvGv"
# os.environ["AZURE_OPENAI_ENDPOINT"] = "https://alac-m8g2szz4-eastus.cognitiveservices.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"


def get_embedding_3_large_simple(text: str) -> np.ndarray:
    """
    A simplified version of get_embedding_3_large that generates embeddings using text-embedding-3-large model.
    
    Args:
        text (str): Input text to generate embedding for
        
    Returns:
        np.ndarray: The embedding vector for the input text as a numpy array
    """
    client = AzureOpenAI(
        api_key="Bnr9Ii0tTFR2CY34yQsKVhY2f31OpaooWaeHCc7Da8RkMgKxiJvuJQQJ99BCACYeBjFXJ3w3AAAAACOGIvGv",
        api_version="2023-05-15",
        azure_endpoint="https://alac-m8g2szz4-eastus.cognitiveservices.azure.com",
        azure_deployment="text-embedding-3-large"
    )
    
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-large"
    )
    
    return np.array(response.data[0].embedding)

def embed_german_text(text: str):
    url = "http://131.189.31.20:8009/embed"
    payload = {
        "texts": [text],
        "to_list": True
    }
    response = requests.post(
        url=url,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        # Convert the 768-dimensional list directly to numpy array
        return np.array(response.json()["embeddings"])
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


      
      
      
# from InstructorEmbedding import INSTRUCTOR
            
# def embedd_repositories(text: str):
#     model = INSTRUCTOR("hkunlp/instructor-xl")
#     sentence = text
#     instruction = "Represent the structure of the repository"
#     return model.encode([instruction, sentence])


