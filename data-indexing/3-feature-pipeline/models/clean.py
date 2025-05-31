from typing import Optional, Tuple, List
import uuid

from models.base import VectorDBDataModel


class PdfCleanedModel(VectorDBDataModel):
    source: str
    cleaned_extracted_text: str
    num_pages: Optional[int] 
    document_title: str
    generated_qeustions: List[str]


    type: str

    
    def to_payload(self) -> Tuple[str, dict]:
        data = {
            "source": self.source,
            "cleaned_extracted_text": self.cleaned_extracted_text,
            "num_pages": self.num_pages,
            "type": self.type,
        }

        # Use UUID for the point ID instead of entry_id which might be an invalid string
        point_id = str(uuid.uuid4())
        return point_id, data


