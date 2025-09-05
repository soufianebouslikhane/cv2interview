"""Pydantic schemas for dashboard API responses."""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

class PeriodInfo(BaseModel):
    """Time period information."""
    start_date: str
    end_date: str
    days: int

class CVAnalyticsData(BaseModel):
    """CV analytics data structure."""
    total_cvs_processed: int
    successful_analyses: int
    success_rate: float
    average_processing_time: float
    file_types: Dict[str, int]

class InterviewAnalyticsData(BaseModel):
    """Interview analytics data structure."""
    total_interview_sessions: int
    average_questions_per_session: float
    average_estimated_duration: float
    difficulty_distribution: Dict[str, int]
    completion_rate: float

class SkillTrendsData(BaseModel):
    """Skill trends data structure."""
    monthly_trends: Dict[str, Dict[str, int]]
    trending_up: List[str]
    trending_down: List[str]

class CareerTrendsData(BaseModel):
    """Career trends data structure."""
    monthly_role_trends: Dict[str, Dict[str, int]]
    popular_roles: List[Dict[str, Any]]
    emerging_roles: List[str]

class PerformanceMetrics(BaseModel):
    """System performance metrics."""
    response_time: Optional[Dict[str, float]] = None
    throughput: Optional[Dict[str, float]] = None
    error_rate: Optional[Dict[str, float]] = None
    cpu_usage: Optional[Dict[str, float]] = None
    memory_usage: Optional[Dict[str, float]] = None

class DashboardSummary(BaseModel):
    """Dashboard summary statistics."""
    total_processed: int
    success_rate: float
    total_interviews: int
    avg_processing_time: float
    health_score: float

class DashboardData(BaseModel):
    """Complete dashboard data structure."""
    period: PeriodInfo
    cv_analytics: CVAnalyticsData
    interview_analytics: InterviewAnalyticsData
    skill_trends: SkillTrendsData
    career_trends: CareerTrendsData
    performance_metrics: PerformanceMetrics
    summary: DashboardSummary

class DashboardResponse(BaseModel):
    """Dashboard API response."""
    success: bool
    data: DashboardData
    message: str

class ProfileSummary(BaseModel):
    """Profile summary data."""
    total_experience_years: float
    education_level: int
    certifications_count: int
    languages_count: int
    key_achievements_count: int

class SkillAnalysis(BaseModel):
    """Skill analysis data."""
    total_skills: int
    skill_categories: Dict[str, List[str]]
    technical_skills_count: int
    soft_skills_count: int

class ExperienceAnalysis(BaseModel):
    """Experience analysis data."""
    total_experience_years: float
    companies_count: int
    unique_roles_count: int
    average_tenure: float

class CareerRecommendationAnalysis(BaseModel):
    """Career recommendation analysis."""
    recommendations_count: int
    confidence_score: float
    primary_recommendations: List[Dict[str, Any]]

class MarketInsights(BaseModel):
    """Market insights data."""
    market_demand: str
    salary_range: Dict[str, Any]
    growth_potential: str
    industry_trends: List[str]

class ProcessingMetrics(BaseModel):
    """Processing metrics data."""
    processing_time: Optional[float]
    file_size: Optional[int]
    status: str

class CVInsightsData(BaseModel):
    """CV insights data structure."""
    cv_id: str
    analysis_date: str
    processing_metrics: ProcessingMetrics
    profile_summary: ProfileSummary
    skill_analysis: SkillAnalysis
    experience_analysis: ExperienceAnalysis
    career_recommendations: CareerRecommendationAnalysis
    market_insights: MarketInsights
    improvement_suggestions: List[str]

class CVInsightsResponse(BaseModel):
    """CV insights API response."""
    success: bool
    data: CVInsightsData
    message: str

class SkillFrequency(BaseModel):
    """Skill frequency data."""
    skill: str
    frequency: int

class SkillAnalyticsData(BaseModel):
    """Skills analytics data structure."""
    total_unique_skills: int
    total_skill_mentions: int
    top_skills: List[SkillFrequency]
    skill_categories: Dict[str, Dict[str, int]]
    skill_distribution: Dict[str, Any]
    trending_skills: List[str]
    skill_gaps: List[str]

class SkillAnalyticsResponse(BaseModel):
    """Skills analytics API response."""
    success: bool
    data: SkillAnalyticsData
    message: str

class RoleFrequency(BaseModel):
    """Role frequency data."""
    role: str
    frequency: int

class ConfidenceDistribution(BaseModel):
    """Confidence score distribution."""
    high: int = Field(description="Confidence scores 0.8-1.0")
    medium: int = Field(description="Confidence scores 0.5-0.79")
    low: int = Field(description="Confidence scores 0.0-0.49")

class CareerProgressionPattern(BaseModel):
    """Career progression pattern."""
    pattern_type: str
    frequency: int
    description: str

class CareerAnalyticsData(BaseModel):
    """Career analytics data structure."""
    total_recommendations: int
    unique_roles: int
    average_confidence_score: float
    top_recommended_roles: List[RoleFrequency]
    confidence_distribution: ConfidenceDistribution
    industry_insights: Dict[str, Any]
    career_progression_patterns: List[CareerProgressionPattern]

class CareerAnalyticsResponse(BaseModel):
    """Career analytics API response."""
    success: bool
    data: CareerAnalyticsData
    message: str

class APIResponse(BaseModel):
    """Generic API response."""
    success: bool
    data: Dict[str, Any]
    message: str

class HealthStatus(BaseModel):
    """System health status."""
    status: str = Field(description="excellent|good|fair|poor")
    health_score: float
    metrics: DashboardSummary
    timestamp: str

class HealthResponse(BaseModel):
    """Health check API response."""
    success: bool
    data: HealthStatus
    message: str

class TrendData(BaseModel):
    """Trend data structure."""
    period_days: int
    trends: Dict[str, Any]
    limit: int

class TrendResponse(BaseModel):
    """Trend API response."""
    success: bool
    data: TrendData
    message: str

class ExportParameters(BaseModel):
    """Export parameters."""
    format: str
    days: int
    user_id: Optional[str]

class ExportData(BaseModel):
    """Export data structure."""
    export_timestamp: str
    parameters: ExportParameters
    dashboard_data: DashboardData
    skill_analytics: SkillAnalyticsData
    career_analytics: CareerAnalyticsData

class ExportResponse(BaseModel):
    """Export API response."""
    success: bool
    data: ExportData
    message: str
    format: str
