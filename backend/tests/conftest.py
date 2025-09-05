"""Test configuration and fixtures."""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
import tempfile
import os

from app.main import app
from app.database.connection import get_db, Base
from app.database.models import User, CVAnalysis, InterviewSession

# Test database URL (SQLite in memory for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

# Test session factory
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
    autocommit=False,
)

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
    
    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
def client(db_session: AsyncSession) -> TestClient:
    """Create a test client with database dependency override."""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()

@pytest.fixture
def sample_cv_text() -> str:
    """Sample CV text for testing."""
    return """
    John Doe
    Software Engineer
    Email: john.doe@email.com
    Phone: +1-234-567-8900
    
    EXPERIENCE:
    Senior Software Engineer at TechCorp (2020-2023)
    - Developed web applications using Python and React
    - Led a team of 5 developers
    - Implemented CI/CD pipelines
    
    Software Engineer at StartupXYZ (2018-2020)
    - Built REST APIs using FastAPI
    - Worked with PostgreSQL databases
    - Collaborated with cross-functional teams
    
    EDUCATION:
    Bachelor of Science in Computer Science
    University of Technology (2014-2018)
    
    SKILLS:
    - Programming: Python, JavaScript, TypeScript
    - Frameworks: FastAPI, React, Django
    - Databases: PostgreSQL, MongoDB
    - Tools: Docker, Git, AWS
    """

@pytest.fixture
def sample_profile_data() -> dict:
    """Sample structured profile data for testing."""
    return {
        "personal_info": {
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "+1-234-567-8900",
            "professional_title": "Software Engineer"
        },
        "skills": {
            "technical": ["Python", "JavaScript", "TypeScript"],
            "frameworks_tools": ["FastAPI", "React", "Django", "Docker", "Git", "AWS"],
            "databases": ["PostgreSQL", "MongoDB"]
        },
        "experience": [
            {
                "company": "TechCorp",
                "position": "Senior Software Engineer",
                "duration": "2020-2023",
                "years": 3.0,
                "responsibilities": ["Developed web applications", "Led team of 5 developers"],
                "technologies": ["Python", "React"]
            },
            {
                "company": "StartupXYZ",
                "position": "Software Engineer",
                "duration": "2018-2020",
                "years": 2.0,
                "responsibilities": ["Built REST APIs", "Worked with databases"],
                "technologies": ["FastAPI", "PostgreSQL"]
            }
        ],
        "education": [
            {
                "institution": "University of Technology",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "graduation_year": "2018"
            }
        ],
        "total_experience_years": 5.0,
        "summary": "Experienced software engineer with 5 years in web development"
    }

@pytest.fixture
def sample_career_recommendation() -> dict:
    """Sample career recommendation data for testing."""
    return {
        "primary_role": "Senior Software Engineer",
        "alternative_roles": ["Full Stack Developer", "Backend Engineer", "Tech Lead"],
        "confidence_score": 0.85,
        "reasoning": "Strong technical background with leadership experience",
        "required_skills": ["Python", "React", "System Design"],
        "skill_gaps": ["Machine Learning", "Cloud Architecture"],
        "salary_range": {"min": 80000, "max": 120000, "currency": "USD"},
        "growth_potential": "High - strong technical and leadership skills",
        "industry_demand": "Very high demand for experienced software engineers"
    }

@pytest.fixture
def sample_interview_questions() -> dict:
    """Sample interview questions data for testing."""
    return {
        "questions": [
            {
                "question": "Tell me about your experience leading a development team.",
                "category": "Leadership",
                "difficulty": "Medium",
                "purpose": "Assess leadership and management skills",
                "expected_answer_type": "Story/Example"
            },
            {
                "question": "How would you design a scalable web application architecture?",
                "category": "Technical Skills",
                "difficulty": "Hard",
                "purpose": "Evaluate system design capabilities",
                "expected_answer_type": "Technical explanation"
            },
            {
                "question": "Describe a challenging bug you had to fix.",
                "category": "Problem Solving",
                "difficulty": "Medium",
                "purpose": "Assess problem-solving approach",
                "expected_answer_type": "Story/Example"
            }
        ],
        "total_questions": 3,
        "estimated_duration": 45,
        "difficulty_distribution": {"Easy": 0, "Medium": 2, "Hard": 1},
        "category_distribution": {"Leadership": 1, "Technical Skills": 1, "Problem Solving": 1}
    }

@pytest.fixture
async def sample_user(db_session: AsyncSession) -> User:
    """Create a sample user for testing."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password_here",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
async def sample_cv_analysis(db_session: AsyncSession, sample_user: User, sample_profile_data: dict) -> CVAnalysis:
    """Create a sample CV analysis for testing."""
    cv_analysis = CVAnalysis(
        user_id=sample_user.id,
        original_filename="test_cv.pdf",
        file_path="/tmp/test_cv.pdf",
        file_size=1024,
        file_type="pdf",
        raw_text="Sample CV text content",
        extracted_profile=sample_profile_data,
        skills=["Python", "JavaScript", "React"],
        experience=[{"company": "TechCorp", "position": "Engineer"}],
        processing_time=2.5,
        ai_model_used="gemini-1.5-flash",
        processing_status="completed"
    )
    db_session.add(cv_analysis)
    await db_session.commit()
    await db_session.refresh(cv_analysis)
    return cv_analysis

@pytest.fixture
def temp_file():
    """Create a temporary file for testing file uploads."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(b"Sample PDF content for testing")
        tmp_path = tmp.name
    
    yield tmp_path
    
    # Cleanup
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)

# Mock environment variables for testing
@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("GEMINI_API_KEY", "test_api_key")
    monkeypatch.setenv("DATABASE_URL", TEST_DATABASE_URL)
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/1")
    monkeypatch.setenv("SECRET_KEY", "test_secret_key")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("ENVIRONMENT", "testing")
