# DayPilot AI-Powered Scheduling System

An AI-powered one-day time management system that transforms natural language task descriptions into structured, optimized daily schedules. The system combines natural language processing, intelligent scheduling algorithms, and machine learning to create personalized daily schedules.

## Architecture Overview

The system follows the principle: **LLM for Understanding, Scheduler for Decisions, ML for Learning, UI for Control**

- **FastAPI Backend**: RESTful API with AI/ML integration
- **React TypeScript Frontend**: Interactive timeline UI  
- **SQLite Database**: Data persistence and historical tracking
- **AI Components**: Natural language processing and duration prediction

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn
- Docker (optional)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database:**
   ```bash
   python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"
   ```

5. **Start backend server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start frontend development server:**
   ```bash
   npm start
   ```

### Quick Development Scripts

Use the provided batch scripts for Windows:

- **Backend**: `scripts\start_backend.bat`
- **Frontend**: `scripts\start_frontend.bat`
- **Tests**: `scripts\run_tests.bat`

### Docker Development (Optional)

```bash
docker-compose up --build
```

## Project Structure

```
daypilot/
├── backend/                    # FastAPI Python backend
│   ├── app/
│   │   ├── api/               # API route handlers
│   │   ├── core/              # Core configuration and database
│   │   ├── models/            # Database models
│   │   └── main.py            # FastAPI application entry point
│   ├── tests/                 # Backend tests
│   ├── requirements.txt       # Python dependencies
│   ├── pyproject.toml         # Python project configuration
│   └── Dockerfile             # Docker configuration
├── frontend/                  # React TypeScript frontend
│   ├── src/                   # React source code
│   ├── public/                # Static assets
│   ├── package.json           # Node.js dependencies
│   └── Dockerfile             # Docker configuration
├── scripts/                   # Development utility scripts
├── docker-compose.yml         # Docker compose configuration
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Development Tools

- **Backend**: Python 3.11+, FastAPI, SQLite, pytest
- **Frontend**: React 18, TypeScript, Redux Toolkit, Jest
- **AI/ML**: OpenAI API integration (optional)
- **Development**: Docker, Black (formatting), Flake8 (linting), mypy (type checking)

## Key Features

- ✅ **Project Structure**: Complete backend and frontend setup
- ✅ **Database Schema**: SQLite with comprehensive data models
- ✅ **Development Environment**: Virtual environment, dependency management
- ✅ **Testing Framework**: Backend pytest, frontend Jest
- ✅ **Docker Support**: Containerized development and deployment
- ✅ **Development Tools**: Linting, formatting, type checking configured
- ✅ **API Foundation**: FastAPI with health endpoints and error handling

### Planned Features

- Natural language task input processing
- AI-powered duration prediction
- Deterministic scheduling algorithms  
- Interactive timeline with drag-and-drop
- Real-time conflict detection and resolution
- Explainable AI decision making
- Continuous learning from user behavior

## API Endpoints

### Health Checks
- `GET /` - Root endpoint with API information
- `GET /health` - Basic health check
- `GET /api/v1/health` - API v1 health check
- `GET /api/v1/status` - Detailed system status

### Development URLs
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs
- Frontend UI: http://localhost:3000

## Testing

### Backend Tests
```bash
cd backend
pytest -v
```

### Frontend Tests
```bash
cd frontend
npm test -- --watchAll=false
```

### All Tests
```bash
scripts\run_tests.bat
```

## Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=sqlite:///./daypilot.db

# AI Services (optional)
OPENAI_API_KEY=your_openai_api_key_here

# Development
DEBUG=true
CORS_ORIGINS=http://localhost:3000
```

## Requirements Implementation

This setup addresses the following specification requirements:

- **Requirements 11.1**: Data persistence with SQLite database and comprehensive schema
- **Requirements 12.4**: FastAPI backend with RESTful API structure and documentation  
- **Requirements 13.4**: Complete development environment with testing frameworks
- **Requirements 14.3**: Error handling and graceful fallback mechanisms
- **Requirements 15.1**: React TypeScript frontend foundation

## Next Steps

1. Implement natural language task parsing (LLM integration)
2. Build deterministic scheduling engine
3. Add ML-based duration prediction
4. Create interactive timeline UI components
5. Develop real-time conflict detection
6. Add explainable AI decision system

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `scripts\run_tests.bat`
5. Submit a pull request

## License

This project is part of the DayPilot AI-powered scheduling system development.