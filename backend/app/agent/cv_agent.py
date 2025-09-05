"""Enhanced CV Agent with comprehensive analysis capabilities."""

import json
import time
import logging
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.tools.pdf_tool import PDFConverterTool
from app.tools.profile_extractor import ProfileExtractorTool
from app.tools.question_generator import QuestionGeneratorTool
from app.tools.career_recommender import CareerRecommenderTool

logger = logging.getLogger(__name__)

class EnhancedCVAgent:
    """Enhanced CV analysis agent with comprehensive capabilities."""

    def __init__(self):
        self.pdf_tool = PDFConverterTool()
        self.profile_tool = ProfileExtractorTool()
        self.question_tool = QuestionGeneratorTool()
        self.career_tool = CareerRecommenderTool()

    async def process_cv_comprehensive(
        self,
        file_path: str,
        target_role: str = "",
        difficulty_level: str = "intermediate",
        db_session: Optional[AsyncSession] = None
    ) -> Dict[str, Any]:
        """Comprehensive CV processing with all analysis steps."""
        start_time = time.time()

        try:
            # Step 1: Extract text from PDF
            logger.info(f"Starting CV processing for file: {file_path}")
            raw_text = self.pdf_tool._run(file_path)

            if "Error" in raw_text:
                raise ValueError(f"PDF extraction failed: {raw_text}")

            # Step 2: Extract structured profile
            logger.info("Extracting structured profile")
            profile_data = self.profile_tool._run(raw_text)

            # Step 3: Generate career recommendations
            logger.info("Generating career recommendations")
            career_recommendations = self.career_tool._run(profile_data)

            # Step 4: Generate interview questions
            logger.info("Generating interview questions")
            interview_questions = self.question_tool._run(
                profile_data,
                target_role,
                difficulty_level
            )

            # Step 5: Calculate processing metrics
            processing_time = time.time() - start_time

            # Step 6: Compile comprehensive results
            results = {
                "processing_info": {
                    "file_path": file_path,
                    "processing_time": round(processing_time, 2),
                    "status": "completed",
                    "timestamp": time.time()
                },
                "raw_text": raw_text,
                "profile_analysis": self._parse_json_safely(profile_data),
                "career_recommendations": self._parse_json_safely(career_recommendations),
                "interview_questions": self._parse_json_safely(interview_questions),
                "analytics": await self._generate_quick_analytics(profile_data, career_recommendations)
            }

            # Step 7: Save to database if session provided
            if db_session:
                await self._save_to_database(results, db_session)

            logger.info(f"CV processing completed in {processing_time:.2f} seconds")
            return results

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"CV processing failed after {processing_time:.2f} seconds: {e}")

            return {
                "processing_info": {
                    "file_path": file_path,
                    "processing_time": round(processing_time, 2),
                    "status": "failed",
                    "error": str(e),
                    "timestamp": time.time()
                },
                "error": str(e)
            }

    async def quick_career_recommendation(self, cv_text: str) -> Dict[str, Any]:
        """Quick career recommendation without full processing."""
        try:
            start_time = time.time()

            # Extract profile summary
            profile_summary = self.profile_tool._run(cv_text)
            if "Error" in profile_summary:
                raise ValueError("Could not extract profile from CV")

            # Generate recommendations
            recommendation = self.career_tool._run(profile_summary)

            processing_time = time.time() - start_time

            return {
                "success": True,
                "processing_time": round(processing_time, 2),
                "profile_summary": self._parse_json_safely(profile_summary),
                "career_recommendation": self._parse_json_safely(recommendation)
            }

        except Exception as e:
            logger.error(f"Quick career recommendation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_targeted_questions(
        self,
        profile_data: str,
        target_role: str,
        difficulty_level: str = "intermediate",
        question_count: int = 15
    ) -> Dict[str, Any]:
        """Generate targeted interview questions based on profile and role."""
        try:
            start_time = time.time()

            # Enhance the profile data with target role context
            enhanced_prompt = f"""
            CANDIDATE PROFILE:
            {profile_data}

            TARGET ROLE: {target_role}
            DIFFICULTY LEVEL: {difficulty_level}
            REQUESTED QUESTIONS: {question_count}

            Generate interview questions specifically tailored for the target role.
            """

            questions = self.question_tool._run(enhanced_prompt, target_role, difficulty_level)
            processing_time = time.time() - start_time

            return {
                "success": True,
                "processing_time": round(processing_time, 2),
                "target_role": target_role,
                "difficulty_level": difficulty_level,
                "questions": self._parse_json_safely(questions)
            }

        except Exception as e:
            logger.error(f"Targeted question generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _parse_json_safely(self, json_string: str) -> Any:
        """Safely parse JSON string, return original if parsing fails."""
        try:
            return json.loads(json_string)
        except (json.JSONDecodeError, TypeError):
            return json_string

    async def _generate_quick_analytics(self, profile_data: str, career_data: str) -> Dict[str, Any]:
        """Generate quick analytics from the processed data."""
        try:
            profile = self._parse_json_safely(profile_data)
            career = self._parse_json_safely(career_data)

            analytics = {
                "profile_completeness": self._calculate_profile_completeness(profile),
                "skill_diversity": self._calculate_skill_diversity(profile),
                "experience_level": self._assess_experience_level(profile),
                "career_confidence": self._extract_career_confidence(career),
                "recommendations_count": self._count_recommendations(career)
            }

            return analytics

        except Exception as e:
            logger.warning(f"Quick analytics generation failed: {e}")
            return {"error": "Analytics generation failed"}

    def _calculate_profile_completeness(self, profile: Any) -> float:
        """Calculate profile completeness score."""
        if not isinstance(profile, dict):
            return 0.0

        required_fields = ["personal_info", "skills", "experience", "education"]
        present_fields = sum(1 for field in required_fields if profile.get(field))

        return round((present_fields / len(required_fields)) * 100, 1)

    def _calculate_skill_diversity(self, profile: Any) -> int:
        """Calculate skill diversity score."""
        if not isinstance(profile, dict):
            return 0

        skills = profile.get("skills", {})
        if not isinstance(skills, dict):
            return 0

        total_skills = sum(len(skill_list) for skill_list in skills.values() if isinstance(skill_list, list))
        return total_skills

    def _assess_experience_level(self, profile: Any) -> str:
        """Assess experience level based on profile."""
        if not isinstance(profile, dict):
            return "unknown"

        years = profile.get("total_experience_years", 0)

        if years < 2:
            return "entry"
        elif years < 5:
            return "junior"
        elif years < 10:
            return "mid"
        else:
            return "senior"

    def _extract_career_confidence(self, career: Any) -> float:
        """Extract confidence score from career recommendations."""
        if isinstance(career, dict):
            return career.get("confidence_score", 0.0)
        return 0.0

    def _count_recommendations(self, career: Any) -> int:
        """Count number of career recommendations."""
        if isinstance(career, dict):
            alternatives = career.get("alternative_roles", [])
            return 1 + len(alternatives) if alternatives else 1
        return 0

    async def _save_to_database(self, results: Dict[str, Any], db_session: AsyncSession):
        """Save processing results to database."""
        try:
            # This would implement database saving logic
            # For now, just log that we would save
            logger.info(f"Would save results to database: {list(results.keys())}")
            # Placeholder to avoid unused parameter warning
            _ = db_session

        except Exception as e:
            logger.error(f"Database save failed: {e}")

# Create global instance
enhanced_cv_agent = EnhancedCVAgent()

# Legacy compatibility functions
async def run_cv_agent(instruction: str) -> Dict[str, Any]:
    """Legacy compatibility function."""
    return {
        "response": f"Enhanced CV Agent received instruction: {instruction}",
        "message": "Please use the new comprehensive processing methods"
    }

async def run_career_recommendation(cv_text: str) -> str:
    """Legacy compatibility function for career recommendations."""
    try:
        result = await enhanced_cv_agent.quick_career_recommendation(cv_text)

        if result.get("success"):
            career_rec = result.get("career_recommendation", {})
            if isinstance(career_rec, dict):
                primary_role = career_rec.get("primary_role", "No specific role identified")
                confidence = career_rec.get("confidence_score", 0)
                return f"Recommended Role: {primary_role} (Confidence: {confidence:.2f})"
            else:
                return str(career_rec)
        else:
            return f"❌ Error during recommendation: {result.get('error', 'Unknown error')}"

    except Exception as e:
        return f"❌ Error during recommendation: {e}"
