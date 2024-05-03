from pydantic import BaseModel
from typing import Optional, List

class Caus(BaseModel):
    entryDate: Optional[str]
    numProcess: Optional[str]
    actionInfraction: Optional[str]
    idMovement: Optional[str]

class Causa(BaseModel):  
    numDocument: Optional[str]
    causas: List[Caus]