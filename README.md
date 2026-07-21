# MCP Agent Architecture 🚀

A complete learning project implementing **Model Context Protocol (MCP)** in two ways:

1. MCP From Scratch
2. MCP Using Python SDK (FastMCP)

The goal of this project is to understand how modern AI agents connect LLMs with external tools using MCP.

---

# Project Structure

```text
MCP

├── MCP SERVER + CLIENT FROM SCRATCH
│
│   ├── MCP Server
│   │
│   │   ├── main.py
│   │   ├── router.py
│   │   ├── transport.py
│   │   ├── protocol.py
│   │   ├── models.py
│   │   ├── registry.py
│   │   │
│   │   └── tools
│   │       ├── calculator.py
│   │       ├── weather.py
│   │       └── joke.py
│   │
│   └── MCP Client
│       ├── main.py
│       ├── agent.py
│       ├── mcp_client.py
│       ├── ollama_client.py
│       ├── parser.py
│       └── prompts.py
│
└── MCP USING SDK
    │
    ├── chat.py
    ├── mcp_config.json
    │
    ├── servers
    │   ├── calculator.py
    │   └── weather.py
    │
    └── data
```

---

# What is MCP?

Model Context Protocol (MCP) is a standard protocol that allows AI models to communicate with external tools, APIs, databases, and data sources.

Without MCP:

```text
LLM

 |
 +---- Weather API
 |
 +---- Database
 |
 +---- Filesystem
 |
 +---- Custom APIs
```

With MCP:

```text
                 LLM

                  |

             MCP Client

                  |

             MCP Protocol

                  |

             MCP Servers

                  |

        ---------------------
        |        |          |
        v        v          v

    Weather  Database  Filesystem
```

The LLM only understands available tools and schemas.

The MCP Client manages communication with MCP servers.

---

# Part 1: MCP From Scratch

This implementation recreates MCP internally without using any MCP SDK.

Implemented:

- Custom MCP Server
- Custom MCP Client
- JSON-RPC communication
- Tool registry
- Tool discovery
- Tool execution
- Ollama integration
- Agent loop

---

# Architecture

```text
                         User

                           |

                           v

                    Agent Runtime

                           |

              -------------------------

              |                       |

              v                       v

          Ollama Gemma3          MCP Client

                                      |

                              JSON-RPC over STDIO

                                      |

                                      v

                               MCP Server

                                      |

              --------------------------------------

              |                  |                 |

              v                  v                 v

        Calculator           Weather            Joke
```

---

# MCP Server

Responsibilities:

- Register tools
- Expose tools
- Receive requests
- Execute tools
- Return responses


The server does not know anything about the LLM.

It only provides capabilities.

---

# JSON-RPC Communication

Example initialize request:

```json
{
 "jsonrpc":"2.0",
 "id":1,
 "method":"initialize",
 "params":{}
}
```

Response:

```json
{
 "jsonrpc":"2.0",
 "id":1,
 "result":{
    "protocolVersion":"0.1",
    "serverInfo":{
        "name":"Scratch MCP",
        "version":"1.0"
    }
 }
}
```

---

# MCP Methods

## tools/list

Returns available tools.

Example:

```json
{
 "jsonrpc":"2.0",
 "method":"tools/list"
}
```

---

## tools/call

Executes a tool.

Example:

```json
{
 "jsonrpc":"2.0",
 "method":"tools/call",
 "params":{
    "name":"calculator",
    "arguments":{
        "operation":"multiply",
        "operands":[10,20]
    }
 }
}
```

---

# Tool Architecture

Every tool follows a common structure:

```python
class BaseTool:

    name = ""

    description = ""

    input_schema = {}


    def execute(self, arguments):
        raise NotImplementedError
```

---

# Implemented Tools

## Calculator

Supports:

```text
add
subtract
multiply
divide
```

Example:

```text
User:

Calculate 20 multiplied by 30
```

LLM generates:

```json
{
 "tool":"calculator",
 "arguments":{
    "operation":"multiply",
    "operands":[20,30]
 }
}
```

---

## Weather

Uses external weather APIs.

Example:

```json
{
 "tool":"weather",
 "arguments":{
    "city":"Kathmandu"
 }
}
```

---

## Joke

Returns random jokes.

Example:

```json
{
 "tool":"joke",
 "arguments":{}
}
```

---

# MCP Client

Responsibilities:

- Start MCP servers
- Send JSON-RPC requests
- Receive responses
- Execute tools
- Connect LLM decisions with tools

---

# Agent Workflow

```text
User Question

        |

        v

       LLM

        |

   Need Tool?

      /     \

    Yes      No

    |         |

 Tool Call  Normal Answer

    |

 MCP Client

    |

 MCP Server

    |

 Tool Execution

    |

 Tool Result

    |

 Final Answer
```

---

# Part 2: MCP Using Python SDK (FastMCP)

This implementation uses the official MCP Python SDK.

Features:

- FastMCP
- Custom MCP servers
- Official MCP servers
- Ollama Agent
- Tool discovery

---

# Architecture

```text
                         User

                           |

                           v

                        chat.py

                     MCP Client


                           |

                    Tool Discovery


              -------------------------

              |                       |

              v                       v


        Custom MCP Servers     Official MCP Servers


        Calculator             Filesystem

        Weather                Fetch

                               SQLite


              -------------------------

                           |

                           v

                       Ollama LLM
```

---

# Custom MCP Servers

## Calculator MCP

Tools:

```python
add()

multiply()
```

---

## Weather MCP

Uses Open-Meteo API.

Tool:

```python
weather(city)
```

---

# Official MCP Servers

## Filesystem MCP

Capabilities:

```text
read_file()

write_file()

edit_file()

create_directory()

list_directory()

search_files()
```

---

## Fetch MCP

Used for fetching external resources.

Example:

```text
Summarize webpage
```

---

## SQLite MCP

Capabilities:

```text
Create tables

Execute queries

Read database data
```

---

# Installation

Create environment:

```bash
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install mcp requests
```

---

# Ollama Setup

Install Ollama:

```text
https://ollama.com
```

Pull model:

```bash
ollama pull llama3.1
```

Run:

```bash
ollama serve
```

---

# Run Project

```bash
python chat.py
```

---

# Important Lessons Learned

## stdout must contain only protocol messages

Wrong:

```text
Server started

Waiting for request

{
 json response
}
```

Correct:

```json
{
 "jsonrpc":"2.0"
}
```

Logs should go to stderr.

---

# Python Environment Issue

Problem:

Client and server used different Python interpreters.

Solution:

```python
sys.executable
```

Example:

```python
subprocess.Popen(
[
 sys.executable,
 "main.py"
]
)
```

---

# Buffering Issue

Problem:

```text
Waiting for response...
```

Solution:

```python
print(
 json.dumps(response),
 flush=True
)
```

---

# Tool Schema Importance

The LLM depends heavily on tool descriptions.

Bad:

```text
calculator
```

Good:

```json
{
 "name":"calculator",
 "description":"Performs arithmetic operations",
 "inputSchema":{
 }
}
```

---

# Tech Stack

- Python
- JSON-RPC
- Ollama
- Gemma3
- Llama3.1
- MCP Python SDK
- FastMCP
- STDIO Communication

---

# Future Improvements

- Multiple MCP servers
- Authentication
- Streaming responses
- Memory MCP
- RAG MCP
- Vector Database MCP
- Browser Automation MCP
- Multi-Agent workflow
- A2A protocol integration

---

# Learning Outcome

After completing this project:

You understand:

- MCP internals
- Client/server architecture
- Tool discovery
- Tool schemas
- LLM tool calling
- Agent execution loops
- Official MCP ecosystem


This project recreates the foundation behind:

- Claude MCP integrations
- Cursor AI tools
- AI coding assistants
- Modern agent frameworks


---

# References

MCP Documentation:

https://modelcontextprotocol.io

MCP Python SDK:

https://github.com/modelcontextprotocol/python-sdk

Ollama:

https://ollama.com


---

# Author

Built as a learning project to understand MCP internals and LLM-powered agent architecture.
