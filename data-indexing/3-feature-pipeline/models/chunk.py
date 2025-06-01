from datetime import datetime
from typing import Optional, List

from models.base import DataModel

class PdfChunkModel(DataModel):
    mongo_id: str
    entry_id: str
    source: str
    chunk_id: str
    chunk_content: str
    num_pages: Optional[int] 
    document_title: str
    generated_questions: List[str]  # Fixed typo: "questions" instead of "qeustions"

    type: str

