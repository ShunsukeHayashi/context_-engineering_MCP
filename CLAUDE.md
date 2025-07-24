# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MCP AI Guides Server - A FastAPI-based REST API that provides programmatic access to a curated collection of AI-related guides from OpenAI, Google, and Anthropic. Enhanced with Google Gemini AI integration for intelligent semantic search, content analysis, and guide comparisons. The server enables listing, searching, and retrieving metadata about AI guides covering topics like prompt engineering, AI agents, and AI safety.

## Commands and Development Workflow

### Initial Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### Running the Server
```bash
# Development with auto-reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Operations
```bash
# Build Docker image
docker build -t mcp-ai-guides-server .

# Run container
docker run -d --name ai-guides-app -p 8000:8000 mcp-ai-guides-server

# View logs
docker logs ai-guides-app

# Stop and remove container
docker stop ai-guides-app && docker rm ai-guides-app
```

### Testing API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# List all guides
curl http://localhost:8000/guides

# Search guides
curl "http://localhost:8000/guides/search?query=agent"

# Get specific guide (URL-encode the title)
curl "http://localhost:8000/guides/OpenAI%3A%20GPT%20Best%20Practices"

# Get download URL
curl "http://localhost:8000/guides/OpenAI%3A%20GPT%20Best%20Practices/download-url"

# Gemini-powered semantic search
curl -X POST "http://localhost:8000/guides/search/gemini" \
  -H "Content-Type: application/json" \
  -d '{"query": "how to build AI agents", "use_grounding": true}'

# Analyze a guide with Gemini
curl "http://localhost:8000/guides/OpenAI%3A%20GPT%20Best%20Practices/analyze"

# Analyze guide from URL
curl -X POST "http://localhost:8000/guides/analyze-url?url=https://example.com/guide.pdf"

# Compare multiple guides
curl -X POST "http://localhost:8000/guides/compare" \
  -H "Content-Type: application/json" \
  -d '{"guide_titles": ["OpenAI: GPT Best Practices", "Google: Introduction to Generative AI"]}'
```

## Architecture and Key Components

### Application Structure
- **main.py**: FastAPI application containing all endpoints and business logic
- **gemini_service.py**: Google Gemini AI integration for semantic search and analysis
- **Data Model**: Hardcoded list of dictionaries (`AI_GUIDES_DATA`) with guide metadata
- **Configuration**: Environment-based configuration loaded via python-dotenv
- **Deployment**: Multi-stage Docker build for optimized container size

### API Design
- RESTful endpoints following standard conventions
- JSON responses for all endpoints
- Proper HTTP status codes (200, 404, 500)
- OpenAPI documentation auto-generated at `/docs` and `/redoc`

### Key Technical Decisions
1. **Modular architecture**: Separate modules for API endpoints and Gemini integration
2. **Hardcoded data**: Guide data is embedded in the application (no database)
3. **Environment configuration**: Settings managed via .env file
4. **Docker security**: Runs as non-root user (`appuser`)
5. **Dual search implementation**: 
   - Standard: Case-insensitive substring matching
   - Gemini: Semantic search with grounding and relevance scoring
6. **AI Integration**: Google Gemini 2.0 Flash for enhanced capabilities

## Adding New Features

### Adding a New Guide
Add to the `AI_GUIDES_DATA` list in main.py:26:
```python
{
    "title": "New Guide Title",
    "publisher": "Publisher Name",
    "description": "Guide description",
    "topics": ["topic1", "topic2"],
    "download_url": "https://example.com/guide.pdf"
}
```

### Adding a New Endpoint
1. Define the endpoint function after existing endpoints
2. Use appropriate FastAPI decorators and type hints
3. Follow existing error handling patterns (HTTPException for 404/500)
4. Update this CLAUDE.md with the new endpoint details

### Implementing Data Persistence
To replace hardcoded data with a database:
1. Add database dependency (e.g., `sqlalchemy`, `asyncpg`)
2. Create models in a separate `models.py` file
3. Add database initialization in main.py
4. Update endpoints to query database instead of `AI_GUIDES_DATA`
5. Add migration scripts for schema management

## Common Development Tasks

### Adding Tests
Currently no tests exist. To add testing:
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Create test file
touch test_main.py

# Run tests
pytest
```

### Implementing Authentication
To add API key authentication:
1. Add `python-jose[cryptography]` to requirements.txt
2. Create middleware or dependency for API key validation
3. Apply to endpoints using FastAPI's dependency injection
4. Store API keys securely (environment variables or secrets manager)

### Performance Optimization
For better performance with large datasets:
1. Implement caching using `aiocache` or Redis
2. Add pagination to `/guides` endpoint
3. Create database indexes for search fields
4. Use async database drivers

## Environment Variables

All configurable via .env file:
- `UVICORN_HOST`: Server bind address (default: 0.0.0.0)
- `UVICORN_PORT`: Server port (default: 8000)
- `LOG_LEVEL`: Logging level (default: info)
- `APP_NAME`: Application name for health endpoint
- `APP_VERSION`: Application version for health endpoint
- `GEMINI_API_KEY`: Google Gemini API key (required for AI features)

## Gemini AI Features

### Semantic Search with Grounding
- Uses Gemini 2.0 Flash model for intelligent search
- Understands context and intent beyond keyword matching
- Returns relevance scores and reasoning for matches
- Endpoint: `POST /guides/search/gemini`

### Guide Analysis
- Generates enhanced summaries with learning objectives
- Estimates reading time and target audience
- Provides recommendations for related guides
- Endpoint: `GET /guides/{title}/analyze`

### URL Content Analysis
- Fetches and analyzes external guide content
- Extracts main topics and key takeaways
- Identifies prerequisites and practical applications
- Endpoint: `POST /guides/analyze-url`

### Guide Comparison
- Compares 2-5 guides simultaneously
- Identifies overlapping content and differences
- Suggests optimal reading order
- Recommends guides based on user expertise level
- Endpoint: `POST /guides/compare`

## Important Notes

- The `/guides/{title}` endpoint requires exact title matching (case-sensitive)
- URL-encode guide titles when making requests
- Docker container exposes port 8000 by default
- Standard search is case-insensitive substring matching
- Gemini features require valid API key in environment
- No rate limiting implemented (consider for production)
- Gemini endpoints may have longer response times due to AI processing