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

class InterviewQuestion(BaseModel):
    """Structured interview question."""
    question: str
    category: str
    difficulty: str
    purpose: str
    expected_answer_type: str

class QuestionSet(BaseModel):
    """Complete set of interview questions."""
    questions: List[InterviewQuestion]
    total_questions: int
    estimated_duration: int
    difficulty_distribution: Dict[str, int]
    category_distribution: Dict[str, int]

class QuestionGeneratorTool(CustomBaseTool):
    name: str = "enhanced_question_generator"
    description: str = (
        "Advanced interview question generator that creates personalized, categorized "
        "interview questions based on candidate profiles with difficulty levels, "
        "estimated duration, and strategic interview flow."
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

    def _run(self, profile_data: str, target_role: str = "", difficulty_level: str = "intermediate") -> str:
        """Generate comprehensive interview questions."""
        start_time = time.time()

        try:
            prompt = self._create_question_prompt(profile_data, target_role, difficulty_level)
            response = self._model.generate_content(prompt)

            processing_time = time.time() - start_time
            logger.info("Interview questions generated",
                       processing_time=processing_time,
                       target_role=target_role,
                       difficulty=difficulty_level)

            # Parse and validate the response
            result = self._parse_response(response.text.strip())
            return result

        except Exception as e:
            logger.error("Error in question generation", error=str(e))
            return f"❌ Error generating questions: {e}"

    def _create_question_prompt(self, profile_data: str, target_role: str, difficulty_level: str) -> str:
        """Create a comprehensive prompt for question generation."""
        return f"""
You are a senior HR professional and interview expert with extensive experience in technical and behavioral interviewing. Generate a comprehensive set of interview questions based on the candidate profile.

CANDIDATE PROFILE:
{profile_data}

TARGET ROLE: {target_role if target_role else "Based on profile analysis"}
DIFFICULTY LEVEL: {difficulty_level}

QUESTION REQUIREMENTS:
1. Generate exactly 15 questions covering all aspects
2. Include multiple question categories
3. Vary difficulty levels appropriately
4. Ensure questions are role-specific and relevant
5. Include both technical and behavioral questions
6. Consider the candidate's experience level

QUESTION CATEGORIES:
- Technical Skills (3-4 questions)
- Problem Solving (2-3 questions)
- Behavioral/Situational (3-4 questions)
- Leadership & Teamwork (2-3 questions)
- Career Goals & Motivation (2-3 questions)

DIFFICULTY LEVELS:
- Easy: Basic knowledge and experience questions
- Medium: Scenario-based and analytical questions
- Hard: Complex problem-solving and strategic thinking

OUTPUT FORMAT (JSON):
{{
    "questions": [
        {{
            "question": "Detailed interview question text",
            "category": "Technical Skills|Problem Solving|Behavioral|Leadership|Career Goals",
            "difficulty": "Easy|Medium|Hard",
            "purpose": "What this question aims to assess",
            "expected_answer_type": "Technical explanation|Story/Example|Opinion|Strategy"
        }}
    ],
    "total_questions": 15,
    "estimated_duration": 60,
    "difficulty_distribution": {{
        "Easy": 5,
        "Medium": 7,
        "Hard": 3
    }},
    "category_distribution": {{
        "Technical Skills": 4,
        "Problem Solving": 3,
        "Behavioral": 4,
        "Leadership": 2,
        "Career Goals": 2
    }}
}}

GUIDELINES:
- Questions should be open-ended and encourage detailed responses
- Avoid yes/no questions
- Include scenario-based questions for behavioral assessment
- Technical questions should match the candidate's skill level
- Consider industry-specific terminology and concepts
- Ensure questions are legally compliant and unbiased
- Include questions that reveal cultural fit
- Balance depth with interview time constraints

EXAMPLE QUESTION FORMATS:
- "Tell me about a time when..."
- "How would you approach..."
- "What's your experience with..."
- "Describe a situation where..."
- "Walk me through your process for..."

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
                "questions", "total_questions", "estimated_duration",
                "difficulty_distribution", "category_distribution"
            ]

            for field in required_fields:
                if field not in parsed_data:
                    if field == "questions":
                        parsed_data[field] = []
                    elif field in ["difficulty_distribution", "category_distribution"]:
                        parsed_data[field] = {}
                    else:
                        parsed_data[field] = 0

            # Validate questions structure
            if "questions" in parsed_data and isinstance(parsed_data["questions"], list):
                for i, question in enumerate(parsed_data["questions"]):
                    if not isinstance(question, dict):
                        continue

                    # Ensure required question fields
                    question_fields = ["question", "category", "difficulty", "purpose", "expected_answer_type"]
                    for field in question_fields:
                        if field not in question:
                            question[field] = "Not specified"

            # Update total questions count
            parsed_data["total_questions"] = len(parsed_data.get("questions", []))

            # Return formatted JSON
            return json.dumps(parsed_data, indent=2)

        except (json.JSONDecodeError, ValueError) as e:
            logger.warning("Failed to parse structured response", error=str(e))
            # Fallback to simple question list
            lines = response_text.strip().split('\n')
            questions = []
            for i, line in enumerate(lines[:15], 1):
                if line.strip():
                    questions.append({
                        "question": line.strip(),
                        "category": "General",
                        "difficulty": "Medium",
                        "purpose": "General assessment",
                        "expected_answer_type": "Detailed response"
                    })

            fallback_data = {
                "questions": questions,
                "total_questions": len(questions),
                "estimated_duration": len(questions) * 4,  # 4 minutes per question
                "difficulty_distribution": {"Medium": len(questions)},
                "category_distribution": {"General": len(questions)}
            }

            return json.dumps(fallback_data, indent=2)

    async def _arun(self, profile_data: str, target_role: str = "", difficulty_level: str = "intermediate") -> str:
        """Async version of the question generation."""
        return self._run(profile_data, target_role, difficulty_level)
