# CV2Interview - Advanced AI-Powered CV Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Overview

CV2Interview is a comprehensive AI-powered platform that transforms CV analysis and interview preparation. Built with cutting-edge technology, it provides intelligent insights, career recommendations, and personalized interview questions to help professionals advance their careers.

### ✨ Key Features

- **🧠 Advanced AI Analysis**: Powered by Google Gemini AI for comprehensive CV parsing and analysis
- **📊 Real-time Analytics**: Interactive dashboards with skills trends, career insights, and performance metrics
- **🎯 Career Recommendations**: AI-driven career path suggestions with confidence scoring
- **❓ Interview Preparation**: Personalized interview questions based on your profile and target role
- **📈 Skills Analytics**: Detailed analysis of skill trends, gaps, and market demand
- **🔒 Enterprise Security**: Built-in rate limiting, authentication, and data protection
- **📱 Responsive Design**: Modern, mobile-first UI with real-time updates

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with async/await support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for performance optimization
- **AI Integration**: Google Gemini AI for natural language processing
- **Authentication**: JWT-based authentication system
- **Monitoring**: Structured logging and performance metrics

### Frontend (Next.js)
- **Framework**: Next.js 14 with App Router
- **UI Components**: Shadcn/ui with Tailwind CSS
- **Charts**: Recharts for data visualization
- **State Management**: React hooks and context
- **TypeScript**: Full type safety throughout

### Database Schema
- **Users**: Authentication and user management
- **CV Analysis**: Structured CV data and processing results
- **Interview Sessions**: Generated questions and session tracking
- **Analytics**: Performance metrics and insights
- **System Metrics**: Monitoring and health data

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 13+
- Redis 6+

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/cv2interview.git
   cd cv2interview
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb cv2interview

   # Run migrations
   alembic upgrade head
   ```

5. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd cv2interview-app
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your configuration
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📋 Environment Variables

### Backend (.env)
```env
# AI Configuration
GEMINI_API_KEY=your_gemini_api_key

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/cv2interview

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_FILE_TYPES=.pdf,.doc,.docx,.txt

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Monitoring
SENTRY_DSN=your_sentry_dsn
ENABLE_METRICS=true

# Development
DEBUG=false
ENVIRONMENT=production
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=CV2Interview
NEXT_PUBLIC_ENVIRONMENT=development
```

## 🧪 Testing

### Backend Tests
```bash
cd backend

# Run all tests
python run_tests.py --all

# Run specific test types
python run_tests.py --unit
python run_tests.py --integration
python run_tests.py --api

# Run with coverage
python run_tests.py --coverage

# Format and lint code
python run_tests.py --format --lint
```

### Frontend Tests
```bash
cd cv2interview-app

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

## 📊 API Documentation

### Core Endpoints

#### CV Processing
- `POST /api/v1/agent/process-cv` - Comprehensive CV analysis
- `POST /api/v1/agent/career-recommendation` - Get career recommendations
- `POST /api/v1/agent/generate-questions` - Generate interview questions

#### Analytics Dashboard
- `GET /api/v1/dashboard/overview` - Dashboard overview data
- `GET /api/v1/dashboard/skills-analytics` - Skills analysis
- `GET /api/v1/dashboard/career-analytics` - Career trends
- `GET /api/v1/dashboard/health` - System health status

#### Data Export
- `GET /api/v1/dashboard/export/data` - Export analytics data
- `GET /api/v1/dashboard/trends/skills` - Skill trends over time
- `GET /api/v1/dashboard/trends/careers` - Career trends over time

### Authentication
```bash
# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "user@example.com", "password": "password"}'

# Use token in requests
curl -X GET "http://localhost:8000/api/v1/dashboard/overview" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔧 Development

### Code Quality
- **Formatting**: Black, isort
- **Linting**: Flake8, ESLint
- **Type Checking**: MyPy, TypeScript
- **Testing**: Pytest, Jest
- **Pre-commit Hooks**: Automated quality checks

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Adding New Features

1. **Backend Feature**
   ```bash
   # Create new module
   mkdir app/features/new_feature
   touch app/features/new_feature/__init__.py
   touch app/features/new_feature/models.py
   touch app/features/new_feature/routes.py
   touch app/features/new_feature/services.py

   # Add tests
   touch tests/test_new_feature.py
   ```

2. **Frontend Component**
   ```bash
   # Create new component
   mkdir cv2interview-app/components/new-component
   touch cv2interview-app/components/new-component/index.tsx
   touch cv2interview-app/components/new-component/new-component.tsx
   ```

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Scale services
docker-compose up -d --scale backend=3
```

### Production Deployment
```bash
# Backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
npm run build
npm start
```

### Environment Setup
- **Development**: Local setup with hot reload
- **Staging**: Docker containers with test data
- **Production**: Kubernetes cluster with monitoring

## 📈 Monitoring & Analytics

### Health Checks
- `GET /health` - Basic health check
- `GET /api/v1/dashboard/health` - Detailed system health

### Metrics
- Response times
- Error rates
- Database performance
- AI model usage
- User activity

### Logging
- Structured JSON logging
- Request/response tracking
- Error tracking with Sentry
- Performance monitoring

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   python run_tests.py --all
   npm test
   ```
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Guidelines
- Follow existing code style
- Add tests for new features
- Update documentation
- Use meaningful commit messages
- Keep PRs focused and small

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful language processing
- **FastAPI** for the excellent async web framework
- **Next.js** for the modern React framework
- **Shadcn/ui** for beautiful UI components
- **Recharts** for data visualization

## 📞 Support

- **Documentation**: [docs.cv2interview.com](https://docs.cv2interview.com)
- **Issues**: [GitHub Issues](https://github.com/your-org/cv2interview/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/cv2interview/discussions)
- **Email**: support@cv2interview.com

---

**Built with ❤️ by the CV2Interview Team**