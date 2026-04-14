# 📂 Project Structure

```
ai-company-sim/
│
├── backend/                          # FastAPI backend + AI engine
│   │
│   ├── app/                          # API layer
│   │   ├── main.py                   # FastAPI entry point
│   │   │
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── chat.py           # Main chat endpoint
│   │   │   │   └── health.py         # Health check endpoint
│   │   │   └── deps.py               # Dependency injection
│   │   │
│   │   ├── core/
│   │   │   ├── config.py             # Application configuration
│   │   │   └── logger.py             # Logging setup
│   │   │
│   │   └── schemas/
│   │       ├── chat.py               # Request/response schemas
│   │       └── agent.py
│   │
│   ├── engine/                       # Core AI system
│   │   │
│   │   ├── orchestrator/
│   │   │   ├── orchestrator.py       # Coordination logic
│   │   │   └── router.py             # Agent routing logic
│   │   │
│   │   ├── agents/
│   │   │   ├── base.py               # Base agent class
│   │   │   │
│   │   │   ├── ceo/
│   │   │   │   ├── agent.py
│   │   │   │   ├── prompt.txt
│   │   │   │   └── config.yaml
│   │   │   │
│   │   │   ├── chro/
│   │   │   │   ├── agent.py
│   │   │   │   ├── prompt.txt
│   │   │   │   └── config.yaml
│   │   │   │
│   │   │   └── manager/
│   │   │
│   │   ├── supervisor/
│   │   │   └── supervisor.py         # Monitoring & validation
│   │   │
│   │   ├── memory/
│   │   │   ├── short_term.py         # Conversation memory
│   │   │   ├── long_term.py          # Persistent memory
│   │   │   └── store.py              # Storage abstraction
│   │   │
│   │   └── tools/
│   │       ├── kpi_calculator.py
│   │       └── ab_testing.py
│   │
│   ├── llm/                          # LLM abstraction layer
│   │   ├── client.py                 # Unified LLM interface
│   │   └── providers/
│   │       ├── groq.py
│   │       └── together.py
│   │
│   ├── configs/                      # Config-driven system
│   │   ├── agents.yaml
│   │   └── system.yaml
│   │
│   ├── scripts/
│   ├── tests/
│   ├── requirements.txt
│   └── .env
│
├── frontend/                         # React application
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBox.jsx
│   │   │   ├── MessageInput.jsx
│   │   │   ├── AgentCard.jsx
│   │   │   └── AgentResponse.jsx
│   │   │
│   │   ├── pages/
│   │   │   └── ChatPage.jsx
│   │   │
│   │   ├── hooks/
│   │   │   └── useChat.js
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   └── types/
│   │       └── chat.ts
│   │
│   ├── package.json
│   └── vite.config.js
│
├── infra/                            # Infrastructure & deployment
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── README.md
└── .gitignore
```
