"""Database models for CV2Interview application."""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, Float, Integer, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .connection import Base
import uuid

class User(Base):
    """User model for authentication and tracking."""
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    cv_analyses: Mapped[List["CVAnalysis"]] = relationship("CVAnalysis", back_populates="user")
    interview_sessions: Mapped[List["InterviewSession"]] = relationship("InterviewSession", back_populates="user")

class CVAnalysis(Base):
    """CV analysis results and metadata."""
    __tablename__ = "cv_analyses"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    
    # File information
    original_filename: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    file_size: Mapped[int] = mapped_column(Integer)
    file_type: Mapped[str] = mapped_column(String(50))
    
    # Extracted content
    raw_text: Mapped[str] = mapped_column(Text)
    processed_text: Mapped[Optional[str]] = mapped_column(Text)
    
    # Analysis results
    extracted_profile: Mapped[Optional[dict]] = mapped_column(JSON)
    skills: Mapped[Optional[List[str]]] = mapped_column(JSON)
    experience: Mapped[Optional[List[dict]]] = mapped_column(JSON)
    education: Mapped[Optional[List[dict]]] = mapped_column(JSON)
    
    # Career recommendations
    recommended_roles: Mapped[Optional[List[dict]]] = mapped_column(JSON)
    career_confidence_score: Mapped[Optional[float]] = mapped_column(Float)
    
    # Processing metadata
    processing_time: Mapped[Optional[float]] = mapped_column(Float)
    ai_model_used: Mapped[Optional[str]] = mapped_column(String(100))
    processing_status: Mapped[str] = mapped_column(String(50), default="pending")
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="cv_analyses")
    interview_sessions: Mapped[List["InterviewSession"]] = relationship("InterviewSession", back_populates="cv_analysis")
    analytics: Mapped[List["CVAnalytics"]] = relationship("CVAnalytics", back_populates="cv_analysis")

class InterviewSession(Base):
    """Interview question generation and session tracking."""
    __tablename__ = "interview_sessions"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    cv_analysis_id: Mapped[str] = mapped_column(String(36), ForeignKey("cv_analyses.id"), index=True)
    
    # Session information
    session_name: Mapped[Optional[str]] = mapped_column(String(255))
    target_role: Mapped[Optional[str]] = mapped_column(String(255))
    difficulty_level: Mapped[str] = mapped_column(String(50), default="intermediate")
    
    # Generated questions
    questions: Mapped[List[dict]] = mapped_column(JSON)
    question_categories: Mapped[Optional[List[str]]] = mapped_column(JSON)
    total_questions: Mapped[int] = mapped_column(Integer, default=0)
    
    # Session metrics
    estimated_duration: Mapped[Optional[int]] = mapped_column(Integer)  # in minutes
    completion_status: Mapped[str] = mapped_column(String(50), default="draft")
    
    # AI generation metadata
    generation_time: Mapped[Optional[float]] = mapped_column(Float)
    ai_model_used: Mapped[Optional[str]] = mapped_column(String(100))
    prompt_version: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="interview_sessions")
    cv_analysis: Mapped["CVAnalysis"] = relationship("CVAnalysis", back_populates="interview_sessions")

class CVAnalytics(Base):
    """Analytics and insights from CV analysis."""
    __tablename__ = "cv_analytics"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cv_analysis_id: Mapped[str] = mapped_column(String(36), ForeignKey("cv_analyses.id"), index=True)
    
    # Skill analysis
    skill_categories: Mapped[Optional[dict]] = mapped_column(JSON)
    skill_levels: Mapped[Optional[dict]] = mapped_column(JSON)
    skill_gaps: Mapped[Optional[List[str]]] = mapped_column(JSON)
    
    # Experience analysis
    total_experience_years: Mapped[Optional[float]] = mapped_column(Float)
    experience_distribution: Mapped[Optional[dict]] = mapped_column(JSON)
    career_progression: Mapped[Optional[dict]] = mapped_column(JSON)
    
    # Education analysis
    education_level: Mapped[Optional[str]] = mapped_column(String(100))
    relevant_certifications: Mapped[Optional[List[str]]] = mapped_column(JSON)
    
    # Market insights
    salary_estimate: Mapped[Optional[dict]] = mapped_column(JSON)
    market_demand_score: Mapped[Optional[float]] = mapped_column(Float)
    industry_fit_scores: Mapped[Optional[dict]] = mapped_column(JSON)
    
    # Improvement suggestions
    skill_recommendations: Mapped[Optional[List[str]]] = mapped_column(JSON)
    career_path_suggestions: Mapped[Optional[List[dict]]] = mapped_column(JSON)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    cv_analysis: Mapped["CVAnalysis"] = relationship("CVAnalysis", back_populates="analytics")

class SystemMetrics(Base):
    """System performance and usage metrics."""
    __tablename__ = "system_metrics"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Metric information
    metric_name: Mapped[str] = mapped_column(String(100), index=True)
    metric_value: Mapped[float] = mapped_column(Float)
    metric_unit: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Context
    endpoint: Mapped[Optional[str]] = mapped_column(String(255))
    user_id: Mapped[Optional[str]] = mapped_column(String(36))
    session_id: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Additional data
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)
    
    # Timestamp
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
