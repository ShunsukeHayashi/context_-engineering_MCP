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
context_engineering_MCP/
├── main.py                      # AI Guides API server (port 8888)
├── gemini_service.py           # Gemini AI integration service
├── scripts/                    # Convenience scripts for common tasks
│   ├── quickstart.sh           # Full platform setup
│   ├── start_context_engineering.sh  # Context Engineering system
│   ├── run-mcp-server.sh       # MCP server startup
│   ├── test-mcp.sh            # MCP server testing
│   └── start_workflow_system.sh # Workflow system
├── context_engineering/        # Context Engineering system (port 9001)
│   ├── context_models.py       # Core data models (Pydantic/dataclass)
│   ├── context_analyzer.py     # AI-powered context analysis
│   ├── context_optimizer.py    # Multi-strategy optimization
│   ├── template_manager.py     # Template CRUD and rendering
│   ├── context_api.py          # FastAPI server
│   └── templates/              # Stored prompt templates
├── mcp-server/                 # MCP server implementations
│   ├── index.js                # Basic AI guides MCP server
│   ├── context_mcp_server.js   # Full platform MCP server (15 tools)
│   └── package.json            # Node.js dependencies
├── workflow_system/            # Workflow automation (experimental)
├── examples/                   # Usage examples and tutorials
└── requirements.txt            # Unified Python dependencies
```

## Commands and Development Workflow

### Initial Setup
```bash
# Clone repository
git clone https://github.com/ShunsukeHayashi/context_-engineering_MCP.git
cd context_engineering_MCP

# Configure environment
cp .env.example .env
# Edit .env to add GEMINI_API_KEY
```

### Running the Platform

#### Quick Start (Recommended)
```bash
# Use the convenience script for full setup
./scripts/quickstart.sh
```

#### Manual Setup

##### 1. AI Guides API Server (Port 8888)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run AI Guides server
uvicorn main:app --host 0.0.0.0 --port 8888 --reload
```

##### 2. Context Engineering System (Port 9001)
```bash
# Use the setup script
./scripts/start_context_engineering.sh

# Or run manually
cd context_engineering
python -m venv context_env
source context_env/bin/activate  # Windows: context_env\Scripts\activate
pip install -r ../requirements.txt
python context_api.py
```

##### 3. MCP Server
```bash
# Use the MCP server script
./scripts/run-mcp-server.sh

# Or run manually
cd mcp-server
npm install
node context_mcp_server.js
```

##### 4. Workflow System (Optional, Port varies)
```bash
./scripts/start_workflow_system.sh
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_context_analyzer.py -v

# Test MCP server
./scripts/test-mcp.sh
```

### Linting and Formatting
```bash
# Python formatting
black .
isort .

# Python linting
ruff check .

# Node.js (MCP server)
cd mcp-server
npm run lint
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

## Architecture & Technical Decisions

### Core Architecture Patterns
1. **Multi-Service Design**: Three independent FastAPI services (AI Guides, Context Engineering, Workflow)
2. **MCP Protocol Integration**: Native Claude Desktop support with stdio transport
3. **Async-First Design**: All I/O operations use asyncio for high concurrency
4. **Type Safety**: Comprehensive type hints with Pydantic models and dataclasses
5. **WebSocket Real-time**: Live updates for context optimization progress

### Data Models Architecture
The system uses a layered data model approach:
- **ContextElement**: Basic building blocks with content, type, priority
- **ContextWindow**: Collections of elements with token management
- **ContextSession**: High-level groupings for project organization
- **PromptTemplate**: Reusable components with variable substitution
- **OptimizationTask**: Async task tracking for long-running operations

### AI Integration Strategy
- **Single AI Provider**: Gemini 2.0 Flash for all AI operations (analysis, optimization, generation)
- **Prompt Engineering**: Specialized prompts for different analysis types
- **Rate Limiting**: Built-in respect for Gemini API limits (60 RPM)
- **Error Recovery**: Graceful degradation when AI services are unavailable

### Optimization Engine Design
Multi-strategy optimization with measurable goals:
- **Token Reduction**: Remove redundancy while preserving meaning
- **Clarity Enhancement**: Improve instruction precision
- **Relevance Boosting**: Prioritize important information
- **Structure Improvement**: Logical flow optimization

## Prompt Engineering Architecture

### Template System Design
The platform uses a sophisticated template management system with the following hierarchy:

#### Template Types (PromptTemplateType Enum)
- **COMPLETION**: Basic completion prompts
- **CHAT**: Conversational chat templates
- **INSTRUCT**: Instruction-based prompts
- **FEWSHOT**: Few-shot learning templates
- **CHAIN_OF_THOUGHT**: Step-by-step reasoning prompts
- **ROLEPLAY**: Role-based interaction templates

#### Template Components
```python
class PromptTemplate:
    id: str                    # Unique identifier
    name: str                  # Human-readable name
    description: str           # Template purpose
    template: str              # Template with {variables}
    variables: List[str]       # Required variables list
    type: PromptTemplateType   # Template category
    category: str              # Grouping (qa, expert, code, etc.)
    tags: List[str]           # Searchable tags
    usage_count: int          # Analytics tracking
    quality_score: float      # AI-evaluated quality (0-100)
```

#### Pre-built Templates
The system includes 5 default templates:
1. **基本的な質問応答** - Simple Q&A format
2. **専門家ロールプレイ** - Expert role-based responses
3. **段階的思考プロセス** - Chain of thought reasoning
4. **Few-Shot学習** - Example-based learning
5. **コード生成** - Programming task templates

### Context Analysis Engine

#### Analysis Metrics
The ContextAnalyzer evaluates contexts across multiple dimensions:

```python
# Basic Metrics
- total_elements: Number of context elements
- total_tokens: Current token count
- token_utilization: Percentage of max tokens used
- avg_element_length: Average content length

# Structure Analysis
- element_type_distribution: Distribution of element types
- priority_distribution: Priority level analysis
- role_diversity: Variety of roles represented

# Semantic Analysis (AI-powered)
- semantic_consistency: How well ideas flow together
- information_density: Information per token ratio
- clarity_score: Readability assessment
- relevance_mapping: Content relevance to purpose
```

#### Quality Assessment Process
1. **Quantitative Analysis**: Token counts, distributions, ratios
2. **AI Semantic Analysis**: Gemini 2.0 evaluates meaning and flow
3. **Quality Scoring**: Combined score (0-100) with specific issues
4. **Recommendations**: Actionable improvement suggestions

### Optimization Strategies

#### Multi-Goal Optimization
The optimizer can target multiple goals simultaneously:

```python
# Available Optimization Goals
- "reduce_tokens": Minimize token usage while preserving meaning
- "improve_clarity": Enhance readability and understanding
- "increase_relevance": Focus on most important information
- "enhance_structure": Improve logical flow and organization
- "boost_specificity": Add concrete details and examples
```

#### Optimization Process
1. **Analysis Phase**: Comprehensive context evaluation
2. **Strategy Selection**: AI chooses optimal approaches
3. **Content Transformation**: Apply selected optimizations
4. **Validation**: Ensure quality maintained or improved
5. **Metrics Reporting**: Before/after comparison

## Common Development Tasks

### Adding New Template Types
```python
# In context_models.py
class PromptTemplateType(Enum):
    NEW_TYPE = "new_type"

# In template_manager.py - _initialize_default_templates()
{
    "name": "New Template Type",
    "description": "Description of the new template",
    "template": "Template with {variables}",
    "type": PromptTemplateType.NEW_TYPE,
    "category": "category_name",
    "tags": ["tag1", "tag2"]
}
```

### Adding Analysis Metrics
```python
# In context_analyzer.py
def _calculate_new_metric(self, window: ContextWindow) -> Dict[str, float]:
    """Add new analysis metric"""
    # Calculate your metric
    return {"new_metric_name": metric_value}

# Add to analyze_context_window()
new_metrics = self._calculate_new_metric(window)
analysis.metrics.update(new_metrics)
```

### Creating Optimization Strategies
```python
# In context_optimizer.py
async def _optimize_for_new_goal(self, window: ContextWindow) -> Dict[str, Any]:
    """New optimization strategy"""
    # Implement optimization logic
    return {
        "optimized_elements": modified_elements,
        "metrics": improvement_metrics,
        "explanation": "What was changed and why"
    }
```

### Adding MCP Tools
```javascript
// In context_mcp_server.js
{
  name: 'new_context_tool',
  description: 'Description of what the tool does',
  inputSchema: {
    type: 'object',
    properties: {
      window_id: { type: 'string', description: 'Context window ID' },
      custom_param: { type: 'string', description: 'Custom parameter' }
    },
    required: ['window_id']
  }
}
```

### Development and Testing
```bash
# Install development dependencies (included in requirements.txt)
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_context_analyzer.py -v

# Test MCP server
./scripts/test-mcp.sh
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