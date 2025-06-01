from typing import Optional, Tuple, List
import uuid

from models.base import VectorDBDataModel


class PdfCleanedModel(VectorDBDataModel):
    mongo_id: str
    source: str
    cleaned_extracted_text: str
    num_pages: Optional[int] 
    document_title: str
    generated_questions: List[str]  # Fixed typo: "questions" instead of "qeustions"

    type: str

    
    def to_payload(self) -> Tuple[str, dict]:
        data = {
            "mongo_id": self.mongo_id,
            "source": self.source,
            "cleaned_extracted_text": self.cleaned_extracted_text,
            "num_pages": self.num_pages,
            "type": self.type,
            "document_title": self.document_title,  # Added missing field
            "generated_questions": self.generated_questions,  # Added missing generated questions
        }

        # Use UUID for the point ID instead of entry_id which might be an invalid string
        point_id = str(uuid.uuid4())
        return point_id, data


