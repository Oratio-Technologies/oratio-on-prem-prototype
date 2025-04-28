from typing import List
import numpy as np
from openai import AzureOpenAI
import os





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









if __name__ == "__main__":
    # Example usage
    text = "This is a test sentence."
    embedding = get_embedding_3_large_simple(text)
    print(embedding)