# 19 — Codegen SDK, n8n Workflow Automation & Agent DevOps Toolchain

> **Mục đích training:** Hiểu Codegen SDK (SWE agent chạy at scale), n8n workflow automation cho AI agents, Milvus vector DB integration, và toolchain tổng hợp cho agent development.

---

## 1. Codegen SDK — "The SWE that Never Sleeps"

### 1.1 Overview
- **Tên:** Codegen SDK
- **Company:** Codegen (codegen.com)
- **GitHub:** [codegen-sh/codegen](https://github.com/codegen-sh/codegen)
- **License:** Apache 2.0
- **Language:** Python 98.4%
- **Stars:** 500+ | Contributors: 31+
- **Mục đích:** Programmatic interface tới AI coding agents chạy at scale

### 1.2 Core Concept

```
TRADITIONAL AI CODING:
├─ 1 developer ↔ 1 Copilot session
├─ Interactive, synchronous
├─ Manual task delegation
└─ Limited parallelism

CODEGEN SDK:
├─ API-driven agent management
├─ Run multiple agents in parallel
├─ Async task execution
├─ Integrate with Slack, Linear, GitHub
├─ Scale to enterprise workflows
└─ "The SWE that Never Sleeps"
```

### 1.3 Quick Start

```python
from codegen.agents.agent import Agent

# 1. Initialize Agent
agent = Agent(
    org_id="YOUR_ORG_ID",       # From codegen.com/token
    token="YOUR_API_TOKEN",      # From codegen.com/token
)

# 2. Run agent with prompt
task = agent.run(
    prompt="Implement sorting feature for users by last login"
)

# 3. Check status
print(task.status)  # "running" | "completed" | "failed"

# 4. Refresh to get updates (tasks take time)
task.refresh()

# 5. Get result
if task.status == "completed":
    print(task.result)  # Code, summaries, PR links
```

### 1.4 Installation & CLI

```bash
# Install
pip install codegen
# or
pipx install codegen
# or
uv tool install codegen

# Auto-update
codegen update

# Check for updates
codegen update --check

# Specific version
codegen update --version 1.2.3
```

### 1.5 Integration Channels

```
CODEGEN INTERFACES:
├─ API — Programmatic access (REST)
├─ Slack — Chat with agent in channels
├─ Linear — Auto-assign to tickets
├─ GitHub — PR-based workflow
├─ Website — Web chat interface
└─ MCP Server — For Claude/Copilot integration
```

### 1.6 Áp dụng cho EMADS-PR

```python
# Concept: Codegen as execution layer for EMADS-PR
class EMDADSCodegenExecutor:
    def __init__(self):
        self.agent = Agent(org_id="...", token="...")
    
    def execute_approved_task(self, reconcile_decision):
        """After ReconcileGPT + Human approval, execute via Codegen"""
        
        if reconcile_decision["approved"]:
            task = self.agent.run(
                prompt=f"""
                Execute the following approved change:
                {reconcile_decision['execution_plan']}
                
                Constraints:
                - Only modify files in allowlist
                - Create PR with full description
                - Include tests for changes
                - Budget: {reconcile_decision['budget_remaining']} tokens
                """
            )
            
            # Monitor async
            while task.status == "running":
                task.refresh()
                time.sleep(30)
            
            return task.result
```

---

## 2. n8n Workflow Automation — Connecting Agents

### 2.1 Overview
- **n8n** = Open-source workflow automation platform
- Self-hostable (không cần cloud subscription)
- 400+ integrations out-of-the-box
- Visual workflow builder (node-based)
- AI-native: built-in LLM nodes, vector store nodes

### 2.2 n8n cho AI Agent Workflows

```
┌─────────────────────────────────────────────────┐
│           n8n AI AGENT WORKFLOW                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  TRIGGER                                        │
│  ├─ Webhook (API call)                          │
│  ├─ Schedule (cron)                             │
│  ├─ Slack message                               │
│  ├─ GitHub event (PR, issue)                    │
│  └─ Email received                              │
│     │                                           │
│  AI PROCESSING                                  │
│  ├─ LLM Node (OpenAI, Claude, local)           │
│  ├─ Vector Store Query (Milvus, Pinecone)       │
│  ├─ RAG Pipeline (retrieve + generate)          │
│  ├─ Agent Node (tool-calling agent)             │
│  └─ Code Node (custom Python/JS)               │
│     │                                           │
│  ACTIONS                                        │
│  ├─ Send Slack/Telegram notification            │
│  ├─ Create GitHub PR/issue                      │
│  ├─ Update database                             │
│  ├─ Send email                                  │
│  └─ Call external API                           │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 2.3 n8n + EMADS-PR Integration

```json
{
  "workflow": "EMADS-PR Auto Routing",
  "nodes": [
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "config": {
        "path": "/emads-pr/task",
        "method": "POST"
      }
    },
    {
      "name": "Orchestrator Agent",
      "type": "n8n-nodes-base.openAi",
      "config": {
        "model": "minimax-m2",
        "system_prompt": "Route task to appropriate specialist agents",
        "tools": ["route_to_cto", "route_to_coo", "route_to_risk"]
      }
    },
    {
      "name": "Parallel Processing",
      "type": "n8n-nodes-base.splitInBatches",
      "config": {
        "agents": ["CTO", "COO", "Legal", "Risk", "Cost"]
      }
    },
    {
      "name": "ReconcileGPT",
      "type": "n8n-nodes-base.openAi",
      "config": {
        "model": "gpt-5",
        "system_prompt": "Analyze trade-offs, score recommendations"
      }
    },
    {
      "name": "Telegram Notification",
      "type": "n8n-nodes-base.telegram",
      "config": {
        "chatId": "ADMIN_CHAT_ID",
        "message": "{{reconcile_decision}} — APPROVE/REJECT?"
      }
    }
  ]
}
```

### 2.4 Self-Hosting n8n

```bash
# Docker (recommended)
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=secure_password \
  n8nio/n8n

# Docker Compose (production)
# docker-compose.yml with PostgreSQL + Redis
```

---

## 3. Milvus Vector Database — Agent Memory Store

### 3.1 Tại sao cần Vector DB cho Agents?

```
AGENT MEMORY NEEDS:
├─ Store embeddings of past interactions
├─ Semantic search for relevant memories
├─ Fast retrieval (milliseconds)
├─ Scale to millions of memories
├─ Filter by metadata (agent_role, timestamp, topic)
└─ Support for ReasoningBank pattern (xem File 16)
```

### 3.2 Milvus Overview
- **Open-source** vector database
- **Scalable:** billions of vectors
- **Fast:** millisecond search
- **Rich filtering:** metadata + vector hybrid search
- **Cloud option:** Zilliz Cloud (managed Milvus)

### 3.3 n8n + Milvus Integration

```python
# Concept: Milvus as memory backend for n8n AI workflows

from pymilvus import connections, Collection, FieldSchema, CollectionSchema

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Schema for agent memory
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="agent_role", dtype=DataType.VARCHAR, max_length=50),
    FieldSchema(name="task_type", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="outcome", dtype=DataType.VARCHAR, max_length=20),  # success/failure
    FieldSchema(name="strategy", dtype=DataType.VARCHAR, max_length=2000),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
    FieldSchema(name="timestamp", dtype=DataType.INT64),
]

schema = CollectionSchema(fields, description="Agent ReasoningBank Memory")
collection = Collection("agent_memory", schema)

# Create index for fast search
collection.create_index(
    field_name="embedding",
    index_params={
        "metric_type": "COSINE",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 1024}
    }
)

# Store memory
def store_memory(agent_role, task_type, outcome, strategy, embedding):
    collection.insert([
        [agent_role],
        [task_type],
        [outcome],
        [strategy],
        [embedding],
        [int(time.time())]
    ])

# Retrieve relevant memories
def retrieve_memories(query_embedding, agent_role, top_k=5):
    collection.load()
    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param={"metric_type": "COSINE", "params": {"nprobe": 10}},
        limit=top_k,
        expr=f'agent_role == "{agent_role}"',
        output_fields=["strategy", "outcome", "task_type"]
    )
    return results
```

---

## 4. Agent DevOps Toolchain — Tổng hợp

### 4.1 Complete Toolchain Map

```
┌──────────────────────────────────────────────────────┐
│           AGENT DEVOPS TOOLCHAIN                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  🏗️ DEVELOPMENT                                     │
│  ├─ VS Code + GitHub Copilot    — IDE + AI coding    │
│  ├─ Copilot CLI                  — Terminal agents    │
│  ├─ Codegen SDK                  — Agent at scale     │
│  ├─ Spec-Driven Dev (main.md)   — Markdown-as-code   │
│  └─ LangGraph / AgentScope      — Framework          │
│                                                      │
│  🔧 ORCHESTRATION                                    │
│  ├─ n8n                         — Workflow automation │
│  ├─ GitHub Actions              — CI/CD              │
│  ├─ MCP Servers                 — Tool integration    │
│  └─ Codegen Agent               — Background SWE     │
│                                                      │
│  💾 DATA & MEMORY                                    │
│  ├─ Milvus                      — Vector DB (memory)  │
│  ├─ PostgreSQL                  — Relational data     │
│  ├─ Redis                       — Cache + queue       │
│  └─ ReasoningBank               — Strategy memory     │
│                                                      │
│  🔒 SECURITY                                         │
│  ├─ Cisco MCP Scanner           — MCP security        │
│  ├─ CodeQL                      — Code analysis       │
│  ├─ Dependabot                  — Dependency safety    │
│  ├─ SLSA + Attestations         — Supply chain        │
│  └─ Secret Scanning             — Credential safety   │
│                                                      │
│  📊 MONITORING                                       │
│  ├─ Telegram Bot                — Alerts + approval   │
│  ├─ Azure Monitor               — Cloud monitoring    │
│  ├─ Prometheus + Grafana        — Metrics             │
│  └─ SIEM/SOC                    — Security monitoring  │
│                                                      │
│  🧪 TESTING                                          │
│  ├─ pytest                      — Unit + integration  │
│  ├─ Adversarial testing         — Prompt injection    │
│  ├─ Cost simulation             — Budget testing      │
│  └─ E2E pipeline tests          — Full flow           │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### 4.2 Setup Priorities (cho dự án mới)

```
PHASE 1 — FOUNDATION (Week 1):
├─ 1. GitHub repo + copilot-instructions.md
├─ 2. Codegen SDK account + API key
├─ 3. n8n self-hosted (Docker)
├─ 4. Milvus instance (Docker)
└─ 5. Telegram Bot for notifications

PHASE 2 — SECURITY (Week 2):
├─ 1. Dependabot enabled
├─ 2. CodeQL analysis workflow
├─ 3. Secret scanning + push protection
├─ 4. Branch protection rules
└─ 5. Cisco MCP Scanner for any MCP servers

PHASE 3 — AGENTS (Week 3-4):
├─ 1. Agent specs (Spec-Driven Dev approach)
├─ 2. LangGraph state graph
├─ 3. ReasoningBank memory with Milvus
├─ 4. n8n workflow for routing + notifications
└─ 5. Copilot CLI for headless automation

PHASE 4 — PRODUCTION (Week 5+):
├─ 1. SLSA Level 3 + artifact attestations
├─ 2. Monitoring + alerting
├─ 3. Cost tracking + budget agents
├─ 4. Adversarial testing
└─ 5. Performance optimization
```

---

## 5. n8n vs Make vs Zapier — So sánh

| Feature | n8n | Make (Integromat) | Zapier |
|---------|-----|-------|--------|
| **Self-hosted** | ✅ Yes | ❌ No | ❌ No |
| **Open source** | ✅ Yes | ❌ No | ❌ No |
| **AI nodes** | ✅ Built-in | ⚠️ Limited | ⚠️ Limited |
| **Vector DB** | ✅ Milvus/Pinecone | ❌ No | ❌ No |
| **Custom code** | ✅ Python + JS | ⚠️ Limited | ⚠️ Limited |
| **Pricing** | Free (self-host) | $9/mo+ | $20/mo+ |
| **Data privacy** | ✅ Your server | ❌ Cloud only | ❌ Cloud only |
| **Complex logic** | ✅ Full control | ⚠️ Limited | ⚠️ Limited |
| **Enterprise** | ✅ n8n Cloud | ✅ Enterprise | ✅ Enterprise |

**Recommendation:** n8n cho EMADS-PR vì self-hosted, AI-native, và free.

---

## 6. Key Takeaways cho Agent

```
✅ Codegen SDK = API-driven AI coding agent, chạy at scale
✅ n8n = best self-hosted workflow automation cho AI agents
✅ Milvus = vector DB cho agent memory (ReasoningBank backend)
✅ n8n + Milvus + LangGraph = full agent orchestration stack
✅ Codegen CLI tự update: `codegen update`
✅ n8n self-hosted = free, data privacy, full control
✅ Toolchain setup theo phases: Foundation → Security → Agents → Production
✅ n8n > Zapier/Make cho agent workflows (AI nodes, self-hosted, open-source)
✅ Kết hợp Codegen (execution) + n8n (orchestration) + Copilot CLI (terminal)
```

---

## 📚 Sources

- GitHub: [Codegen SDK](https://github.com/codegen-sh/codegen)
- Codegen: [Documentation](https://docs.codegen.com/)
- Codegen: [Getting Started](https://docs.codegen.com/introduction/getting-started)
- n8n: [Official Docs](https://docs.n8n.io/)
- n8n: [Self-Hosting Guide](https://docs.n8n.io/hosting/)
- n8n: [AI Agent Nodes](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/)
- Milvus: [Documentation](https://milvus.io/docs)
- Milvus: [n8n Integration](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.vectorstoremilvus/)
