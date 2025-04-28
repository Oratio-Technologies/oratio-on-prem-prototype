from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
)

from config import settings


# def chunk_text(text: str) -> list[str]:
#     character_splitter = RecursiveCharacterTextSplitter(
#         separators=["\n\n"], chunk_size=500, chunk_overlap=0
#     )
#     text_split = character_splitter.split_text(text)

#     token_splitter = SentenceTransformersTokenTextSplitter(
#         chunk_overlap=50,
#         tokens_per_chunk=settings.EMBEDDING_MODEL_MAX_INPUT_LENGTH,
#         model_name=settings.EMBEDDING_MODEL_ID,
#     )
#     chunks = []

#     # for section in text_split:
#     #     chunks.extend(token_splitter.split_text(section))

#     return chunks

from typing import List

def chunk_text(text: str) -> List[str]:
    """
    Split text into chunks of approximately 1000 characters, trying to break at paragraph boundaries.
    
    Parameters:
    -----------
    text : str
        The input text to be chunked
        
    Returns:
    --------
    List[str]
        A list of text chunks
    """
    # Define fixed chunk size
    chunk_size: int = 1000
    
    # Split by paragraphs (empty lines)
    paragraphs: List[str] = []
    current: List[str] = []
    
    for line in text.split('\n'):
        # Skip standalone page numbers
        if line.strip().isdigit() and len(line.strip()) < 3:
            continue
            
        if line.strip() == '':
            if current:
                paragraphs.append('\n'.join(current))
                current = []
        else:
            current.append(line)
    
    # Add the last paragraph if exists
    if current:
        paragraphs.append('\n'.join(current))
    
    # Group paragraphs into chunks
    chunks: List[str] = []
    current_chunk: List[str] = []
    current_size: int = 0
    
    for paragraph in paragraphs:
        paragraph_size: int = len(paragraph)
        
        # If adding this paragraph would exceed the chunk size and we already have content
        if current_size + paragraph_size > chunk_size and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_size = 0
        
        current_chunk.append(paragraph)
        current_size += paragraph_size
    
    # Add the last chunk if exists
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks