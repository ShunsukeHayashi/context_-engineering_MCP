#!/usr/bin/env python3
"""
Quick Start Example for Context Engineering Platform

This example demonstrates the basic usage of the Context Engineering API.
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

# API Base URL
API_BASE = "http://localhost:9001"

async def create_session(name: str) -> str:
    """Create a new context session"""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE}/api/sessions",
            params={"name": name, "description": "Quick start example"}
        ) as response:
            data = await response.json()
            print(f"✅ Created session: {data['name']} (ID: {data['session_id']})")
            return data['session_id']

async def create_context_window(session_id: str) -> str:
    """Create a context window in the session"""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE}/api/sessions/{session_id}/windows",
            json={"max_tokens": 4096, "reserved_tokens": 512}
        ) as response:
            data = await response.json()
            print(f"✅ Created context window: {data['window_id']}")
            return data['window_id']

async def add_context_elements(window_id: str):
    """Add some context elements"""
    elements = [
        {
            "content": "You are a helpful AI assistant focused on providing clear, concise answers.",
            "type": "system",
            "priority": 10
        },
        {
            "content": "Always explain your reasoning step by step.",
            "type": "system", 
            "priority": 8
        },
        {
            "content": "User: What is context engineering?",
            "type": "user",
            "priority": 5
        },
        {
            "content": "Context engineering is the practice of designing, managing, and optimizing the context provided to AI models to improve their performance, efficiency, and output quality.",
            "type": "assistant",
            "priority": 5
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        for element in elements:
            async with session.post(
                f"{API_BASE}/api/contexts/{window_id}/elements",
                json=element
            ) as response:
                data = await response.json()
                print(f"✅ Added element: {element['type']} (Tokens: {data['current_tokens']})")

async def analyze_context(window_id: str) -> Dict[str, Any]:
    """Analyze the context quality"""
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE}/api/contexts/{window_id}/analyze") as response:
            data = await response.json()
            print(f"\n📊 Context Analysis:")
            print(f"   Quality Score: {data['quality_score']:.2f}/100")
            print(f"   Metrics: {json.dumps(data['metrics'], indent=6)}")
            print(f"   Insights: {', '.join(data['insights'][:3])}")
            return data

async def optimize_context(window_id: str):
    """Optimize the context"""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE}/api/contexts/{window_id}/optimize",
            json={
                "goals": ["reduce_tokens", "improve_clarity"],
                "constraints": {"min_tokens": 50}
            }
        ) as response:
            data = await response.json()
            print(f"\n⚡ Started optimization: Task ID {data['task_id']}")
            print(f"   Status: {data['status']}")
            print(f"   Goals: {', '.join(data['goals'])}")

async def create_template():
    """Create a prompt template"""
    template_data = {
        "name": "Quick Start Template",
        "description": "A simple template for demonstrations",
        "template": "You are a {role} assistant. Your task is to {task}.\n\nContext: {context}\n\nPlease {action}.",
        "type": "completion",
        "category": "demo",
        "tags": ["example", "quickstart"]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE}/api/templates", json=template_data) as response:
            data = await response.json()
            print(f"\n📋 Created template: {data['name']} (ID: {data['template_id']})")
            print(f"   Variables: {', '.join(data['variables'])}")
            return data['template_id']

async def render_template(template_id: str):
    """Render the template with variables"""
    variables = {
        "role": "technical",
        "task": "explain complex concepts simply",
        "context": "The user is learning about AI",
        "action": "provide a clear explanation"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE}/api/templates/{template_id}/render",
            json={"template_id": template_id, "variables": variables}
        ) as response:
            data = await response.json()
            print(f"\n📝 Rendered template:")
            print(f"{data['rendered_content']}")

async def main():
    """Run the quick start example"""
    print("🚀 Context Engineering Platform - Quick Start Example\n")
    
    try:
        # 1. Create a session
        session_id = await create_session("Quick Start Session")
        
        # 2. Create a context window
        window_id = await create_context_window(session_id)
        
        # 3. Add context elements
        print(f"\n📝 Adding context elements...")
        await add_context_elements(window_id)
        
        # 4. Analyze the context
        await analyze_context(window_id)
        
        # 5. Optimize the context
        await optimize_context(window_id)
        
        # 6. Create and use a template
        template_id = await create_template()
        await render_template(template_id)
        
        print("\n✨ Quick start completed successfully!")
        print(f"\nNext steps:")
        print(f"1. View the dashboard at http://localhost:9001")
        print(f"2. Check the API docs at http://localhost:9001/docs")
        print(f"3. Try the MCP tools with Claude Desktop")
        
    except aiohttp.ClientError as e:
        print(f"\n❌ Error: Could not connect to the API server.")
        print(f"   Make sure the Context Engineering server is running on port 9001.")
        print(f"   Error details: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())