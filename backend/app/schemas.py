from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Any
import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    level: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: 'UserOut'

class RecommendRequest(BaseModel):
    user_id: int
    limit: int = 5

class GradeRequest(BaseModel):
    user_id: int
    problem_id: str
    code: str

class GradeResult(BaseModel):
    passed: bool
    score: float
    feedback: Any

class ChatRequest(BaseModel):
    user_id: int
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: Optional[list] = None
