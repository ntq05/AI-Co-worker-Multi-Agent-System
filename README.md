# 🚀 Agentic Corporate Simulation: A Cognitive Multi-Agent Framework

In a modern corporate landscape, decision-making often requires the intersection of various expertise—Strategic, Human Resources, and Operational. This project builds an Agentic AI Ecosystem that simulates a professional board of directors.

Instead of a simple chatbot, this system implements a Cognitive Architecture where specialized AI Agents (CEO, CHRO, Manager) collaborate to solve business problems. By treating agents as modular tools and implementing a sophisticated memory management cycle, the framework ensures high-quality reasoning while maintaining efficiency in production environments.

This repository features a sophisticated **Agentic AI System** designed to simulate a corporate decision-making environment. It leverages a **Supervisor-Worker architecture**, served via **FastAPI**, and is fully containerized using **Docker**.

---

## 🔄 1. System Workflow: The Lifecycle of a Request

The system utilizes a **LangGraph state machine** to ensure logical consistency and context efficiency through a predefined execution path:

### 🔹 Entry Point (Summarizer Node)
- Every user input is first processed by the **Summarizer**.
- If the thread history exceeds **10 messages**:
  - Older interactions are archived into a **"Progressive Summary"**.
  - Only the **3 most recent messages** are retained as raw context.
- This ensures the LLM receives a condensed yet relevant context window, preventing context overflow and maintaining focus.

### 🔹 Routing (Orchestrator / Supervisor Node)
- The **Orchestrator** analyzes the user intent alongside the current summary.
- Acts as a router using **LangChain Tool Calling** to trigger specialized sub-agents:
  - `call_ceo` → Strategy
  - `call_chro` → HR

### 🔹 Execution (Worker Nodes)
- The selected Worker (**CEO, CHRO, or Manager**) receives refined context.
- Generates responses based on:
  - Persona
  - Business Goal (defined in YAML configurations)

### 🔹 Persistence
- State is automatically saved to **PostgreSQL** via an asynchronous checkpointer.
- Enables **stateful, long-running conversations** across sessions.

---

## 🧠 2. Intelligent Memory Management

### 🔹 Short-Term Memory
- Managed via **LangGraph State**
- Tracks current conversation flow

### 🔹 Progressive Memory
- The **Summarizer Agent** compresses historical data
- Maintains long-term context while optimizing token usage

### 🔹 Stateful Persistence
- Powered by **AsyncPostgresSaver**
- Allows perfect restoration of any conversation thread

---

## 🛠️ 3. Tech Stack & Infrastructure

- **Framework:** LangChain (Prompt Templates, LLM interaction, Output Parsing)
- **Orchestration:** LangGraph (State Machine & cyclic workflows)
- **Infrastructure:** Docker & Docker Compose
- **Backend:** FastAPI (Async production-grade API)
- **LLM Gateway:** OpenRouter (gpt-oss-120b:free)
- **Database:** PostgreSQL (Async thread-state checkpointer)

---

## 🔮 4. Future Roadmap: Towards a Cognitive Engine

### 🔹 Modular Agent Toolsets
- Role-specific tools for enhanced capabilities

### 🔹 Comprehensive Memory Model
- **Semantic Memory:** Vector-based retrieval using Qdrant
- **Episodic Memory:** Learning from past experiences
- **Procedural Memory:** Encoding business SOPs into graph logic

---

## 🚀 Quick Start

### 🔹 Prerequisites
Ensure you have **Docker** and **Docker Compose** installed.

### 🔹 Step 1: Environment Configuration
Create a `.env` file in the root directory and add:

```env
OPENROUTER_API_KEY=your_api_key_here
```
### 🔹 Step 2: Build and Run

```bash
cd infra
docker-compose up --build -d
```
### 🔹 Step 3: Access & Testing

Interactive API Docs: http://localhost:8000/docs
Stopping the system:

```bash
docker-compose down
```
## 🗄️ 5. Database Management (pgAdmin)

### 🔹 Connecting to the Database

| Field                 | Value                                          |
|----------------------|-----------------------------------------------|
| Host                 | db-persistence (or localhost if using host)   |
| Port                 | 5432                                          |
| Maintenance Database | ai_memory                                     |
| Username             | user                                          |
| Password             | password                                      |

## 🔮 6. Extended Future Roadmap

### 🔹 Modular Toolsets

- Financial analysis tools
- Market intelligence tools

### 🔹 Cognitive Memory Tiers

- Semantic Memory: Vectorized knowledge via Qdrant

- Episodic Memory: Learning from historical interactions

- Procedural Memory: Business SOPs embedded into graph logic

---

# Project Structure
```text
C:.
│   .gitignore
│   README.md
│
├───backend
│   │   .env
│   │   requirements.txt
│   │
│   ├───app
│   │   │   main.py
│   │   │
│   │   ├───api
│   │   │   │   deps.py
│   │   │   │
│   │   │   └───routes
│   │   │       │   chat.py
│   │   │       │   health.py
│   │   │       │
│   │   │       └───__pycache__
│   │   │               chat.cpython-311.pyc
│   │   │
│   │   ├───core
│   │   │       config.py
│   │   │       logger.py
│   │   │
│   │   ├───schemas
│   │   │   │   agent.py
│   │   │   │   chat.py
│   │   │   │
│   │   │   └───__pycache__
│   │   │           chat.cpython-311.pyc
│   │   │
│   │   └───__pycache__
│   │           main.cpython-311.pyc
│   │
│   └───engine
│       │   README.md
│       │   state.py
│       │
│       ├───agents
│       │   │   base.py
│       │   │
│       │   ├───ceo
│       │   │   │   agent.py
│       │   │   │   config.yaml
│       │   │   │   prompt.txt
│       │   │   │
│       │   │   └───__pycache__
│       │   │           agent.cpython-311.pyc
│       │   │
│       │   ├───chro
│       │   │   │   agent.py
│       │   │   │   config.yaml
│       │   │   │   prompt.txt
│       │   │   │
│       │   │   └───__pycache__
│       │   │           agent.cpython-311.pyc
│       │   │
│       │   ├───manager
│       │   │   │   agent.py
│       │   │   │   config.yaml
│       │   │   │   prompt.txt
│       │   │   │
│       │   │   └───__pycache__
│       │   │           agent.cpython-311.pyc
│       │   │
│       │   ├───orchestrator
│       │   │   │   agent.py
│       │   │   │   config.yaml
│       │   │   │   prompt.txt
│       │   │   │   routerDecision.py
│       │   │   │
│       │   │   └───__pycache__
│       │   │           agent.cpython-311.pyc
│       │   │           orchestrator.cpython-311.pyc
│       │   │           routerDecision.cpython-311.pyc
│       │   │
│       │   ├───SummarizerAgent
│       │   │   │   agent.py
│       │   │   │   config.yaml
│       │   │   │   prompt.txt
│       │   │   │
│       │   │   └───__pycache__
│       │   │           agent.cpython-311.pyc
│       │   │
│       │   └───__pycache__
│       │           base.cpython-311.pyc
│       │
│       ├───configs
│       ├───llm
│       │   │   client.py
│       │   │
│       │   ├───providers
│       │   │   │   groq.py
│       │   │   │   openRouter.py
│       │   │   │
│       │   │   └───__pycache__
│       │   │           groq.cpython-311.pyc
│       │   │           openRouter.cpython-311.pyc
│       │   │
│       │   └───__pycache__
│       │           client.cpython-311.pyc
│       │
│       ├───memory
│       │   │   long_term.py
│       │   │   short_term.py
│       │   │
│       │   └───__pycache__
│       │           short_term.cpython-311.pyc
│       │
│       ├───orchestrator
│       │   │   orchestrator.py
│       │   │   router.py
│       │   │
│       │   └───__pycache__
│       │           orchestrator.cpython-311.pyc
│       │
│       ├───scripts
│       ├───supervisor
│       ├───tests
│       ├───tools
│       │   │   registry.py
│       │   │
│       │   └───__pycache__
│       │           registry.cpython-311.pyc
│       │
│       └───__pycache__
│               state.cpython-311.pyc
│
├───frontend
└───infra
        docker-compose.yml
        Dockerfile.backend
        Dockerfile.frontend
```

