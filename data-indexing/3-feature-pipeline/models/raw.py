from datetime import datetime
from typing import Optional, Tuple, List

from models.base import DataModel, VectorDBDataModel





class PdfRawModel(DataModel):
    mongo_id: str
    extracted_text: str
    source: str
    num_pages: Optional[int] 
    document_title: str
    generated_questions: List[str]










