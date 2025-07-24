#!/bin/bash

# Set the API URL (defaults to localhost:8888)
export AI_GUIDES_API_URL="${AI_GUIDES_API_URL:-http://localhost:8888}"

# Change to MCP server directory
cd "$(dirname "$0")/mcp-server"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..." >&2
    npm install >&2
fi

# Run the MCP server
exec node index.js