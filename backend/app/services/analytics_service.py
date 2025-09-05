"""Analytics service for generating insights and dashboard data."""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_
from app.database.models import CVAnalysis, InterviewSession, CVAnalytics, SystemMetrics, User
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service for generating analytics and insights."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def generate_cv_insights(self, cv_analysis_id: str) -> Dict[str, Any]:
        """Generate comprehensive insights for a specific CV analysis."""
        try:
            # Get CV analysis data
            result = await self.db.execute(
                select(CVAnalysis).where(CVAnalysis.id == cv_analysis_id)
            )
            cv_analysis = result.scalar_one_or_none()
            
            if not cv_analysis:
                raise ValueError(f"CV analysis not found: {cv_analysis_id}")
            
            insights = {
                "cv_id": cv_analysis_id,
                "analysis_date": cv_analysis.created_at.isoformat(),
                "processing_metrics": {
                    "processing_time": cv_analysis.processing_time,
                    "file_size": cv_analysis.file_size,
                    "status": cv_analysis.processing_status
                },
                "profile_summary": await self._analyze_profile_data(cv_analysis),
                "skill_analysis": await self._analyze_skills(cv_analysis),
                "experience_analysis": await self._analyze_experience(cv_analysis),
                "career_recommendations": await self._analyze_career_recommendations(cv_analysis),
                "market_insights": await self._generate_market_insights(cv_analysis),
                "improvement_suggestions": await self._generate_improvement_suggestions(cv_analysis)
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating CV insights: {e}")
            raise
    
    async def get_dashboard_data(self, user_id: Optional[str] = None, days: int = 30) -> Dict[str, Any]:
        """Generate dashboard data for overview analytics."""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Base query filters
            filters = [CVAnalysis.created_at >= start_date]
            if user_id:
                filters.append(CVAnalysis.user_id == user_id)
            
            # Get CV analysis statistics
            cv_stats = await self._get_cv_statistics(filters)
            
            # Get interview session statistics
            interview_stats = await self._get_interview_statistics(filters, start_date)
            
            # Get skill trends
            skill_trends = await self._get_skill_trends(filters)
            
            # Get career recommendation trends
            career_trends = await self._get_career_trends(filters)
            
            # Get system performance metrics
            performance_metrics = await self._get_performance_metrics(start_date)
            
            dashboard_data = {
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days": days
                },
                "cv_analytics": cv_stats,
                "interview_analytics": interview_stats,
                "skill_trends": skill_trends,
                "career_trends": career_trends,
                "performance_metrics": performance_metrics,
                "summary": await self._generate_dashboard_summary(cv_stats, interview_stats)
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Error generating dashboard data: {e}")
            raise
    
    async def get_skill_analytics(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate detailed skill analytics."""
        try:
            filters = []
            if user_id:
                filters.append(CVAnalysis.user_id == user_id)
            
            # Get all CV analyses
            query = select(CVAnalysis).where(and_(*filters)) if filters else select(CVAnalysis)
            result = await self.db.execute(query)
            cv_analyses = result.scalars().all()
            
            # Aggregate skill data
            all_skills = []
            skill_categories = {}
            skill_frequency = {}
            
            for cv in cv_analyses:
                if cv.skills:
                    for skill in cv.skills:
                        all_skills.append(skill.lower())
                        skill_frequency[skill.lower()] = skill_frequency.get(skill.lower(), 0) + 1
                
                if cv.extracted_profile and isinstance(cv.extracted_profile, dict):
                    profile_skills = cv.extracted_profile.get('skills', {})
                    if isinstance(profile_skills, dict):
                        for category, skills in profile_skills.items():
                            if isinstance(skills, list):
                                if category not in skill_categories:
                                    skill_categories[category] = {}
                                for skill in skills:
                                    skill_key = skill.lower()
                                    skill_categories[category][skill_key] = skill_categories[category].get(skill_key, 0) + 1
            
            # Generate insights
            top_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)[:20]
            
            skill_analytics = {
                "total_unique_skills": len(skill_frequency),
                "total_skill_mentions": sum(skill_frequency.values()),
                "top_skills": [{"skill": skill, "frequency": freq} for skill, freq in top_skills],
                "skill_categories": skill_categories,
                "skill_distribution": await self._calculate_skill_distribution(skill_categories),
                "trending_skills": await self._identify_trending_skills(cv_analyses),
                "skill_gaps": await self._identify_skill_gaps(cv_analyses)
            }
            
            return skill_analytics
            
        except Exception as e:
            logger.error(f"Error generating skill analytics: {e}")
            raise
    
    async def get_career_analytics(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate career recommendation analytics."""
        try:
            filters = []
            if user_id:
                filters.append(CVAnalysis.user_id == user_id)
            
            query = select(CVAnalysis).where(and_(*filters)) if filters else select(CVAnalysis)
            result = await self.db.execute(query)
            cv_analyses = result.scalars().all()
            
            # Aggregate career data
            recommended_roles = {}
            confidence_scores = []
            industry_distribution = {}
            
            for cv in cv_analyses:
                if cv.recommended_roles:
                    for role_data in cv.recommended_roles:
                        if isinstance(role_data, dict):
                            role = role_data.get('primary_role', '')
                            if role:
                                recommended_roles[role] = recommended_roles.get(role, 0) + 1
                            
                            confidence = role_data.get('confidence_score', 0)
                            if confidence:
                                confidence_scores.append(float(confidence))
                
                if cv.career_confidence_score:
                    confidence_scores.append(cv.career_confidence_score)
            
            # Calculate statistics
            avg_confidence = np.mean(confidence_scores) if confidence_scores else 0
            top_roles = sorted(recommended_roles.items(), key=lambda x: x[1], reverse=True)[:15]
            
            career_analytics = {
                "total_recommendations": len(cv_analyses),
                "unique_roles": len(recommended_roles),
                "average_confidence_score": round(avg_confidence, 2),
                "top_recommended_roles": [{"role": role, "frequency": freq} for role, freq in top_roles],
                "confidence_distribution": await self._calculate_confidence_distribution(confidence_scores),
                "industry_insights": industry_distribution,
                "career_progression_patterns": await self._analyze_career_progression(cv_analyses)
            }
            
            return career_analytics
            
        except Exception as e:
            logger.error(f"Error generating career analytics: {e}")
            raise
    
    # Helper methods
    async def _analyze_profile_data(self, cv_analysis: CVAnalysis) -> Dict[str, Any]:
        """Analyze profile data for insights."""
        profile = cv_analysis.extracted_profile or {}
        
        return {
            "total_experience_years": profile.get('total_experience_years', 0),
            "education_level": len(profile.get('education', [])),
            "certifications_count": len(profile.get('certifications', [])),
            "languages_count": len(profile.get('languages', [])),
            "key_achievements_count": len(profile.get('key_achievements', []))
        }
    
    async def _analyze_skills(self, cv_analysis: CVAnalysis) -> Dict[str, Any]:
        """Analyze skills data."""
        skills = cv_analysis.skills or []
        profile_skills = cv_analysis.extracted_profile.get('skills', {}) if cv_analysis.extracted_profile else {}
        
        return {
            "total_skills": len(skills),
            "skill_categories": profile_skills,
            "technical_skills_count": len(profile_skills.get('technical', [])),
            "soft_skills_count": len(profile_skills.get('soft_skills', []))
        }
    
    async def _analyze_experience(self, cv_analysis: CVAnalysis) -> Dict[str, Any]:
        """Analyze experience data."""
        experience = cv_analysis.experience or []
        
        total_years = 0
        companies = set()
        roles = set()
        
        for exp in experience:
            if isinstance(exp, dict):
                years = exp.get('years', 0)
                if isinstance(years, (int, float)):
                    total_years += years
                
                company = exp.get('company', '')
                if company:
                    companies.add(company)
                
                position = exp.get('position', '')
                if position:
                    roles.add(position)
        
        return {
            "total_experience_years": total_years,
            "companies_count": len(companies),
            "unique_roles_count": len(roles),
            "average_tenure": total_years / len(experience) if experience else 0
        }
    
    async def _analyze_career_recommendations(self, cv_analysis: CVAnalysis) -> Dict[str, Any]:
        """Analyze career recommendations."""
        recommendations = cv_analysis.recommended_roles or []
        
        return {
            "recommendations_count": len(recommendations),
            "confidence_score": cv_analysis.career_confidence_score or 0,
            "primary_recommendations": recommendations[:3] if recommendations else []
        }
    
    async def _generate_market_insights(self, cv_analysis: CVAnalysis) -> Dict[str, Any]:
        """Generate market insights based on profile."""
        # This would typically integrate with external APIs for real market data
        return {
            "market_demand": "High",  # Placeholder
            "salary_range": {"min": 50000, "max": 80000, "currency": "USD"},
            "growth_potential": "Strong",
            "industry_trends": ["Remote work", "AI/ML skills in demand"]
        }
    
    async def _generate_improvement_suggestions(self, cv_analysis: CVAnalysis) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        profile = cv_analysis.extracted_profile or {}
        skills = profile.get('skills', {})
        
        # Check for common improvement areas
        if not skills.get('technical', []):
            suggestions.append("Consider adding more technical skills to your profile")
        
        if not profile.get('certifications', []):
            suggestions.append("Professional certifications could strengthen your profile")
        
        if len(profile.get('languages', [])) < 2:
            suggestions.append("Additional language skills could be valuable")
        
        return suggestions

    async def _get_cv_statistics(self, filters: List) -> Dict[str, Any]:
        """Get CV analysis statistics."""
        query = select(CVAnalysis).where(and_(*filters)) if filters else select(CVAnalysis)
        result = await self.db.execute(query)
        cv_analyses = result.scalars().all()

        total_cvs = len(cv_analyses)
        successful_analyses = len([cv for cv in cv_analyses if cv.processing_status == "completed"])
        avg_processing_time = np.mean([cv.processing_time for cv in cv_analyses if cv.processing_time]) if cv_analyses else 0

        return {
            "total_cvs_processed": total_cvs,
            "successful_analyses": successful_analyses,
            "success_rate": (successful_analyses / total_cvs * 100) if total_cvs > 0 else 0,
            "average_processing_time": round(avg_processing_time, 2),
            "file_types": self._get_file_type_distribution(cv_analyses)
        }

    async def _get_interview_statistics(self, filters: List, start_date: datetime) -> Dict[str, Any]:
        """Get interview session statistics."""
        # Get interview sessions for the period
        interview_query = select(InterviewSession).where(InterviewSession.created_at >= start_date)
        if filters:
            # Join with CVAnalysis to apply user filters
            interview_query = interview_query.join(CVAnalysis).where(and_(*filters))

        result = await self.db.execute(interview_query)
        sessions = result.scalars().all()

        total_sessions = len(sessions)
        avg_questions = np.mean([s.total_questions for s in sessions if s.total_questions]) if sessions else 0
        avg_duration = np.mean([s.estimated_duration for s in sessions if s.estimated_duration]) if sessions else 0

        return {
            "total_interview_sessions": total_sessions,
            "average_questions_per_session": round(avg_questions, 1),
            "average_estimated_duration": round(avg_duration, 1),
            "difficulty_distribution": self._get_difficulty_distribution(sessions),
            "completion_rate": self._calculate_completion_rate(sessions)
        }

    async def _get_skill_trends(self, filters: List) -> Dict[str, Any]:
        """Get skill trends over time."""
        query = select(CVAnalysis).where(and_(*filters)) if filters else select(CVAnalysis)
        result = await self.db.execute(query)
        cv_analyses = result.scalars().all()

        # Group by month and analyze skill trends
        monthly_skills = {}
        for cv in cv_analyses:
            month_key = cv.created_at.strftime("%Y-%m")
            if month_key not in monthly_skills:
                monthly_skills[month_key] = {}

            if cv.skills:
                for skill in cv.skills:
                    skill_lower = skill.lower()
                    monthly_skills[month_key][skill_lower] = monthly_skills[month_key].get(skill_lower, 0) + 1

        return {
            "monthly_trends": monthly_skills,
            "trending_up": self._identify_trending_skills_up(monthly_skills),
            "trending_down": self._identify_trending_skills_down(monthly_skills)
        }

    async def _get_career_trends(self, filters: List) -> Dict[str, Any]:
        """Get career recommendation trends."""
        query = select(CVAnalysis).where(and_(*filters)) if filters else select(CVAnalysis)
        result = await self.db.execute(query)
        cv_analyses = result.scalars().all()

        role_trends = {}
        for cv in cv_analyses:
            month_key = cv.created_at.strftime("%Y-%m")
            if month_key not in role_trends:
                role_trends[month_key] = {}

            if cv.recommended_roles:
                for role_data in cv.recommended_roles:
                    if isinstance(role_data, dict):
                        role = role_data.get('primary_role', '')
                        if role:
                            role_trends[month_key][role] = role_trends[month_key].get(role, 0) + 1

        return {
            "monthly_role_trends": role_trends,
            "popular_roles": self._get_popular_roles(role_trends),
            "emerging_roles": self._identify_emerging_roles(role_trends)
        }

    async def _get_performance_metrics(self, start_date: datetime) -> Dict[str, Any]:
        """Get system performance metrics."""
        query = select(SystemMetrics).where(SystemMetrics.recorded_at >= start_date)
        result = await self.db.execute(query)
        metrics = result.scalars().all()

        # Group metrics by type
        metric_groups = {}
        for metric in metrics:
            if metric.metric_name not in metric_groups:
                metric_groups[metric.metric_name] = []
            metric_groups[metric.metric_name].append(metric.metric_value)

        # Calculate statistics for each metric
        performance_stats = {}
        for metric_name, values in metric_groups.items():
            performance_stats[metric_name] = {
                "average": round(np.mean(values), 2),
                "min": round(min(values), 2),
                "max": round(max(values), 2),
                "count": len(values)
            }

        return performance_stats

    async def _generate_dashboard_summary(self, cv_stats: Dict, interview_stats: Dict) -> Dict[str, Any]:
        """Generate summary statistics for dashboard."""
        return {
            "total_processed": cv_stats.get("total_cvs_processed", 0),
            "success_rate": cv_stats.get("success_rate", 0),
            "total_interviews": interview_stats.get("total_interview_sessions", 0),
            "avg_processing_time": cv_stats.get("average_processing_time", 0),
            "health_score": self._calculate_system_health_score(cv_stats, interview_stats)
        }

    def _get_file_type_distribution(self, cv_analyses: List[CVAnalysis]) -> Dict[str, int]:
        """Get distribution of file types."""
        file_types = {}
        for cv in cv_analyses:
            file_type = cv.file_type or "unknown"
            file_types[file_type] = file_types.get(file_type, 0) + 1
        return file_types

    def _get_difficulty_distribution(self, sessions: List[InterviewSession]) -> Dict[str, int]:
        """Get distribution of interview difficulty levels."""
        difficulty_dist = {}
        for session in sessions:
            difficulty = session.difficulty_level or "intermediate"
            difficulty_dist[difficulty] = difficulty_dist.get(difficulty, 0) + 1
        return difficulty_dist

    def _calculate_completion_rate(self, sessions: List[InterviewSession]) -> float:
        """Calculate interview completion rate."""
        if not sessions:
            return 0.0

        completed = len([s for s in sessions if s.completion_status == "completed"])
        return round((completed / len(sessions)) * 100, 2)

    def _calculate_system_health_score(self, cv_stats: Dict, interview_stats: Dict) -> float:
        """Calculate overall system health score."""
        success_rate = cv_stats.get("success_rate", 0)
        completion_rate = interview_stats.get("completion_rate", 0)

        # Simple health score calculation
        health_score = (success_rate + completion_rate) / 2
        return round(health_score, 1)
