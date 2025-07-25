# MCP Tools Usage Examples

This guide shows how to use the Context Engineering MCP tools in Claude Desktop.

## Setup

1. Add to your Claude Desktop config:
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

2. Restart Claude Desktop

## Basic Usage Examples

### 1. List AI Guides
```
Can you list all available AI guides?
```
Claude will use: `list_ai_guides`

### 2. Search for Specific Guides
```
Search for guides about prompt engineering
```
Claude will use: `search_ai_guides` with query "prompt engineering"

### 3. Semantic Search with AI
```
Find guides that explain how to build AI agents using natural language understanding
```
Claude will use: `search_guides_with_gemini` for semantic search

### 4. Analyze a Guide
```
Analyze the "OpenAI: GPT Best Practices" guide
```
Claude will use: `analyze_guide` with the guide title

## Context Engineering Examples

### 5. Create a New Session
```
Create a new context session for my chatbot project
```
Claude will use: `create_context_session`

### 6. Add Context Elements
```
Add a system prompt that says "You are a helpful customer service bot" to my context window
```
Claude will use: `add_context_element` with appropriate parameters

### 7. Analyze Context Quality
```
Analyze the quality of my current context window
```
Claude will use: `analyze_context`

### 8. Optimize Context
```
Optimize my context to reduce tokens while maintaining clarity
```
Claude will use: `optimize_context` with goals

### 9. Auto-Optimize
```
Automatically optimize my context with AI recommendations
```
Claude will use: `auto_optimize_context`

## Template Management Examples

### 10. Create a Template
```
Create a prompt template for customer support responses
```
Claude will use: `create_prompt_template`

### 11. Generate Template with AI
```
Generate a template for technical documentation writing
```
Claude will use: `generate_prompt_template`

### 12. List Templates
```
Show me all available prompt templates
```
Claude will use: `list_prompt_templates`

### 13. Render Template
```
Use the customer support template with these variables: name="John", issue="password reset"
```
Claude will use: `render_template` with variables

## Advanced Workflows

### 14. Complete Context Setup
```
Help me set up a complete context for a coding assistant:
1. Create a session called "Code Assistant"
2. Add a system prompt for Python expertise
3. Analyze the quality
4. Optimize if needed
```
Claude will chain multiple tools together

### 15. Template-Based Context Creation
```
Create a chatbot using the "Expert Roleplay" template for a medical assistant
```
Claude will:
1. List templates to find the right one
2. Render it with appropriate variables
3. Create a context window
4. Add the rendered content

## Tips for Best Results

1. **Be specific** - The more details you provide, the better the tools work
2. **Chain operations** - Claude can use multiple tools in sequence
3. **Check status** - Use `get_context_stats` to see system status
4. **Iterate** - Analyze, optimize, and improve your contexts

## Troubleshooting

If tools aren't working:
1. Check that both servers are running (API on 9001, MCP on stdio)
2. Verify your Claude Desktop config
3. Restart Claude Desktop after config changes
4. Check server logs for errors