#!/bin/bash

# CV2Interview Deployment Script
# This script helps deploy the CV2Interview application in different environments

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="cv2interview"
DOCKER_COMPOSE_FILE="docker-compose.yml"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    log_info "Checking system requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    
    log_success "All requirements satisfied"
}

setup_environment() {
    log_info "Setting up environment..."
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        log_warning ".env file not found. Creating from template..."
        cat > .env << EOF
# AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Security
SECRET_KEY=$(openssl rand -hex 32)

# Database (will be set by Docker Compose)
DATABASE_URL=postgresql+asyncpg://cv2interview:cv2interview_password@postgres:5432/cv2interview

# Redis (will be set by Docker Compose)
REDIS_URL=redis://redis:6379/0

# Application
DEBUG=false
ENVIRONMENT=production
ENABLE_METRICS=true

# File Upload
MAX_FILE_SIZE=10485760
ALLOWED_FILE_TYPES=.pdf,.doc,.docx,.txt

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
EOF
        log_warning "Please edit .env file and add your GEMINI_API_KEY"
        log_warning "You can get it from: https://makersuite.google.com/app/apikey"
    fi
    
    # Create necessary directories
    mkdir -p backend/uploaded_files
    mkdir -p backend/output
    mkdir -p backend/logs
    
    log_success "Environment setup complete"
}

build_images() {
    log_info "Building Docker images..."
    
    # Build backend
    log_info "Building backend image..."
    docker-compose build backend
    
    # Build frontend
    log_info "Building frontend image..."
    docker-compose build frontend
    
    log_success "Docker images built successfully"
}

start_services() {
    local profile=${1:-""}
    
    log_info "Starting services..."
    
    if [ -n "$profile" ]; then
        docker-compose --profile "$profile" up -d
    else
        docker-compose up -d postgres redis backend frontend
    fi
    
    log_info "Waiting for services to be healthy..."
    sleep 10
    
    # Check service health
    check_service_health
    
    log_success "All services started successfully"
}

check_service_health() {
    log_info "Checking service health..."
    
    # Check PostgreSQL
    if docker-compose exec -T postgres pg_isready -U cv2interview -d cv2interview &> /dev/null; then
        log_success "PostgreSQL is healthy"
    else
        log_error "PostgreSQL is not healthy"
        return 1
    fi
    
    # Check Redis
    if docker-compose exec -T redis redis-cli ping | grep -q PONG; then
        log_success "Redis is healthy"
    else
        log_error "Redis is not healthy"
        return 1
    fi
    
    # Check Backend
    if curl -f http://localhost:8000/health &> /dev/null; then
        log_success "Backend is healthy"
    else
        log_warning "Backend health check failed, but it might still be starting..."
    fi
    
    # Check Frontend
    if curl -f http://localhost:3000 &> /dev/null; then
        log_success "Frontend is healthy"
    else
        log_warning "Frontend health check failed, but it might still be starting..."
    fi
}

stop_services() {
    log_info "Stopping services..."
    docker-compose down
    log_success "Services stopped"
}

restart_services() {
    log_info "Restarting services..."
    stop_services
    start_services
    log_success "Services restarted"
}

show_logs() {
    local service=${1:-""}
    
    if [ -n "$service" ]; then
        docker-compose logs -f "$service"
    else
        docker-compose logs -f
    fi
}

run_tests() {
    log_info "Running tests..."
    
    # Backend tests
    log_info "Running backend tests..."
    docker-compose exec backend python run_tests.py --all
    
    # Frontend tests (if test command exists)
    log_info "Running frontend tests..."
    docker-compose exec frontend npm test --passWithNoTests
    
    log_success "Tests completed"
}

backup_data() {
    local backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
    
    log_info "Creating backup in $backup_dir..."
    mkdir -p "$backup_dir"
    
    # Backup database
    docker-compose exec -T postgres pg_dump -U cv2interview cv2interview > "$backup_dir/database.sql"
    
    # Backup uploaded files
    docker cp cv2interview-backend:/app/uploaded_files "$backup_dir/"
    
    # Backup Redis data
    docker-compose exec -T redis redis-cli BGSAVE
    docker cp cv2interview-redis:/data/dump.rdb "$backup_dir/"
    
    log_success "Backup created in $backup_dir"
}

show_status() {
    log_info "Service Status:"
    docker-compose ps
    
    echo ""
    log_info "Application URLs:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo "  API Documentation: http://localhost:8000/docs"
    echo "  Health Check: http://localhost:8000/health"
}

show_help() {
    echo "CV2Interview Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  setup       Setup environment and create necessary files"
    echo "  build       Build Docker images"
    echo "  start       Start all services"
    echo "  stop        Stop all services"
    echo "  restart     Restart all services"
    echo "  status      Show service status and URLs"
    echo "  logs        Show logs (optional: specify service name)"
    echo "  test        Run tests"
    echo "  backup      Create backup of data"
    echo "  clean       Clean up Docker resources"
    echo "  help        Show this help message"
    echo ""
    echo "Profiles:"
    echo "  production  Start with Nginx reverse proxy"
    echo "  monitoring  Start with Prometheus and Grafana"
    echo ""
    echo "Examples:"
    echo "  $0 setup                    # Setup environment"
    echo "  $0 start                    # Start basic services"
    echo "  $0 start production         # Start with production profile"
    echo "  $0 logs backend             # Show backend logs"
    echo "  $0 backup                   # Create data backup"
}

clean_up() {
    log_info "Cleaning up Docker resources..."
    
    # Stop and remove containers
    docker-compose down --remove-orphans
    
    # Remove unused images
    docker image prune -f
    
    # Remove unused volumes (be careful with this)
    read -p "Do you want to remove unused volumes? This will delete data! (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker volume prune -f
        log_warning "Volumes removed. Data may be lost!"
    fi
    
    log_success "Cleanup completed"
}

# Main script logic
case "${1:-help}" in
    setup)
        check_requirements
        setup_environment
        ;;
    build)
        check_requirements
        build_images
        ;;
    start)
        check_requirements
        start_services "$2"
        show_status
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        show_status
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs "$2"
        ;;
    test)
        run_tests
        ;;
    backup)
        backup_data
        ;;
    clean)
        clean_up
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
