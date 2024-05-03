from pydantic import BaseModel
from typing import Optional

class Proceso(BaseModel):
    _id: Optional[str]
    document_number: str
    page_number: Optional[int]
    total_pages: Optional[int]
    description: Optional[str]
    status: Optional[str]