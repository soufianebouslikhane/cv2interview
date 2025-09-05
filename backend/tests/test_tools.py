"""Tests for AI tools."""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from app.tools.profile_extractor import ProfileExtractorTool
from app.tools.career_recommender import CareerRecommenderTool
from app.tools.question_generator import QuestionGeneratorTool
from app.tools.pdf_tool import PDFConverterTool

class TestProfileExtractorTool:
    """Test cases for ProfileExtractorTool."""
    
    def test_init(self):
        """Test tool initialization."""
        tool = ProfileExtractorTool()
        assert tool.name == "enhanced_profile_extractor"
        assert "comprehensive" in tool.description.lower()
    
    @patch('app.tools.profile_extractor.genai')
    def test_run_success(self, mock_genai, sample_cv_text):
        """Test successful profile extraction."""
        # Mock the AI response
        mock_response = Mock()
        mock_response.text = json.dumps({
            "personal_info": {"name": "John Doe", "email": "john@example.com"},
            "skills": {"technical": ["Python", "JavaScript"]},
            "experience": [{"company": "TechCorp", "position": "Engineer"}],
            "education": [{"degree": "BS Computer Science"}],
            "certifications": [],
            "languages": [],
            "summary": "Software engineer with 5 years experience",
            "total_experience_years": 5.0,
            "key_achievements": ["Led team of 5 developers"]
        })
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        tool = ProfileExtractorTool()
        result = tool._run(sample_cv_text)
        
        # Verify the result is valid JSON
        parsed_result = json.loads(result)
        assert "personal_info" in parsed_result
        assert "skills" in parsed_result
        assert "experience" in parsed_result
        assert parsed_result["total_experience_years"] == 5.0
    
    @patch('app.tools.profile_extractor.genai')
    def test_run_with_invalid_json_response(self, mock_genai, sample_cv_text):
        """Test handling of invalid JSON response."""
        # Mock an invalid JSON response
        mock_response = Mock()
        mock_response.text = "This is not valid JSON"
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        tool = ProfileExtractorTool()
        result = tool._run(sample_cv_text)
        
        # Should return the original response as fallback
        assert result == "This is not valid JSON"
    
    @patch('app.tools.profile_extractor.genai')
    def test_run_with_exception(self, mock_genai, sample_cv_text):
        """Test handling of exceptions during processing."""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_genai.GenerativeModel.return_value = mock_model
        
        tool = ProfileExtractorTool()
        result = tool._run(sample_cv_text)
        
        assert "Error extracting profile" in result
        assert "API Error" in result
    
    def test_preprocess_text(self):
        """Test text preprocessing functionality."""
        tool = ProfileExtractorTool()
        
        # Test with messy text
        messy_text = "  Multiple   spaces\n\nand\n\nnewlines  "
        cleaned = tool._preprocess_text(messy_text)
        
        assert "Multiple spaces and newlines" in cleaned
        assert cleaned.strip() == cleaned  # No leading/trailing whitespace

class TestCareerRecommenderTool:
    """Test cases for CareerRecommenderTool."""
    
    def test_init(self):
        """Test tool initialization."""
        tool = CareerRecommenderTool()
        assert tool.name == "enhanced_career_recommender"
        assert "comprehensive" in tool.description.lower()
    
    @patch('app.tools.career_recommender.genai')
    def test_run_success(self, mock_genai, sample_profile_data):
        """Test successful career recommendation."""
        # Mock the AI response
        mock_response = Mock()
        mock_response.text = json.dumps({
            "primary_role": "Senior Software Engineer",
            "alternative_roles": ["Full Stack Developer", "Tech Lead"],
            "confidence_score": 0.85,
            "reasoning": "Strong technical background",
            "required_skills": ["Python", "System Design"],
            "skill_gaps": ["Machine Learning"],
            "salary_range": {"min": 80000, "max": 120000, "currency": "USD"},
            "growth_potential": "High",
            "industry_demand": "Very high"
        })
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        tool = CareerRecommenderTool()
        result = tool._run(json.dumps(sample_profile_data))
        
        # Verify the result is valid JSON
        parsed_result = json.loads(result)
        assert parsed_result["primary_role"] == "Senior Software Engineer"
        assert parsed_result["confidence_score"] == 0.85
        assert "alternative_roles" in parsed_result
    
    @patch('app.tools.career_recommender.genai')
    def test_run_with_exception(self, mock_genai):
        """Test handling of exceptions during processing."""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_genai.GenerativeModel.return_value = mock_model
        
        tool = CareerRecommenderTool()
        result = tool._run("sample profile")
        
        assert "Error while generating career recommendations" in result
        assert "API Error" in result

class TestQuestionGeneratorTool:
    """Test cases for QuestionGeneratorTool."""
    
    def test_init(self):
        """Test tool initialization."""
        tool = QuestionGeneratorTool()
        assert tool.name == "enhanced_question_generator"
        assert "personalized" in tool.description.lower()
    
    @patch('app.tools.question_generator.genai')
    def test_run_success(self, mock_genai, sample_profile_data):
        """Test successful question generation."""
        # Mock the AI response
        mock_response = Mock()
        mock_response.text = json.dumps({
            "questions": [
                {
                    "question": "Tell me about your leadership experience.",
                    "category": "Leadership",
                    "difficulty": "Medium",
                    "purpose": "Assess leadership skills",
                    "expected_answer_type": "Story/Example"
                },
                {
                    "question": "How do you approach system design?",
                    "category": "Technical Skills",
                    "difficulty": "Hard",
                    "purpose": "Evaluate technical depth",
                    "expected_answer_type": "Technical explanation"
                }
            ],
            "total_questions": 2,
            "estimated_duration": 30,
            "difficulty_distribution": {"Medium": 1, "Hard": 1},
            "category_distribution": {"Leadership": 1, "Technical Skills": 1}
        })
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        tool = QuestionGeneratorTool()
        result = tool._run(json.dumps(sample_profile_data), "Senior Engineer", "intermediate")
        
        # Verify the result is valid JSON
        parsed_result = json.loads(result)
        assert "questions" in parsed_result
        assert len(parsed_result["questions"]) == 2
        assert parsed_result["total_questions"] == 2
    
    @patch('app.tools.question_generator.genai')
    def test_run_with_fallback_parsing(self, mock_genai):
        """Test fallback parsing when structured response fails."""
        # Mock a response that's not valid JSON but contains questions
        mock_response = Mock()
        mock_response.text = """
        1. What is your experience with Python?
        2. How do you handle team conflicts?
        3. Describe your approach to debugging.
        """
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        tool = QuestionGeneratorTool()
        result = tool._run("sample profile")
        
        # Should create fallback structure
        parsed_result = json.loads(result)
        assert "questions" in parsed_result
        assert parsed_result["total_questions"] > 0

class TestPDFConverterTool:
    """Test cases for PDFConverterTool."""
    
    def test_init(self):
        """Test tool initialization."""
        tool = PDFConverterTool()
        assert tool.name == "pdf_converter"
        assert "pdf" in tool.description.lower()
    
    @patch('app.tools.pdf_tool.markitdown.MarkItDown')
    def test_run_success(self, mock_markitdown, temp_file):
        """Test successful PDF conversion."""
        # Mock the MarkItDown response
        mock_result = Mock()
        mock_result.text_content = "Extracted text from PDF"
        
        mock_converter = Mock()
        mock_converter.convert.return_value = mock_result
        mock_markitdown.return_value = mock_converter
        
        tool = PDFConverterTool()
        result = tool._run(temp_file)
        
        assert result == "Extracted text from PDF"
        mock_converter.convert.assert_called_once_with(temp_file)
    
    @patch('app.tools.pdf_tool.markitdown.MarkItDown')
    def test_run_with_exception(self, mock_markitdown, temp_file):
        """Test handling of exceptions during PDF conversion."""
        mock_converter = Mock()
        mock_converter.convert.side_effect = Exception("Conversion failed")
        mock_markitdown.return_value = mock_converter
        
        tool = PDFConverterTool()
        result = tool._run(temp_file)
        
        assert "Error converting PDF" in result
        assert "Conversion failed" in result
    
    def test_run_with_nonexistent_file(self):
        """Test handling of nonexistent file."""
        tool = PDFConverterTool()
        result = tool._run("/nonexistent/file.pdf")
        
        assert "Error converting PDF" in result

# Integration tests for tool combinations
class TestToolIntegration:
    """Integration tests for multiple tools working together."""
    
    @patch('app.tools.pdf_tool.markitdown.MarkItDown')
    @patch('app.tools.profile_extractor.genai')
    @patch('app.tools.career_recommender.genai')
    def test_full_pipeline(self, mock_career_genai, mock_profile_genai, mock_markitdown, temp_file):
        """Test the full pipeline from PDF to career recommendation."""
        # Mock PDF conversion
        mock_pdf_result = Mock()
        mock_pdf_result.text_content = "John Doe, Software Engineer with 5 years experience"
        mock_pdf_converter = Mock()
        mock_pdf_converter.convert.return_value = mock_pdf_result
        mock_markitdown.return_value = mock_pdf_converter
        
        # Mock profile extraction
        mock_profile_response = Mock()
        mock_profile_response.text = json.dumps({
            "personal_info": {"name": "John Doe"},
            "skills": {"technical": ["Python"]},
            "experience": [],
            "education": [],
            "certifications": [],
            "languages": [],
            "summary": "Software engineer",
            "total_experience_years": 5.0,
            "key_achievements": []
        })
        mock_profile_model = Mock()
        mock_profile_model.generate_content.return_value = mock_profile_response
        mock_profile_genai.GenerativeModel.return_value = mock_profile_model
        
        # Mock career recommendation
        mock_career_response = Mock()
        mock_career_response.text = json.dumps({
            "primary_role": "Software Engineer",
            "alternative_roles": [],
            "confidence_score": 0.8,
            "reasoning": "Good fit",
            "required_skills": [],
            "skill_gaps": [],
            "salary_range": {"min": 60000, "max": 90000, "currency": "USD"},
            "growth_potential": "Good",
            "industry_demand": "High"
        })
        mock_career_model = Mock()
        mock_career_model.generate_content.return_value = mock_career_response
        mock_career_genai.GenerativeModel.return_value = mock_career_model
        
        # Run the pipeline
        pdf_tool = PDFConverterTool()
        profile_tool = ProfileExtractorTool()
        career_tool = CareerRecommenderTool()
        
        # Step 1: Extract text from PDF
        cv_text = pdf_tool._run(temp_file)
        assert cv_text == "John Doe, Software Engineer with 5 years experience"
        
        # Step 2: Extract profile
        profile_data = profile_tool._run(cv_text)
        parsed_profile = json.loads(profile_data)
        assert parsed_profile["personal_info"]["name"] == "John Doe"
        
        # Step 3: Get career recommendation
        career_rec = career_tool._run(profile_data)
        parsed_career = json.loads(career_rec)
        assert parsed_career["primary_role"] == "Software Engineer"
        assert parsed_career["confidence_score"] == 0.8
