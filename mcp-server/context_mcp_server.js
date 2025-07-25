#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fetch from 'node-fetch';

const CONTEXT_API_URL = process.env.CONTEXT_API_URL || 'http://localhost:9001';
const AI_GUIDES_API_URL = process.env.AI_GUIDES_API_URL || 'http://localhost:8888';

class ContextEngineeringMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'context-engineering-mcp-server',
        version: '2.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupHandlers();
  }

  async makeRequest(baseUrl, endpoint, options = {}) {
    try {
      const url = `${baseUrl}${endpoint}`;
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Request failed: ${error.message}`);
    }
  }

  setupHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        // AI Guides Tools
        {
          name: 'list_ai_guides',
          description: 'List all available AI guides from OpenAI, Google, and Anthropic',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
        {
          name: 'search_ai_guides',
          description: 'Search for AI guides by keyword',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'The keyword to search for',
              },
            },
            required: ['query'],
          },
        },
        {
          name: 'search_guides_with_gemini',
          description: 'Search guides using Gemini AI semantic search',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'The search query',
              },
              use_grounding: {
                type: 'boolean',
                description: 'Whether to use Gemini grounding',
                default: true,
              },
            },
            required: ['query'],
          },
        },
        {
          name: 'analyze_guide',
          description: 'Analyze a guide using Gemini AI',
          inputSchema: {
            type: 'object',
            properties: {
              title: {
                type: 'string',
                description: 'The exact title of the AI guide to analyze',
              },
            },
            required: ['title'],
          },
        },
        
        // Context Engineering Tools
        {
          name: 'create_context_session',
          description: 'Create a new context engineering session',
          inputSchema: {
            type: 'object',
            properties: {
              name: {
                type: 'string',
                description: 'Session name',
                default: 'New Context Session',
              },
              description: {
                type: 'string',
                description: 'Session description',
                default: '',
              },
            },
          },
        },
        {
          name: 'create_context_window',
          description: 'Create a new context window in a session',
          inputSchema: {
            type: 'object',
            properties: {
              session_id: {
                type: 'string',
                description: 'The session ID',
              },
              max_tokens: {
                type: 'integer',
                description: 'Maximum tokens for the context window',
                default: 8192,
              },
              reserved_tokens: {
                type: 'integer',
                description: 'Reserved tokens for response',
                default: 512,
              },
            },
            required: ['session_id'],
          },
        },
        {
          name: 'add_context_element',
          description: 'Add an element to a context window',
          inputSchema: {
            type: 'object',
            properties: {
              window_id: {
                type: 'string',
                description: 'The context window ID',
              },
              content: {
                type: 'string',
                description: 'The content to add',
              },
              type: {
                type: 'string',
                description: 'Element type',
                enum: ['system', 'user', 'assistant', 'function', 'tool', 'multimodal'],
                default: 'user',
              },
              priority: {
                type: 'integer',
                description: 'Priority (1-10, higher is more important)',
                default: 5,
              },
              tags: {
                type: 'array',
                items: { type: 'string' },
                description: 'Tags for the element',
                default: [],
              },
            },
            required: ['window_id', 'content'],
          },
        },
        {
          name: 'analyze_context',
          description: 'Analyze a context window for quality and optimization opportunities',
          inputSchema: {
            type: 'object',
            properties: {
              window_id: {
                type: 'string',
                description: 'The context window ID to analyze',
              },
            },
            required: ['window_id'],
          },
        },
        {
          name: 'optimize_context',
          description: 'Optimize a context window using AI',
          inputSchema: {
            type: 'object',
            properties: {
              window_id: {
                type: 'string',
                description: 'The context window ID to optimize',
              },
              goals: {
                type: 'array',
                items: {
                  type: 'string',
                  enum: ['reduce_tokens', 'improve_clarity', 'enhance_relevance', 'remove_redundancy', 'improve_structure'],
                },
                description: 'Optimization goals',
                default: ['reduce_tokens', 'improve_clarity'],
              },
            },
            required: ['window_id'],
          },
        },
        {
          name: 'auto_optimize_context',
          description: 'Automatically optimize context with AI recommendations',
          inputSchema: {
            type: 'object',
            properties: {
              window_id: {
                type: 'string',
                description: 'The context window ID to auto-optimize',
              },
            },
            required: ['window_id'],
          },
        },
        {
          name: 'create_prompt_template',
          description: 'Create a new prompt template',
          inputSchema: {
            type: 'object',
            properties: {
              name: {
                type: 'string',
                description: 'Template name',
              },
              description: {
                type: 'string',
                description: 'Template description',
              },
              template: {
                type: 'string',
                description: 'Template content with {variables}',
              },
              type: {
                type: 'string',
                enum: ['completion', 'chat', 'instruct', 'fewshot', 'chain_of_thought', 'roleplay'],
                description: 'Template type',
                default: 'completion',
              },
              category: {
                type: 'string',
                description: 'Template category',
                default: 'general',
              },
              tags: {
                type: 'array',
                items: { type: 'string' },
                description: 'Template tags',
                default: [],
              },
            },
            required: ['name', 'description', 'template'],
          },
        },
        {
          name: 'generate_prompt_template',
          description: 'Generate a prompt template using AI',
          inputSchema: {
            type: 'object',
            properties: {
              purpose: {
                type: 'string',
                description: 'The purpose of the template',
              },
              examples: {
                type: 'array',
                items: { type: 'string' },
                description: 'Example outputs',
                default: [],
              },
              constraints: {
                type: 'array',
                items: { type: 'string' },
                description: 'Constraints for the template',
                default: [],
              },
            },
            required: ['purpose'],
          },
        },
        {
          name: 'list_prompt_templates',
          description: 'List available prompt templates',
          inputSchema: {
            type: 'object',
            properties: {
              category: {
                type: 'string',
                description: 'Filter by category',
              },
              tags: {
                type: 'string',
                description: 'Filter by tags (comma-separated)',
              },
            },
          },
        },
        {
          name: 'render_template',
          description: 'Render a prompt template with variables',
          inputSchema: {
            type: 'object',
            properties: {
              template_id: {
                type: 'string',
                description: 'The template ID',
              },
              variables: {
                type: 'object',
                description: 'Variables to substitute in the template',
              },
            },
            required: ['template_id', 'variables'],
          },
        },
        {
          name: 'get_context_stats',
          description: 'Get statistics about the context engineering system',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          // AI Guides Tools
          case 'list_ai_guides': {
            const guides = await this.makeRequest(AI_GUIDES_API_URL, '/guides');
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(guides, null, 2),
                },
              ],
            };
          }

          case 'search_ai_guides': {
            const guides = await this.makeRequest(AI_GUIDES_API_URL, `/guides/search?query=${encodeURIComponent(args.query)}`);
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(guides, null, 2),
                },
              ],
            };
          }

          case 'search_guides_with_gemini': {
            const result = await this.makeRequest(AI_GUIDES_API_URL, '/guides/search/gemini', {
              method: 'POST',
              body: JSON.stringify({
                query: args.query,
                use_grounding: args.use_grounding ?? true,
              }),
            });
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(result, null, 2),
                },
              ],
            };
          }

          case 'analyze_guide': {
            const result = await this.makeRequest(AI_GUIDES_API_URL, `/guides/${encodeURIComponent(args.title)}/analyze`);
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(result, null, 2),
                },
              ],
            };
          }

          // Context Engineering Tools
          case 'create_context_session': {
            const result = await this.makeRequest(CONTEXT_API_URL, '/api/sessions', {
              method: 'POST',
              body: JSON.stringify({
                name: args.name || 'New Context Session',
                description: args.description || '',
              }),
            });
            return {
              content: [
                {
                  type: 'text',
                  text: `Created context session: ${result.name} (ID: ${result.session_id})`,
                },
              ],
            };
          }

          case 'create_context_window': {
            const result = await this.makeRequest(CONTEXT_API_URL, `/api/sessions/${args.session_id}/windows`, {
              method: 'POST',
              body: JSON.stringify({
                max_tokens: args.max_tokens || 8192,
                reserved_tokens: args.reserved_tokens || 512,
              }),
            });
            return {
              content: [
                {
                  type: 'text',
                  text: `Created context window: ${result.window_id} (Max tokens: ${result.max_tokens})`,
                },
              ],
            };
          }

          case 'add_context_element': {
            const result = await this.makeRequest(CONTEXT_API_URL, `/api/contexts/${args.window_id}/elements`, {
              method: 'POST',
              body: JSON.stringify({
                content: args.content,
                type: args.type || 'user',
                priority: args.priority || 5,
                tags: args.tags || [],
              }),
            });
            return {
              content: [
                {
                  type: 'text',
                  text: `Added element to context window. Current tokens: ${result.current_tokens} (${result.utilization_ratio.toFixed(2)}% utilization)`,
                },
              ],
            };
          }

          case 'analyze_context': {
            const result = await this.makeRequest(CONTEXT_API_URL, `/api/contexts/${args.window_id}/analyze`, {
              method: 'POST',
            });
            return {
              content: [
                {
                  type: 'text',
                  text: `Context Analysis Results:\n\nQuality Score: ${result.quality_score.toFixed(2)}\n\nMetrics:\n${JSON.stringify(result.metrics, null, 2)}\n\nInsights:\n${result.insights.join('\n- ')}\n\nRecommendations:\n${result.recommendations.join('\n- ')}`,
                },
              ],
            };
          }

          case 'optimize_context': {
            const result = await this.makeRequest(CONTEXT_API_URL, `/api/contexts/${args.window_id}/optimize`, {
              method: 'POST',
              body: JSON.stringify({
                goals: args.goals || ['reduce_tokens', 'improve_clarity'],
                constraints: args.constraints || {},
              }),
            });
            return {
              content: [
                {
                  type: 'text',
                  text: `Started context optimization task: ${result.task_id}\nStatus: ${result.status}\nGoals: ${result.goals.join(', ')}`,
                },
              ],
            };
          }

          case 'auto_optimize_context': {
            const result = await this.makeRequest(CONTEXT_API_URL, `/api/contexts/${args.window_id}/auto-optimize`, {
              method: 'POST',
            });
            return {
              content: [
                {
                  type: 'text',
                  text: `Auto-optimization started: ${result.task_id}\nRecommended goals: ${result.recommendations.recommended_goals.join(', ')}\nReason: ${result.recommendations.reasoning}`,
                },
              ],
            };
          }

          case 'create_prompt_template': {
            const result = await this.makeRequest(CONTEXT_API_URL, '/api/templates', {
              method: 'POST',
              body: JSON.stringify({
                name: args.name,
                description: args.description,
                template: args.template,
                type: args.type || 'completion',
                category: args.category || 'general',
                tags: args.tags || [],
              }),
            });
            return {
              content: [
                {
                  type: 'text',
                  text: `Created template: ${result.name} (ID: ${result.template_id})\nVariables: ${result.variables.join(', ')}`,
                },
              ],
            };
          }

          case 'generate_prompt_template': {
            const params = new URLSearchParams();
            params.append('purpose', args.purpose);
            if (args.examples && args.examples.length > 0) {
              args.examples.forEach(ex => params.append('examples', ex));
            }
            if (args.constraints && args.constraints.length > 0) {
              args.constraints.forEach(c => params.append('constraints', c));
            }

            const result = await this.makeRequest(CONTEXT_API_URL, `/api/templates/generate?${params.toString()}`, {
              method: 'POST',
            });
            return {
              content: [
                {
                  type: 'text',
                  text: `Generated template: ${result.name} (ID: ${result.template_id})\n\nTemplate:\n${result.template}\n\nVariables: ${result.variables.join(', ')}`,
                },
              ],
            };
          }

          case 'list_prompt_templates': {
            const params = new URLSearchParams();
            if (args.category) params.append('category', args.category);
            if (args.tags) params.append('tags', args.tags);

            const result = await this.makeRequest(CONTEXT_API_URL, `/api/templates?${params.toString()}`);
            const templateList = result.templates.map(t => 
              `${t.name} (ID: ${t.id})\n  Type: ${t.type} | Category: ${t.category}\n  Usage: ${t.usage_count} | Quality: ${t.quality_score.toFixed(2)}\n  Variables: ${t.variables.join(', ')}`
            ).join('\n\n');
            
            return {
              content: [
                {
                  type: 'text',
                  text: `Available Templates (${result.templates.length}):\n\n${templateList}`,
                },
              ],
            };
          }

          case 'render_template': {
            const result = await this.makeRequest(CONTEXT_API_URL, `/api/templates/${args.template_id}/render`, {
              method: 'POST',
              body: JSON.stringify({
                template_id: args.template_id,
                variables: args.variables,
              }),
            });
            return {
              content: [
                {
                  type: 'text',
                  text: `Rendered Template:\n\n${result.rendered_content}`,
                },
              ],
            };
          }

          case 'get_context_stats': {
            const result = await this.makeRequest(CONTEXT_API_URL, '/api/stats');
            return {
              content: [
                {
                  type: 'text',
                  text: `Context Engineering System Statistics:\n\nSessions: ${result.sessions.total} total, ${result.sessions.active} active\nContext Windows: ${result.contexts.total_windows}\nElements: ${result.contexts.total_elements} (avg ${result.contexts.avg_elements_per_window.toFixed(1)} per window)\nTemplates: ${result.templates.total_templates}\nOptimization Tasks: ${result.optimization_tasks}`,
                },
              ],
            };
          }

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`,
            },
          ],
        };
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Context Engineering MCP Server running on stdio');
  }
}

const server = new ContextEngineeringMCPServer();
server.run().catch(console.error);