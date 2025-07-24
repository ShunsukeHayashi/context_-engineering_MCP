#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fetch from 'node-fetch';

const API_BASE_URL = process.env.AI_GUIDES_API_URL || 'http://localhost:8888';

class AIGuidesMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'ai-guides-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupHandlers();
  }

  async makeRequest(endpoint, options = {}) {
    try {
      const url = `${API_BASE_URL}${endpoint}`;
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
          description: 'Search for AI guides by keyword in title, description, or topics',
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
          name: 'get_guide_details',
          description: 'Get full details of a specific AI guide by its title',
          inputSchema: {
            type: 'object',
            properties: {
              title: {
                type: 'string',
                description: 'The exact title of the AI guide',
              },
            },
            required: ['title'],
          },
        },
        {
          name: 'get_guide_download_url',
          description: 'Get the download URL for a specific AI guide',
          inputSchema: {
            type: 'object',
            properties: {
              title: {
                type: 'string',
                description: 'The exact title of the AI guide',
              },
            },
            required: ['title'],
          },
        },
        {
          name: 'search_guides_with_gemini',
          description: 'Search guides using Gemini AI semantic search with grounding',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'The search query',
              },
              use_grounding: {
                type: 'boolean',
                description: 'Whether to use Gemini grounding (default: true)',
                default: true,
              },
            },
            required: ['query'],
          },
        },
        {
          name: 'analyze_guide',
          description: 'Analyze a guide using Gemini AI to get enhanced summary and insights',
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
        {
          name: 'analyze_guide_url',
          description: 'Analyze guide content from a URL using Gemini AI',
          inputSchema: {
            type: 'object',
            properties: {
              url: {
                type: 'string',
                description: 'The URL of the guide to analyze',
              },
            },
            required: ['url'],
          },
        },
        {
          name: 'compare_guides',
          description: 'Compare multiple AI guides to find differences and recommendations',
          inputSchema: {
            type: 'object',
            properties: {
              guide_titles: {
                type: 'array',
                items: {
                  type: 'string',
                },
                description: 'List of guide titles to compare (2-5 guides)',
                minItems: 2,
                maxItems: 5,
              },
            },
            required: ['guide_titles'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'list_ai_guides': {
            const guides = await this.makeRequest('/guides');
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
            const guides = await this.makeRequest(`/guides/search?query=${encodeURIComponent(args.query)}`);
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(guides, null, 2),
                },
              ],
            };
          }

          case 'get_guide_details': {
            const guide = await this.makeRequest(`/guides/${encodeURIComponent(args.title)}`);
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(guide, null, 2),
                },
              ],
            };
          }

          case 'get_guide_download_url': {
            const result = await this.makeRequest(`/guides/${encodeURIComponent(args.title)}/download-url`);
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(result, null, 2),
                },
              ],
            };
          }

          case 'search_guides_with_gemini': {
            const result = await this.makeRequest('/guides/search/gemini', {
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
            const result = await this.makeRequest(`/guides/${encodeURIComponent(args.title)}/analyze`);
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(result, null, 2),
                },
              ],
            };
          }

          case 'analyze_guide_url': {
            const result = await this.makeRequest(`/guides/analyze-url?url=${encodeURIComponent(args.url)}`, {
              method: 'POST',
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

          case 'compare_guides': {
            const result = await this.makeRequest('/guides/compare', {
              method: 'POST',
              body: JSON.stringify({
                guide_titles: args.guide_titles,
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
    console.error('AI Guides MCP Server running on stdio');
  }
}

const server = new AIGuidesMCPServer();
server.run().catch(console.error);