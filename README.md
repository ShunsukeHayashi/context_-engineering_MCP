# MCP AI Guides Server

A centralized repository and search interface for a curated collection of free AI-related guides published by OpenAI, Google, and Anthropic.

This server provides programmatic access to metadata about these guides, including their titles, publishers, descriptions, topics, and direct download links, covering subjects such as AI agent construction, prompt engineering, and enterprise-scale AI deployment.

## Features

*   **List all guides**: Retrieve a comprehensive list of all available AI guides.
*   **Search guides**: Filter guides based on keywords or topics in their title or description.
*   **Get guide details**: Access full metadata for a specific AI guide by its exact title.
*   **Get download URL**: Obtain the direct download link for a specific guide.
*   **Health Check**: Endpoint to verify server status.

## Prerequisites

*   Python 3.10+
*   pip (Python package installer)
*   Docker (optional, for containerized deployment)

## Setup and Running Locally

1.  **Clone the repository (if applicable)**:
    ```bash
    git clone <your-repo-url>
    cd mcp-ai-guides-server
    ```

2.  **Create a virtual environment (recommended)**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file**: Copy the contents from `.env.example` into a new file named `.env` in the project root.
    ```bash
    cp .env.example .env
    ```
    You can customize the values in `.env` if needed, e.g., for `UVICORN_PORT` or `LOG_LEVEL`.

5.  **Run the server**: 
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload  # Use --reload for development
    ```
    For production, omit `--reload` and ensure `UVICORN_HOST` and `UVICORN_PORT` are set correctly (e.g., via environment variables or `.env`).

The server will be accessible at `http://127.0.0.1:8000` (or `http://localhost:8000`).

## Running with Docker

1.  **Build the Docker image**:
    ```bash
    docker build -t mcp-ai-guides-server .
    ```

2.  **Run the Docker container**:
    ```bash
    docker run -d --name ai-guides-app -p 8000:8000 mcp-ai-guides-server
    ```
    The `-p 8000:8000` maps port 8000 of your host to port 8000 inside the container. The server will be accessible at `http://localhost:8000`.

## API Endpoints

All endpoints are prefixed with `/`. The OpenAPI documentation (Swagger UI) is available at `/docs` and ReDoc at `/redoc`.

*   **GET `/health`**
    *   **Description**: Simple health check to verify server status.
    *   **Example Response**:
        ```json
        {
          "status": "ok",
          "service": "MCP AI Guides Server",
          "version": "1.0.0"
        }
        ```

*   **GET `/guides`**
    *   **Description**: Lists all available AI guides.
    *   **Example Response**:
        ```json
        [
          {
            "title": "OpenAI: GPT Best Practices",
            "publisher": "OpenAI",
            "description": "Comprehensive guide on best practices for prompting and using GPT models effectively.",
            "topics": [
              "prompt engineering",
              "LLM usage",
              "AI best practices"
            ],
            "download_url": "https://example.com/openai-gpt-best-practices.pdf"
          }
          // ... more guides
        ]
        ```

*   **GET `/guides/search?query={keyword}`**
    *   **Description**: Searches for AI guides based on keywords or topics in their title or description.
    *   **Example**: `/guides/search?query=agent`
    *   **Example Response**:
        ```json
        [
          {
            "title": "OpenAI: AI Agent Construction Guidelines",
            "publisher": "OpenAI",
            "description": "A detailed guide on constructing robust and intelligent AI agents.",
            "topics": [
              "AI agents",
              "agent architecture",
              "AI development"
            ],
            "download_url": "https://example.com/openai-ai-agents.pdf"
          }
        ]
        ```

*   **GET `/guides/{title}`**
    *   **Description**: Retrieves the full details of a specific AI guide by its exact title.
    *   **Example**: `/guides/OpenAI%3A%20GPT%20Best%20Practices` (Note: URL-encode the title)
    *   **Example Response**:
        ```json
        {
          "title": "OpenAI: GPT Best Practices",
          "publisher": "OpenAI",
          "description": "Comprehensive guide on best practices for prompting and using GPT models effectively.",
          "topics": [
            "prompt engineering",
            "LLM usage",
            "AI best practices"
          ],
          "download_url": "https://example.com/openai-gpt-best-practices.pdf"
        }
        ```

*   **GET `/guides/{title}/download-url`**
    *   **Description**: Provides the direct download URL for a specific AI guide by its title.
    *   **Example**: `/guides/Google%3A%20Introduction%20to%20Generative%20AI/download-url`
    *   **Example Response**:
        ```json
        {
          "download_url": "https://example.com/google-intro-gen-ai.pdf"
        }
        ```

## Error Handling

*   **404 Not Found**: Returned if a specific guide is not found when requesting details or a download URL.
*   **500 Internal Server Error**: Returned for unexpected server issues, such as malformed data.

## Development

Feel free to extend the `AI_GUIDES_DATA` with more guides or implement a persistent storage solution (e.g., a database) if the collection grows large.
