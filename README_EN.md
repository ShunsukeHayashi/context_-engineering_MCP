# 🧠 Context Engineering MCP Platform

A comprehensive AI-powered Context Engineering platform that goes beyond simple AI guide retrieval to provide complete context management, optimization, and prompt engineering capabilities.

## ✨ Key Features

### 📚 AI Guides Management
- **Complete Guide List**: Access comprehensive metadata for AI guides from OpenAI, Google, and Anthropic
- **Search Capabilities**: Filter guides by keywords, topics, and descriptions
- **Semantic Search**: Gemini AI-powered semantic understanding for better search results
- **Guide Analysis**: Detailed analysis with learning objectives generation
- **Guide Comparison**: Compare multiple guides side-by-side

### 🔧 Context Engineering System
- **Context Windows Management**: Create and manage context windows with token tracking
- **Context Analysis**: AI-powered quality evaluation with semantic consistency checks
- **Optimization Engine**: Automatic optimization for token reduction, clarity, and relevance
- **Multi-modal Support**: Handle text, images, audio, video, and documents
- **RAG Integration**: Retrieval-Augmented Generation context management

### 📋 Prompt Template Management
- **Template Creation**: Create and manage reusable prompt templates
- **AI Generation**: Automatically generate templates based on purpose and examples
- **Version Control**: Track template usage and quality scores
- **Template Rendering**: Dynamic variable substitution

### 🤖 MCP Server Integration
- **Claude Desktop Support**: Full MCP protocol integration
- **15 Comprehensive Tools**: Complete toolset for context engineering
- **Real-time Updates**: WebSocket support for live updates

### 📊 Workflow Management
- **Automatic Workflow Generation**: Create workflows from natural language input
- **Intelligent Task Decomposition**: AI-powered task breakdown
- **Agent Management**: Automatic assignment based on capabilities
- **Real-time Visualization**: Beautiful dashboard for progress tracking

## 🛠️ Prerequisites

- Python 3.10+
- Node.js 16+ (for MCP server)
- Google Gemini API key
- Docker (optional, for containerized deployment)

## 🚀 Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ShunsukeHayashi/context_-engineering_MCP.git
cd "context engineering_mcp_server"
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env file to add your GEMINI_API_KEY
```

### 3. Install Dependencies

#### For AI Guides API Server
```bash
pip install -r requirements.txt
```

#### For Context Engineering System
```bash
cd context_engineering
python -m venv context_env
source context_env/bin/activate  # Windows: context_env\Scripts\activate
pip install -r requirements.txt
```

#### For MCP Server
```bash
cd mcp-server
npm install
```

## 🌐 Running the Platform

### 1. AI Guides API Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8888 --reload
```

### 2. Context Engineering API Server
```bash
cd context_engineering
./start_context_engineering.sh
```

### 3. MCP Server (for Claude Desktop)
```bash
cd mcp-server
node context_mcp_server.js
```

## 🌍 Access Points

### AI Guides API
- **API Server**: http://localhost:8888
- **API Documentation**: http://localhost:8888/docs
- **ReDoc**: http://localhost:8888/redoc

### Context Engineering Platform
- **Dashboard**: http://localhost:9001
- **API Documentation**: http://localhost:9001/docs
- **WebSocket**: ws://localhost:9001/ws

### MCP Server Configuration
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

## 📡 API Endpoints

### AI Guides Endpoints

#### Basic Endpoints
- `GET /guides` - List all AI guides
- `GET /guides/search?query={keyword}` - Search guides
- `GET /guides/{title}` - Get guide details
- `GET /guides/{title}/download-url` - Get download URL

#### Gemini-Enhanced Endpoints
- `POST /guides/search/gemini` - Semantic search
- `GET /guides/{title}/analyze` - Analyze guide
- `POST /guides/analyze-url` - Analyze external URL
- `POST /guides/compare` - Compare multiple guides

### Context Engineering Endpoints

#### Session Management
- `POST /api/sessions` - Create new session
- `GET /api/sessions` - List sessions
- `GET /api/sessions/{session_id}` - Get session details

#### Context Windows
- `POST /api/sessions/{session_id}/windows` - Create context window
- `POST /api/contexts/{window_id}/elements` - Add context element
- `GET /api/contexts/{window_id}` - Get context window
- `POST /api/contexts/{window_id}/analyze` - Analyze context

#### Optimization
- `POST /api/contexts/{window_id}/optimize` - Optimize context
- `POST /api/contexts/{window_id}/auto-optimize` - Auto-optimize
- `GET /api/optimization/{task_id}` - Get optimization status

#### Template Management
- `POST /api/templates` - Create template
- `POST /api/templates/generate` - Generate template with AI
- `GET /api/templates` - List templates
- `POST /api/templates/{template_id}/render` - Render template

## 🧰 MCP Tools (15 Available)

### AI Guides Tools (4)
1. **list_ai_guides** - List all AI guides
2. **search_ai_guides** - Search guides by keyword
3. **search_guides_with_gemini** - Semantic search with Gemini
4. **analyze_guide** - Analyze specific guide

### Context Engineering Tools (7)
5. **create_context_session** - Create new context session
6. **create_context_window** - Create context window
7. **add_context_element** - Add element to context
8. **analyze_context** - Analyze context quality
9. **optimize_context** - Optimize context window
10. **auto_optimize_context** - Automatic optimization
11. **get_context_stats** - Get system statistics

### Template Management Tools (4)
12. **create_prompt_template** - Create new template
13. **generate_prompt_template** - AI-generate template
14. **list_prompt_templates** - List available templates
15. **render_template** - Render template with variables

## 🎯 Usage Examples

### Basic AI Guide Search
```bash
curl "http://localhost:8888/guides/search?query=agent"
```

### Semantic Search with Gemini
```bash
curl -X POST "http://localhost:8888/guides/search/gemini" \
  -H "Content-Type: application/json" \
  -d '{"query": "How to build AI agents", "use_grounding": true}'
```

### Create Context Session
```bash
curl -X POST "http://localhost:9001/api/sessions" \
  -H "Content-Type: application/json" \
  -d '{"name": "My AI Project", "description": "Context for chatbot development"}'
```

### Add Context Element
```bash
curl -X POST "http://localhost:9001/api/contexts/{window_id}/elements" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "You are a helpful AI assistant...",
    "type": "system",
    "priority": 10
  }'
```

### Optimize Context
```bash
curl -X POST "http://localhost:9001/api/contexts/{window_id}/optimize" \
  -H "Content-Type: application/json" \
  -d '{
    "goals": ["reduce_tokens", "improve_clarity"],
    "constraints": {"min_tokens": 100}
  }'
```

## 📊 System Architecture

### Core Components
- **main.py**: FastAPI main application for AI guides
- **gemini_service.py**: Gemini AI integration service
- **context_engineering/**: Complete context engineering system
  - **context_models.py**: Data models for context management
  - **context_analyzer.py**: AI-powered context analysis
  - **context_optimizer.py**: Context optimization engine
  - **template_manager.py**: Prompt template management
  - **context_api.py**: FastAPI server for context engineering
- **mcp-server/**: MCP server implementations
  - **index.js**: Basic AI guides MCP server
  - **context_mcp_server.js**: Full context engineering MCP server

### Pre-defined Templates (5)
1. **Basic Q&A** - Simple question-answer format
2. **Expert Roleplay** - Specialized expert responses
3. **Step-by-Step Thinking** - Chain of thought reasoning
4. **Few-Shot Learning** - Example-based learning
5. **Code Generation** - Programming task templates

## 🔧 Docker Deployment

### Build Docker Image
```bash
docker build -t context-engineering-platform .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

## 🚀 Performance Optimization

- Gemini API rate limiting consideration
- Token usage optimization
- WebSocket connection management
- Caching for frequently accessed data

## 🤝 Contributing

This project is open source. We welcome issue reports and pull requests.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Start development servers
uvicorn main:app --reload  # AI Guides
cd context_engineering && python context_api.py  # Context Engineering
```

## 📄 License

MIT License - See LICENSE file for details.

## 🆘 Support

If you encounter issues:
1. Report bugs in [Issues](https://github.com/ShunsukeHayashi/context_-engineering_MCP/issues)
2. Ask questions in [Discussions](https://github.com/ShunsukeHayashi/context_-engineering_MCP/discussions)
3. 📧 Contact the developer directly

---

**🤖 This project was enhanced with Claude Code**

A complete Context Engineering platform that handles everything from AI guide management to advanced context optimization, prompt engineering, and real-time workflow visualization.