import json
import time
from typing import Dict, List
from dotenv import load_dotenv
import google.generativeai as genai
from app.tools.base import CustomBaseTool
from app.config.config import GEMINI_API_KEY, AI_MODEL_TEMPERATURE, AI_MAX_TOKENS
from pydantic import PrivateAttr, BaseModel
import logging

logger = logging.getLogger(__name__)

class CareerRecommendation(BaseModel):
    """Structured career recommendation output."""
    primary_role: str
    alternative_roles: List[str]
    confidence_score: float
    reasoning: str
    required_skills: List[str]
    skill_gaps: List[str]
    salary_range: Dict[str, int]
    growth_potential: str
    industry_demand: str

class CareerRecommenderTool(CustomBaseTool):
    name: str = "enhanced_career_recommender"
    description: str = (
        "Advanced career recommendation tool that analyzes candidate profiles and provides "
        "comprehensive career suggestions with confidence scores, skill gap analysis, "
        "salary estimates, and market insights."
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

    def _run(self, profile_text: str) -> str:
        """Generate comprehensive career recommendations."""
        start_time = time.time()

        try:
            prompt = self._create_enhanced_prompt(profile_text)
            response = self._model.generate_content(prompt)

            processing_time = time.time() - start_time
            logger.info("Career recommendation generated",
                       processing_time=processing_time,
                       profile_length=len(profile_text))

            # Parse and validate the response
            result = self._parse_response(response.text.strip())
            return result

        except Exception as e:
            logger.error("Error in career recommendation", error=str(e))
            return f"❌ Error while generating career recommendations: {e}"

    def _create_enhanced_prompt(self, profile_text: str) -> str:
        """Create a comprehensive prompt for career recommendations."""
        return f"""
You are an expert career counselor and HR professional with deep knowledge of job markets, salary trends, and career progression paths. Analyze the following candidate profile and provide comprehensive career recommendations.

CANDIDATE PROFILE:
{profile_text}

ANALYSIS REQUIREMENTS:
1. Identify the candidate's core competencies and experience level
2. Assess their technical and soft skills
3. Consider their career trajectory and growth potential
4. Evaluate market demand for their skill set
5. Identify skill gaps for target roles

OUTPUT FORMAT (JSON):
{{
    "primary_role": "Most suitable job title based on current profile",
    "alternative_roles": ["2-3 alternative job titles that match the profile"],
    "confidence_score": 0.85,
    "reasoning": "Detailed explanation of why these roles are recommended",
    "required_skills": ["Key skills needed for the primary role"],
    "skill_gaps": ["Skills the candidate should develop"],
    "salary_range": {{"min": 50000, "max": 80000, "currency": "USD"}},
    "growth_potential": "High/Medium/Low with explanation",
    "industry_demand": "Current market demand assessment"
}}

GUIDELINES:
- Be realistic and data-driven in recommendations
- Consider both current skills and potential for growth
- Provide actionable insights for career development
- Include salary estimates based on market standards
- Assess industry trends and demand
- Confidence score should reflect how well the profile matches the role (0.0-1.0)

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
                "primary_role", "alternative_roles", "confidence_score",
                "reasoning", "required_skills", "skill_gaps",
                "salary_range", "growth_potential", "industry_demand"
            ]

            for field in required_fields:
                if field not in parsed_data:
                    raise ValueError(f"Missing required field: {field}")

            # Return formatted JSON
            return json.dumps(parsed_data, indent=2)

        except (json.JSONDecodeError, ValueError) as e:
            logger.warning("Failed to parse structured response", error=str(e))
            # Fallback to original response
            return response_text

    async def _arun(self, profile_text: str) -> str:
        """Async version of the career recommendation."""
        return self._run(profile_text)
