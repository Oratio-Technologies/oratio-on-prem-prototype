from datetime import datetime
from typing import Optional, Tuple, List
import uuid

import numpy as np

from models.base import VectorDBDataModel



class PdfEmbeddedChunkModel(VectorDBDataModel):
    entry_id: str
    source: str
    chunk_id: str
    chunk_content: str
    embedded_content: np.ndarray
    num_pages: Optional[int] 
    document_title: str
    generated_qeustions: List[str]

    type: str

    
    class Config:
        arbitrary_types_allowed = True

    def to_payload(self) -> Tuple[str, np.ndarray, dict]:
        data = {
            "id": self.entry_id,
            "source": self.source,
            "content": self.chunk_content,
            "num_pages": self.num_pages,
            "type": self.type,
        }

        # Use UUID for the point ID instead of chunk_id which might be an MD5 hash
        point_id = str(uuid.uuid4())
        return point_id, self.embedded_content, data
