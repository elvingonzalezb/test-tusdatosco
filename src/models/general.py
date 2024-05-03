from pydantic import BaseModel
from typing import Optional

class General(BaseModel):
    _id: Optional[str]
    personType: str
    name: Optional[str]
    companyName: Optional[str]