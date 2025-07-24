# AI Guides MCP Server

This is an MCP (Model Context Protocol) server that provides access to the AI Guides API, including Gemini-powered semantic search and analysis features.

## Setup

1. Make sure the AI Guides API server is running:
   ```bash
   cd ..
   uvicorn main:app --port 8888
   ```

2. The MCP server has been added to your Claude Desktop configuration.

3. Restart Claude Desktop to load the new MCP server.

## Available Tools

Once loaded in Claude Desktop, you'll have access to these tools:

### Basic Tools
- `list_ai_guides` - List all available AI guides
- `search_ai_guides` - Search guides by keyword
- `get_guide_details` - Get details of a specific guide
- `get_guide_download_url` - Get download URL for a guide

### Gemini-Enhanced Tools
- `search_guides_with_gemini` - Semantic search using Gemini AI
- `analyze_guide` - Analyze a guide with Gemini
- `analyze_guide_url` - Analyze external guide content
- `compare_guides` - Compare multiple guides

## Usage Example

In Claude Desktop, you can now use these tools directly:

```
"Search for guides about AI agents"
"Analyze the OpenAI GPT Best Practices guide"
"Compare OpenAI and Google AI guides"
```

## Configuration

The MCP server connects to the API server at `http://localhost:8888` by default. You can change this by setting the `AI_GUIDES_API_URL` environment variable in the Claude Desktop configuration.