"""Tests for analytics service."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.analytics_service import AnalyticsService
from app.database.models import CVAnalysis, InterviewSession, CVAnalytics, SystemMetrics

@pytest.mark.database
class TestAnalyticsService:
    """Test cases for AnalyticsService."""
    
    async def test_generate_cv_insights(self, db_session: AsyncSession, sample_cv_analysis):
        """Test generating CV insights."""
        analytics_service = AnalyticsService(db_session)
        
        insights = await analytics_service.generate_cv_insights(sample_cv_analysis.id)
        
        assert insights["cv_id"] == sample_cv_analysis.id
        assert "analysis_date" in insights
        assert "processing_metrics" in insights
        assert "profile_summary" in insights
        assert "skill_analysis" in insights
    
    async def test_generate_cv_insights_not_found(self, db_session: AsyncSession):
        """Test generating insights for non-existent CV."""
        analytics_service = AnalyticsService(db_session)
        
        with pytest.raises(ValueError, match="CV analysis not found"):
            await analytics_service.generate_cv_insights("non-existent-id")
    
    async def test_get_dashboard_data(self, db_session: AsyncSession, sample_cv_analysis):
        """Test getting dashboard data."""
        # Create some test data
        interview_session = InterviewSession(
            user_id=sample_cv_analysis.user_id,
            cv_analysis_id=sample_cv_analysis.id,
            questions=[{"question": "Test question"}],
            total_questions=1,
            estimated_duration=30,
            difficulty_level="medium",
            completion_status="completed"
        )
        db_session.add(interview_session)
        await db_session.commit()
        
        analytics_service = AnalyticsService(db_session)
        dashboard_data = await analytics_service.get_dashboard_data(days=30)
        
        assert "period" in dashboard_data
        assert "cv_analytics" in dashboard_data
        assert "interview_analytics" in dashboard_data
        assert "summary" in dashboard_data
        
        # Check CV analytics
        cv_analytics = dashboard_data["cv_analytics"]
        assert cv_analytics["total_cvs_processed"] >= 1
        assert cv_analytics["successful_analyses"] >= 1
        assert cv_analytics["success_rate"] > 0
        
        # Check interview analytics
        interview_analytics = dashboard_data["interview_analytics"]
        assert interview_analytics["total_interview_sessions"] >= 1
    
    async def test_get_dashboard_data_with_user_filter(self, db_session: AsyncSession, sample_cv_analysis):
        """Test getting dashboard data filtered by user."""
        analytics_service = AnalyticsService(db_session)
        
        # Get data for specific user
        dashboard_data = await analytics_service.get_dashboard_data(
            user_id=sample_cv_analysis.user_id,
            days=30
        )
        
        assert "cv_analytics" in dashboard_data
        cv_analytics = dashboard_data["cv_analytics"]
        assert cv_analytics["total_cvs_processed"] >= 1
    
    async def test_get_skill_analytics(self, db_session: AsyncSession, sample_cv_analysis):
        """Test getting skill analytics."""
        analytics_service = AnalyticsService(db_session)
        
        skill_analytics = await analytics_service.get_skill_analytics()
        
        assert "total_unique_skills" in skill_analytics
        assert "total_skill_mentions" in skill_analytics
        assert "top_skills" in skill_analytics
        assert "skill_categories" in skill_analytics
        assert "trending_skills" in skill_analytics
        assert "skill_gaps" in skill_analytics
        
        # Should have at least the skills from our sample CV
        assert skill_analytics["total_unique_skills"] >= 3  # Python, JavaScript, React
    
    async def test_get_career_analytics(self, db_session: AsyncSession, sample_cv_analysis):
        """Test getting career analytics."""
        # Add career recommendations to the CV analysis
        sample_cv_analysis.recommended_roles = [
            {
                "primary_role": "Software Engineer",
                "confidence_score": 0.85
            }
        ]
        sample_cv_analysis.career_confidence_score = 0.85
        await db_session.commit()
        
        analytics_service = AnalyticsService(db_session)
        career_analytics = await analytics_service.get_career_analytics()
        
        assert "total_recommendations" in career_analytics
        assert "unique_roles" in career_analytics
        assert "average_confidence_score" in career_analytics
        assert "top_recommended_roles" in career_analytics
        assert "confidence_distribution" in career_analytics
        
        # Should have at least one recommendation
        assert career_analytics["total_recommendations"] >= 1
        assert career_analytics["average_confidence_score"] > 0
    
    async def test_analyze_profile_data(self, db_session: AsyncSession, sample_cv_analysis):
        """Test profile data analysis."""
        analytics_service = AnalyticsService(db_session)
        
        profile_analysis = await analytics_service._analyze_profile_data(sample_cv_analysis)
        
        assert "total_experience_years" in profile_analysis
        assert "education_level" in profile_analysis
        assert "certifications_count" in profile_analysis
        assert "languages_count" in profile_analysis
        assert "key_achievements_count" in profile_analysis
    
    async def test_analyze_skills(self, db_session: AsyncSession, sample_cv_analysis):
        """Test skills analysis."""
        analytics_service = AnalyticsService(db_session)
        
        skills_analysis = await analytics_service._analyze_skills(sample_cv_analysis)
        
        assert "total_skills" in skills_analysis
        assert "skill_categories" in skills_analysis
        assert "technical_skills_count" in skills_analysis
        assert "soft_skills_count" in skills_analysis
        
        # Should count the skills from our sample CV
        assert skills_analysis["total_skills"] == 3  # Python, JavaScript, React
    
    async def test_analyze_experience(self, db_session: AsyncSession, sample_cv_analysis):
        """Test experience analysis."""
        analytics_service = AnalyticsService(db_session)
        
        experience_analysis = await analytics_service._analyze_experience(sample_cv_analysis)
        
        assert "total_experience_years" in experience_analysis
        assert "companies_count" in experience_analysis
        assert "unique_roles_count" in experience_analysis
        assert "average_tenure" in experience_analysis
    
    async def test_get_cv_statistics(self, db_session: AsyncSession, sample_cv_analysis):
        """Test CV statistics calculation."""
        analytics_service = AnalyticsService(db_session)
        
        # Create filters for recent data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        filters = [CVAnalysis.created_at >= start_date]
        
        cv_stats = await analytics_service._get_cv_statistics(filters)
        
        assert "total_cvs_processed" in cv_stats
        assert "successful_analyses" in cv_stats
        assert "success_rate" in cv_stats
        assert "average_processing_time" in cv_stats
        assert "file_types" in cv_stats
        
        # Should have at least our sample CV
        assert cv_stats["total_cvs_processed"] >= 1
        assert cv_stats["successful_analyses"] >= 1
    
    async def test_get_interview_statistics(self, db_session: AsyncSession, sample_cv_analysis):
        """Test interview statistics calculation."""
        # Create an interview session
        interview_session = InterviewSession(
            user_id=sample_cv_analysis.user_id,
            cv_analysis_id=sample_cv_analysis.id,
            questions=[{"question": "Test question"}],
            total_questions=5,
            estimated_duration=45,
            difficulty_level="intermediate",
            completion_status="completed"
        )
        db_session.add(interview_session)
        await db_session.commit()
        
        analytics_service = AnalyticsService(db_session)
        
        # Create filters
        start_date = datetime.utcnow() - timedelta(days=30)
        filters = [CVAnalysis.created_at >= start_date]
        
        interview_stats = await analytics_service._get_interview_statistics(filters, start_date)
        
        assert "total_interview_sessions" in interview_stats
        assert "average_questions_per_session" in interview_stats
        assert "average_estimated_duration" in interview_stats
        assert "difficulty_distribution" in interview_stats
        assert "completion_rate" in interview_stats
        
        # Should have our interview session
        assert interview_stats["total_interview_sessions"] >= 1
        assert interview_stats["average_questions_per_session"] > 0
    
    async def test_get_performance_metrics(self, db_session: AsyncSession):
        """Test performance metrics retrieval."""
        # Create some system metrics
        metrics = [
            SystemMetrics(
                metric_name="response_time",
                metric_value=0.5,
                metric_unit="seconds",
                endpoint="/api/v1/agent/process-cv"
            ),
            SystemMetrics(
                metric_name="response_time",
                metric_value=0.3,
                metric_unit="seconds",
                endpoint="/api/v1/agent/process-cv"
            ),
            SystemMetrics(
                metric_name="memory_usage",
                metric_value=75.5,
                metric_unit="percent"
            )
        ]
        
        for metric in metrics:
            db_session.add(metric)
        await db_session.commit()
        
        analytics_service = AnalyticsService(db_session)
        start_date = datetime.utcnow() - timedelta(days=1)
        
        performance_metrics = await analytics_service._get_performance_metrics(start_date)
        
        assert "response_time" in performance_metrics
        assert "memory_usage" in performance_metrics
        
        # Check response time statistics
        response_time_stats = performance_metrics["response_time"]
        assert "average" in response_time_stats
        assert "min" in response_time_stats
        assert "max" in response_time_stats
        assert "count" in response_time_stats
        
        assert response_time_stats["count"] == 2
        assert response_time_stats["average"] == 0.4  # (0.5 + 0.3) / 2
    
    async def test_generate_dashboard_summary(self, db_session: AsyncSession):
        """Test dashboard summary generation."""
        analytics_service = AnalyticsService(db_session)
        
        cv_stats = {
            "total_cvs_processed": 100,
            "success_rate": 95.0,
            "average_processing_time": 2.5
        }
        
        interview_stats = {
            "total_interview_sessions": 50,
            "completion_rate": 85.0
        }
        
        summary = await analytics_service._generate_dashboard_summary(cv_stats, interview_stats)
        
        assert "total_processed" in summary
        assert "success_rate" in summary
        assert "total_interviews" in summary
        assert "avg_processing_time" in summary
        assert "health_score" in summary
        
        assert summary["total_processed"] == 100
        assert summary["success_rate"] == 95.0
        assert summary["total_interviews"] == 50
        assert summary["health_score"] == 90.0  # (95 + 85) / 2
    
    def test_calculate_profile_completeness(self, db_session: AsyncSession):
        """Test profile completeness calculation."""
        analytics_service = AnalyticsService(db_session)
        
        # Complete profile
        complete_profile = {
            "personal_info": {"name": "John Doe"},
            "skills": {"technical": ["Python"]},
            "experience": [{"company": "TechCorp"}],
            "education": [{"degree": "BS"}]
        }
        
        completeness = analytics_service._calculate_profile_completeness(complete_profile)
        assert completeness == 100.0
        
        # Partial profile
        partial_profile = {
            "personal_info": {"name": "John Doe"},
            "skills": {"technical": ["Python"]}
        }
        
        completeness = analytics_service._calculate_profile_completeness(partial_profile)
        assert completeness == 50.0  # 2 out of 4 required fields
        
        # Invalid profile
        completeness = analytics_service._calculate_profile_completeness("not a dict")
        assert completeness == 0.0
    
    def test_calculate_skill_diversity(self, db_session: AsyncSession):
        """Test skill diversity calculation."""
        analytics_service = AnalyticsService(db_session)
        
        profile_with_skills = {
            "skills": {
                "technical": ["Python", "JavaScript"],
                "soft_skills": ["Communication"],
                "frameworks": ["React", "Django"]
            }
        }
        
        diversity = analytics_service._calculate_skill_diversity(profile_with_skills)
        assert diversity == 5  # 2 + 1 + 2 skills
        
        # Profile without skills
        profile_without_skills = {"personal_info": {"name": "John"}}
        diversity = analytics_service._calculate_skill_diversity(profile_without_skills)
        assert diversity == 0
    
    def test_assess_experience_level(self, db_session: AsyncSession):
        """Test experience level assessment."""
        analytics_service = AnalyticsService(db_session)
        
        # Test different experience levels
        assert analytics_service._assess_experience_level({"total_experience_years": 1}) == "entry"
        assert analytics_service._assess_experience_level({"total_experience_years": 3}) == "junior"
        assert analytics_service._assess_experience_level({"total_experience_years": 7}) == "mid"
        assert analytics_service._assess_experience_level({"total_experience_years": 12}) == "senior"
        assert analytics_service._assess_experience_level("not a dict") == "unknown"
