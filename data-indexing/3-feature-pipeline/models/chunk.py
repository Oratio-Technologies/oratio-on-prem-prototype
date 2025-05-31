from datetime import datetime
from typing import Optional, List

from models.base import DataModel

class PdfChunkModel(DataModel):
    entry_id: str
    source: str
    chunk_id: str
    chunk_content: str
    num_pages: Optional[int] 
    document_title: str
    generated_qeustions: List[str]

    type: str

