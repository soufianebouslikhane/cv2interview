from pydantic import BaseModel
from typing import List, Optional

class AgentRequest(BaseModel):
    instruction: str
    file_paths: Optional[List[str]] = None

class Profile(BaseModel):
    skills: List[str]
    experience: List[str]
    education: List[str]

class QuestionOutput(BaseModel):
    questions: List[str]

class CVProcessingResult(BaseModel):
    profile: Profile
    recommended_role: Optional[str]
    generated_questions: Optional[List[str]]
