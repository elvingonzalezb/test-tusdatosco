from pydantic import BaseModel, Field
from typing import Optional
import passlib.hash as _hash
from uuid import UUID

class User(BaseModel):
    _id: Optional[str]
    email: str
    username: str
    #hashed_password: str
    password: str
    status: str
    
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    

class UserOut(BaseModel):
    id: UUID
    email: str


class SystemUser(UserOut):
    password: str
    
class UserToken(BaseModel):
    token: str = Field(..., description="user toekn")