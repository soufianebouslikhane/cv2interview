"""Tests for API endpoints."""

import pytest
import json
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.api
class TestChatEndpoints:
    """Test cases for chat/agent endpoints."""
    
    def test_health_endpoint(self, client: TestClient):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data
    
    def test_root_endpoint(self, client: TestClient):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "CV2Interview API" in data["message"]
        assert "features" in data
        assert isinstance(data["features"], list)
    
    @patch('app.agent.cv_agent.enhanced_cv_agent.process_cv_comprehensive')
    def test_process_cv_endpoint_success(self, mock_process, client: TestClient, temp_file):
        """Test successful CV processing."""
        # Mock the comprehensive processing
        mock_process.return_value = {
            "processing_info": {
                "status": "completed",
                "processing_time": 2.5
            },
            "profile_analysis": {
                "personal_info": {"name": "John Doe"},
                "skills": {"technical": ["Python"]}
            },
            "career_recommendations": {
                "primary_role": "Software Engineer",
                "confidence_score": 0.85
            },
            "interview_questions": {
                "questions": [{"question": "Tell me about yourself"}],
                "total_questions": 1
            }
        }
        
        with open(temp_file, "rb") as f:
            response = client.post(
                "/api/v1/agent/process-cv",
                files={"file": ("test.pdf", f, "application/pdf")}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "profile_analysis" in data["data"]
        assert "career_recommendations" in data["data"]
    
    def test_process_cv_endpoint_no_file(self, client: TestClient):
        """Test CV processing endpoint without file."""
        response = client.post("/api/v1/agent/process-cv")
        assert response.status_code == 422  # Validation error
    
    def test_process_cv_endpoint_invalid_file_type(self, client: TestClient):
        """Test CV processing with invalid file type."""
        # Create a text file instead of PDF
        response = client.post(
            "/api/v1/agent/process-cv",
            files={"file": ("test.txt", b"text content", "text/plain")}
        )
        assert response.status_code == 400
        data = response.json()
        assert "Invalid file type" in data["detail"]
    
    @patch('app.agent.cv_agent.enhanced_cv_agent.quick_career_recommendation')
    def test_career_recommendation_endpoint(self, mock_recommend, client: TestClient, sample_cv_text):
        """Test career recommendation endpoint."""
        mock_recommend.return_value = {
            "success": True,
            "career_recommendation": {
                "primary_role": "Software Engineer",
                "confidence_score": 0.85
            }
        }
        
        response = client.post(
            "/api/v1/agent/career-recommendation",
            json={"cv_text": sample_cv_text}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "career_recommendation" in data["data"]
    
    @patch('app.agent.cv_agent.enhanced_cv_agent.generate_targeted_questions')
    def test_generate_questions_endpoint(self, mock_generate, client: TestClient, sample_profile_data):
        """Test question generation endpoint."""
        mock_generate.return_value = {
            "success": True,
            "questions": {
                "questions": [
                    {
                        "question": "Tell me about your experience",
                        "category": "General",
                        "difficulty": "Medium"
                    }
                ],
                "total_questions": 1
            }
        }
        
        response = client.post(
            "/api/v1/agent/generate-questions",
            json={
                "profile_data": json.dumps(sample_profile_data),
                "target_role": "Software Engineer",
                "difficulty_level": "intermediate"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "questions" in data["data"]

@pytest.mark.api
class TestDashboardEndpoints:
    """Test cases for dashboard endpoints."""
    
    @patch('app.services.analytics_service.AnalyticsService.get_dashboard_data')
    def test_dashboard_overview_endpoint(self, mock_get_data, client: TestClient):
        """Test dashboard overview endpoint."""
        mock_get_data.return_value = {
            "period": {"start_date": "2024-01-01", "end_date": "2024-01-31", "days": 30},
            "cv_analytics": {
                "total_cvs_processed": 100,
                "successful_analyses": 95,
                "success_rate": 95.0,
                "average_processing_time": 2.5,
                "file_types": {"pdf": 80, "docx": 20}
            },
            "interview_analytics": {
                "total_interview_sessions": 50,
                "average_questions_per_session": 15.0,
                "completion_rate": 85.0
            },
            "summary": {
                "total_processed": 100,
                "success_rate": 95.0,
                "health_score": 90.0
            }
        }
        
        response = client.get("/api/v1/dashboard/overview")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "cv_analytics" in data["data"]
        assert "interview_analytics" in data["data"]
    
    def test_dashboard_overview_with_params(self, client: TestClient):
        """Test dashboard overview with query parameters."""
        with patch('app.services.analytics_service.AnalyticsService.get_dashboard_data') as mock_get_data:
            mock_get_data.return_value = {"test": "data"}
            
            response = client.get("/api/v1/dashboard/overview?days=7&user_id=test-user")
            assert response.status_code == 200
            
            # Verify the service was called with correct parameters
            mock_get_data.assert_called_once()
            args, kwargs = mock_get_data.call_args
            assert kwargs.get("days") == 7
            assert kwargs.get("user_id") == "test-user"
    
    @patch('app.services.analytics_service.AnalyticsService.get_skill_analytics')
    def test_skills_analytics_endpoint(self, mock_get_skills, client: TestClient):
        """Test skills analytics endpoint."""
        mock_get_skills.return_value = {
            "total_unique_skills": 150,
            "total_skill_mentions": 500,
            "top_skills": [
                {"skill": "Python", "frequency": 50},
                {"skill": "JavaScript", "frequency": 40}
            ],
            "skill_categories": {
                "technical": {"python": 50, "javascript": 40},
                "soft_skills": {"communication": 30}
            }
        }
        
        response = client.get("/api/v1/dashboard/skills-analytics")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "total_unique_skills" in data["data"]
        assert "top_skills" in data["data"]
    
    @patch('app.services.analytics_service.AnalyticsService.get_career_analytics')
    def test_career_analytics_endpoint(self, mock_get_career, client: TestClient):
        """Test career analytics endpoint."""
        mock_get_career.return_value = {
            "total_recommendations": 100,
            "unique_roles": 25,
            "average_confidence_score": 0.78,
            "top_recommended_roles": [
                {"role": "Software Engineer", "frequency": 30},
                {"role": "Data Scientist", "frequency": 20}
            ]
        }
        
        response = client.get("/api/v1/dashboard/career-analytics")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "total_recommendations" in data["data"]
        assert "top_recommended_roles" in data["data"]
    
    def test_system_health_endpoint(self, client: TestClient):
        """Test system health endpoint."""
        with patch('app.services.analytics_service.AnalyticsService.get_dashboard_data') as mock_get_data:
            mock_get_data.return_value = {
                "summary": {
                    "health_score": 85.0,
                    "total_processed": 100,
                    "success_rate": 95.0
                }
            }
            
            response = client.get("/api/v1/dashboard/health")
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] is True
            assert "status" in data["data"]
            assert "health_score" in data["data"]

@pytest.mark.api
class TestErrorHandling:
    """Test error handling in API endpoints."""
    
    def test_404_endpoint(self, client: TestClient):
        """Test 404 error handling."""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client: TestClient):
        """Test method not allowed error."""
        response = client.delete("/health")  # Health endpoint only supports GET
        assert response.status_code == 405
    
    @patch('app.services.analytics_service.AnalyticsService.get_dashboard_data')
    def test_internal_server_error(self, mock_get_data, client: TestClient):
        """Test internal server error handling."""
        mock_get_data.side_effect = Exception("Database connection failed")
        
        response = client.get("/api/v1/dashboard/overview")
        assert response.status_code == 500
        
        data = response.json()
        assert "error" in data
    
    def test_validation_error(self, client: TestClient):
        """Test validation error handling."""
        # Send invalid data to career recommendation endpoint
        response = client.post(
            "/api/v1/agent/career-recommendation",
            json={"invalid_field": "value"}  # Missing required cv_text field
        )
        assert response.status_code == 422

@pytest.mark.integration
class TestDatabaseIntegration:
    """Integration tests with database."""
    
    async def test_cv_analysis_creation(self, db_session: AsyncSession, sample_user):
        """Test creating CV analysis in database."""
        from app.database.models import CVAnalysis
        
        cv_analysis = CVAnalysis(
            user_id=sample_user.id,
            original_filename="test.pdf",
            file_path="/tmp/test.pdf",
            file_size=1024,
            file_type="pdf",
            raw_text="Sample CV content",
            processing_status="completed"
        )
        
        db_session.add(cv_analysis)
        await db_session.commit()
        await db_session.refresh(cv_analysis)
        
        assert cv_analysis.id is not None
        assert cv_analysis.user_id == sample_user.id
        assert cv_analysis.processing_status == "completed"
    
    async def test_interview_session_creation(self, db_session: AsyncSession, sample_cv_analysis):
        """Test creating interview session in database."""
        from app.database.models import InterviewSession
        
        session = InterviewSession(
            user_id=sample_cv_analysis.user_id,
            cv_analysis_id=sample_cv_analysis.id,
            session_name="Test Interview",
            target_role="Software Engineer",
            questions=[
                {
                    "question": "Tell me about yourself",
                    "category": "General",
                    "difficulty": "Easy"
                }
            ],
            total_questions=1,
            completion_status="draft"
        )
        
        db_session.add(session)
        await db_session.commit()
        await db_session.refresh(session)
        
        assert session.id is not None
        assert session.cv_analysis_id == sample_cv_analysis.id
        assert len(session.questions) == 1
