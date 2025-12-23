from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AnalysisResult(BaseModel):
    """Schema for storing analysis results in MongoDB"""
    match_score: float = Field(..., ge=0, le=100)
    missing_keywords: List[str]
    matched_keywords: List[str]
    summary: str
    resume_filename: str
    job_description: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "match_score": 78.5,
                "missing_keywords": ["Docker", "Kubernetes"],
                "matched_keywords": ["Python", "React", "FastAPI"],
                "summary": "Strong match with room for improvement",
                "resume_filename": "john_doe_resume.pdf",
                "job_description": "We are looking for...",
                "timestamp": "2024-12-23T10:30:00"
            }
        }

class AnalysisResponse(BaseModel):
    """API Response model"""
    success: bool
    match_score: float
    missing_keywords: List[str]
    matched_keywords: List[str]
    summary: str
    analysis_id: Optional[str] = None