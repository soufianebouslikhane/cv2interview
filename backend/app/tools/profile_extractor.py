import json
import time
import re
from typing import Dict, List, Any
from dotenv import load_dotenv
import google.generativeai as genai
from app.tools.base import CustomBaseTool
from app.config.config import GEMINI_API_KEY, AI_MODEL_TEMPERATURE, AI_MAX_TOKENS
from pydantic import PrivateAttr, BaseModel
import logging

logger = logging.getLogger(__name__)

class ExtractedProfile(BaseModel):
    """Structured profile extraction output."""
    personal_info: Dict[str, Any]
    skills: Dict[str, List[str]]
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    certifications: List[str]
    languages: List[Dict[str, str]]
    summary: str
    total_experience_years: float
    key_achievements: List[str]

class ProfileExtractorTool(CustomBaseTool):
    name: str = "enhanced_profile_extractor"
    description: str = (
        "Advanced profile extraction tool that comprehensively analyzes CV/resume content "
        "and extracts structured information including skills categorization, detailed "
        "work experience, education, certifications, and key achievements."
    )

    _model = PrivateAttr()

    def __init__(self):
        super().__init__()
        load_dotenv()
        genai.configure(api_key=GEMINI_API_KEY)
        self._model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config=genai.types.GenerationConfig(
                temperature=AI_MODEL_TEMPERATURE,
                max_output_tokens=AI_MAX_TOKENS,
            )
        )

    def _run(self, cv_text: str) -> str:
        """Extract comprehensive profile information from CV text."""
        start_time = time.time()

        try:
            # Preprocess the CV text
            cleaned_text = self._preprocess_text(cv_text)

            prompt = self._create_extraction_prompt(cleaned_text)
            response = self._model.generate_content(prompt)

            processing_time = time.time() - start_time
            logger.info("Profile extraction completed",
                       processing_time=processing_time,
                       cv_length=len(cv_text))

            # Parse and validate the response
            result = self._parse_response(response.text.strip())
            return result

        except Exception as e:
            logger.error("Error in profile extraction", error=str(e))
            return f"❌ Error extracting profile: {e}"

    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess CV text for better extraction."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters that might interfere
        text = re.sub(r'[^\w\s\-\.\,\(\)\@\+\#\&\%\$\!\?\:\;]', '', text)

        # Normalize common CV sections
        text = re.sub(r'(?i)(experience|work experience|employment)', 'WORK EXPERIENCE', text)
        text = re.sub(r'(?i)(education|academic)', 'EDUCATION', text)
        text = re.sub(r'(?i)(skills|technical skills|core competencies)', 'SKILLS', text)

        return text.strip()

    def _create_extraction_prompt(self, cv_text: str) -> str:
        """Create a comprehensive prompt for profile extraction."""
        return f"""
You are an expert HR professional and CV parser. Analyze the following CV/resume text and extract comprehensive information in a structured format.

CV TEXT:
{cv_text}

EXTRACTION REQUIREMENTS:
1. Personal Information: Name, contact details, location, professional title
2. Skills: Categorize into technical, soft skills, tools, programming languages, frameworks
3. Work Experience: Company, role, duration, responsibilities, achievements
4. Education: Institution, degree, field of study, graduation year, GPA if mentioned
5. Certifications: Professional certifications and licenses
6. Languages: Spoken languages and proficiency levels
7. Summary: Professional summary or objective
8. Calculate total years of experience
9. Key achievements and accomplishments

OUTPUT FORMAT (JSON):
{{
    "personal_info": {{
        "name": "Full name if found",
        "email": "Email address",
        "phone": "Phone number",
        "location": "City, Country",
        "professional_title": "Current or desired job title",
        "linkedin": "LinkedIn profile URL if found"
    }},
    "skills": {{
        "technical": ["List of technical skills"],
        "programming_languages": ["Programming languages"],
        "frameworks_tools": ["Frameworks, tools, software"],
        "soft_skills": ["Communication, leadership, etc."],
        "domains": ["Industry domains, specializations"]
    }},
    "experience": [
        {{
            "company": "Company name",
            "position": "Job title",
            "duration": "Start date - End date",
            "years": 2.5,
            "responsibilities": ["Key responsibilities"],
            "achievements": ["Notable achievements"],
            "technologies": ["Technologies used"]
        }}
    ],
    "education": [
        {{
            "institution": "University/School name",
            "degree": "Degree type",
            "field_of_study": "Major/Field",
            "graduation_year": "Year",
            "gpa": "GPA if mentioned",
            "honors": "Any honors or distinctions"
        }}
    ],
    "certifications": ["Professional certifications"],
    "languages": [
        {{
            "language": "Language name",
            "proficiency": "Native/Fluent/Intermediate/Basic"
        }}
    ],
    "summary": "Professional summary or career objective",
    "total_experience_years": 5.5,
    "key_achievements": ["Major accomplishments and highlights"]
}}

GUIDELINES:
- Extract information accurately without making assumptions
- If information is not found, use null or empty arrays
- Calculate experience years based on work history
- Categorize skills appropriately
- Include quantifiable achievements when mentioned
- Maintain original company and institution names
- Be precise with dates and durations

Respond ONLY with valid JSON format.
"""

    def _parse_response(self, response_text: str) -> str:
        """Parse and validate the AI response."""
        try:
            # Try to extract JSON from the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")

            json_str = response_text[start_idx:end_idx]
            parsed_data = json.loads(json_str)

            # Validate required fields
            required_fields = [
                "personal_info", "skills", "experience", "education",
                "certifications", "languages", "summary",
                "total_experience_years", "key_achievements"
            ]

            for field in required_fields:
                if field not in parsed_data:
                    parsed_data[field] = {} if field in ["personal_info", "skills"] else []

            # Ensure numeric fields are properly typed
            if "total_experience_years" in parsed_data:
                try:
                    parsed_data["total_experience_years"] = float(parsed_data["total_experience_years"])
                except (ValueError, TypeError):
                    parsed_data["total_experience_years"] = 0.0

            # Return formatted JSON
            return json.dumps(parsed_data, indent=2)

        except (json.JSONDecodeError, ValueError) as e:
            logger.warning("Failed to parse structured response", error=str(e))
            # Fallback to original response
            return response_text

    async def _arun(self, cv_text: str) -> str:
        """Async version of the profile extraction."""
        return self._run(cv_text)
