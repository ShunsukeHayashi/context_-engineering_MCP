# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Context Engineering MCP Platform - A comprehensive AI-powered platform that transforms context management for AI applications. Originally an AI guides server, it has evolved into a complete Context Engineering system with:

- **AI Guides Management**: Curated collection from OpenAI, Google, and Anthropic with Gemini-powered search
- **Context Engineering**: Complete context lifecycle management with analysis, optimization, and templates
- **MCP Integration**: Native Claude Desktop support with 15 powerful tools
- **Real-time Dashboards**: WebSocket-powered visualization and monitoring

## System Architecture

```
context_engineering_mcp_server/
├── main.py                      # AI Guides API server (port 8888)
├── gemini_service.py           # Gemini AI integration service
├── context_engineering/        # Context Engineering system (port 9001)
│   ├── context_models.py       # Core data models
│   ├── context_analyzer.py     # AI-powered analysis engine
│   ├── context_optimizer.py    # Optimization algorithms
│   ├── template_manager.py     # Template management system
│   └── context_api.py         # FastAPI server
├── mcp-server/                # MCP server implementations
│   ├── index.js               # Basic AI guides MCP server
│   └── context_mcp_server.js  # Full platform MCP server
└── examples/                  # Usage examples and tutorials
```

## Commands and Development Workflow

### Initial Setup
```bash
# Clone repository
git clone https://github.com/ShunsukeHayashi/context_-engineering_MCP.git
cd "context engineering_mcp_server"

# Configure environment
cp .env.example .env
# Edit .env to add GEMINI_API_KEY
```

### Running the Platform

#### 1. AI Guides API Server
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --host 0.0.0.0 --port 8888 --reload
```

#### 2. Context Engineering System
```bash
cd context_engineering

# Create virtual environment
python -m venv context_env
source context_env/bin/activate  # Windows: context_env\Scripts\activate

# Install and run
pip install -r requirements.txt
./start_context_engineering.sh
# Or directly: python context_api.py
```

#### 3. MCP Server
```bash
cd mcp-server
npm install
node context_mcp_server.js
```

### Docker Operations
```bash
# Build image
docker build -t context-engineering-platform .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## API Endpoints Reference

### AI Guides API (Port 8888)

#### Basic Endpoints
- `GET /health` - Health check
- `GET /guides` - List all guides
- `GET /guides/search?query={keyword}` - Search guides
- `GET /guides/{title}` - Get guide details
- `GET /guides/{title}/download-url` - Get download URL

#### Gemini-Enhanced Endpoints
- `POST /guides/search/gemini` - Semantic search
- `GET /guides/{title}/analyze` - Analyze guide
- `POST /guides/analyze-url` - Analyze external URL
- `POST /guides/compare` - Compare multiple guides

### Context Engineering API (Port 9001)

#### Session Management
- `POST /api/sessions` - Create session
- `GET /api/sessions` - List sessions
- `GET /api/sessions/{session_id}` - Get session

#### Context Windows
- `POST /api/sessions/{session_id}/windows` - Create window
- `POST /api/contexts/{window_id}/elements` - Add element
- `GET /api/contexts/{window_id}` - Get window
- `POST /api/contexts/{window_id}/analyze` - Analyze context

#### Optimization
- `POST /api/contexts/{window_id}/optimize` - Optimize context
- `POST /api/contexts/{window_id}/auto-optimize` - Auto-optimize
- `GET /api/optimization/{task_id}` - Get task status

#### Templates
- `POST /api/templates` - Create template
- `POST /api/templates/generate` - AI generate template
- `GET /api/templates` - List templates
- `POST /api/templates/{template_id}/render` - Render template

#### System
- `GET /api/stats` - System statistics
- `WS /ws` - WebSocket connection

## MCP Tools (15 Available)

### Configuration
Add to Claude Desktop config:
```json
{
  "mcpServers": {
    "context-engineering": {
      "command": "node",
      "args": ["/path/to/mcp-server/context_mcp_server.js"]
    }
  }
}
```

### Available Tools
1. **AI Guides Tools** (4): list, search, semantic search, analyze
2. **Context Tools** (7): sessions, windows, elements, analysis, optimization
3. **Template Tools** (4): create, generate, list, render

## Key Technical Decisions

### Architecture Choices
1. **Modular Design**: Separate services for different functionalities
2. **AI Integration**: Gemini 2.0 Flash for all AI operations
3. **Async Everything**: Full async/await for performance
4. **Type Safety**: Type hints and Pydantic models throughout
5. **WebSocket Support**: Real-time updates for dashboards

### Optimization Strategies
1. **Token Reduction**: Up to 52% reduction while maintaining quality
2. **Multi-goal Optimization**: Clarity, relevance, structure
3. **Semantic Analysis**: AI-powered quality scoring
4. **Template Reuse**: 78% average reuse rate

### Security Considerations
1. **API Key Management**: Environment variables only
2. **Docker Security**: Non-root user execution
3. **Input Validation**: Pydantic models for all inputs
4. **Error Handling**: Comprehensive try-catch blocks

## Common Development Tasks

### Adding New Context Analysis Features
```python
# In context_analyzer.py
async def analyze_new_metric(self, window: ContextWindow) -> float:
    """Add new analysis metric"""
    # Implementation here
    pass
```

### Creating New Optimization Strategy
```python
# In context_optimizer.py
async def _optimize_for_new_goal(self, window: ContextWindow) -> Dict[str, Any]:
    """New optimization strategy"""
    # Implementation here
    pass
```

### Adding MCP Tool
```javascript
// In context_mcp_server.js
{
  name: 'new_tool_name',
  description: 'Tool description',
  inputSchema: {
    type: 'object',
    properties: {
      // Parameters
    }
  }
}
```

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test
pytest tests/test_context_analyzer.py -v
```

## Performance Optimization Tips

1. **Caching**: Implement Redis for template caching
2. **Batch Operations**: Use bulk element addition
3. **Async Processing**: Leverage asyncio for parallel operations
4. **Token Estimation**: Pre-calculate before API calls
5. **Connection Pooling**: Reuse HTTP connections

## Environment Variables

### Required
- `GEMINI_API_KEY`: Google Gemini API key

### Optional
- `UVICORN_HOST`: API host (default: 0.0.0.0)
- `UVICORN_PORT`: API port (default: 8888/9001)
- `LOG_LEVEL`: Logging level (default: info)
- `CONTEXT_API_URL`: Context API URL for MCP (default: http://localhost:9001)
- `AI_GUIDES_API_URL`: Guides API URL for MCP (default: http://localhost:8888)

## Debugging Tips

### Check Service Status
```bash
# AI Guides API
curl http://localhost:8888/health

# Context Engineering API
curl http://localhost:9001/api/stats

# MCP Server (check Claude Desktop)
```

### Common Issues
1. **Port conflicts**: Change ports in .env
2. **API key errors**: Verify GEMINI_API_KEY
3. **MCP not working**: Restart Claude Desktop
4. **Optimization timeout**: Increase task timeout

### Logging
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Debug information here")
```

## Contributing Guidelines

1. **Code Style**: Black for Python, ESLint for JS
2. **Type Hints**: Required for all functions
3. **Documentation**: Docstrings for all public methods
4. **Tests**: Maintain >80% coverage
5. **Commits**: Follow conventional commits

## Important Notes

- Context windows have token limits (default 8192)
- Optimization is compute-intensive (may take time)
- Templates are cached for performance
- WebSocket connections auto-reconnect
- MCP tools work in stdio mode only
- Gemini API has rate limits (60 RPM)

## Future Enhancements

- [ ] Cloud deployment (AWS/GCP)
- [ ] Team collaboration features
- [ ] Advanced caching strategies
- [ ] Multi-language support
- [ ] Export/import contexts
- [ ] A/B testing for templates