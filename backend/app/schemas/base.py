# schemas/base.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union, Dict, Any
from datetime import datetime

class Source(BaseModel):
    source: str
    text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatHistory(BaseModel):
    prompt: str
    response: str

    def to_internal(self) -> Dict[str, str]:
        return {
            "role": "user",
            "content": self.prompt
        } if self.response is None else [
            {"role": "user", "content": self.prompt},
            {"role": "assistant", "content": self.response}
        ]
    
    
    