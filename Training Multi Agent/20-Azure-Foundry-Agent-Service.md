# 20 — Azure Foundry Agent Service & Microsoft Foundry Platform

> **Nguồn:** Microsoft Learn — Foundry Agent Service Overview, What is Microsoft Foundry  
> **URLs:** https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview, https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-ai-foundry  
> **Ngày tạo:** 2026-02-08  
> **Độ quan trọng:** ⭐⭐⭐⭐⭐  
> **Tags:** `azure`, `foundry`, `agent-service`, `enterprise`, `production`, `cloud`

---

## 📌 Tại sao cần biết?

Microsoft Foundry (trước đây là Azure AI Foundry) là nền tảng chính thức của Microsoft cho enterprise AI — đặc biệt là **Foundry Agent Service** cho việc build, deploy, và quản lý AI agents production-ready. Đây là đối thủ/bổ sung trực tiếp cho self-hosted solutions (n8n, LangGraph) trong EMADS-PR architecture.

---

## 1. Microsoft Foundry Platform Overview

### Foundry là gì?
- **Unified Azure PaaS** cho enterprise AI operations
- Kết hợp: models + tools + frameworks + governance
- Hỗ trợ: Python, C#, JavaScript/TypeScript (preview), Java (preview) SDKs
- Có VS Code Extension: `Microsoft Foundry for VS Code`

### 2 Portal versions:
| Portal | Mô tả | Khi nào dùng |
|--------|--------|-------------|
| **Foundry (classic)** | Full features, multi-resource types | Azure OpenAI, hub-based projects |
| **Foundry (new)** | Streamlined, agent-focused | Multi-agent applications |

### Core capabilities:
- **Model catalog:** GPT-4o, GPT-4, Llama, DeepSeek, xAI, etc.
- **Evaluations:** Built-in evaluation framework (preview)
- **Playgrounds:** Test models interactively
- **Content understanding:** Document processing
- **Model router:** Multi-model orchestration
- **Datasets & Indexes:** Data management

---

## 2. Foundry Agent Service — "Agent Factory"

### Agent = 3 Core Components

```
┌─────────────────────────────────┐
│           AI AGENT              │
├─────────────────────────────────┤
│  1. Model (LLM)                │
│     └─ GPT-4o, GPT-4, Llama   │
│                                 │
│  2. Instructions               │
│     ├─ Prompt-based (single)   │
│     ├─ Workflow (YAML/code)    │
│     └─ Hosted (containerized)  │
│                                 │
│  3. Tools                      │
│     └─ Knowledge + Actions     │
└─────────────────────────────────┘
        ↕ (bidirectional)
   [Bing, SharePoint, Azure AI Search,
    Logic Apps, Azure Functions, OpenAPI]
```

### 6-Step Assembly Line (Agent Factory)

```
Step 1: Models          → Chọn LLM (GPT-4o, Llama, etc.)
Step 2: Customizability → Fine-tune, distillation, domain prompts
Step 3: Knowledge/Tools → Connect enterprise data + actions
Step 4: Orchestration   → Agent-to-agent messaging, tool calls
Step 5: Observability   → Logs, traces, evaluations, App Insights
Step 6: Trust           → Entra ID, RBAC, content filters, encryption
```

### Instruction Types (3 loại):

| Type | Mô tả | Use case |
|------|--------|----------|
| **Prompt-based** | Single agent, natural language prompts | Simple chatbot, Q&A |
| **Workflow** | YAML/code orchestration, multi-agent | EMADS-PR pipeline |
| **Hosted** | Containerized, deployed in code | Custom agent logic |

---

## 3. Key Enterprise Features

### Multi-Agent Coordination
- Built-in **agent-to-agent messaging**
- **Connected agents** orchestrate full lifecycle
- Server-side tool call execution + retry
- Structured logging for every interaction

### Observability
- **Full conversation visibility:** user-to-agent AND agent-to-agent
- **Application Insights integration:** real-time monitoring
- **Trace agents with SDK:** debug tool calls and decisions
- **Metrics dashboard:** usage data, performance

### Security & Trust
| Feature | Chi tiết |
|---------|----------|
| Identity | Microsoft Entra ID |
| Access Control | RBAC + audit logs + conditional access |
| Content Safety | Integrated content filters (XPIA protection) |
| Network | Virtual networks, network isolation |
| Encryption | Data at rest + in transit |
| Data Residency | Bring-your-own storage, Azure Cosmos DB |

### XPIA Protection (Cross-Prompt Injection Attacks)
- Content filters tự động detect và block XPIA
- Policy-governed outputs
- Enterprise compliance built-in

---

## 4. Enterprise Integration — Bring Your Own Resources

```
┌─────────────────────────────────────────┐
│         Foundry Agent Service           │
├──────────┬──────────┬───────────────────┤
│ Storage  │ Search   │ Conversation State│
│ (Azure   │ (Azure   │ (Azure Cosmos DB) │
│ Storage) │ AI Search│                   │
├──────────┴──────────┴───────────────────┤
│ Key Vault │ VNet │ App Insights         │
└─────────────────────────────────────────┘
```

**Bring-your-own:**
- Azure Storage → file management
- Azure AI Search → knowledge retrieval (RAG)
- Azure Cosmos DB → conversation state + BCDR
- Azure Key Vault → secrets management
- Virtual Network → network isolation

### BCDR (Business Continuity & Disaster Recovery)
- Customer-provisioned Azure Cosmos DB
- Auto-failover to secondary region
- All agent state preserved across regions

---

## 5. Tools Integration

### Knowledge Sources
| Tool | Mục đích |
|------|----------|
| **Bing** | Web search |
| **SharePoint** | Enterprise documents |
| **Azure AI Search** | Semantic search, RAG |
| **Azure Blob Storage** | File storage |

### Action Tools
| Tool | Mục đích |
|------|----------|
| **Azure Logic Apps** | Workflow automation |
| **Azure Functions** | Custom code execution |
| **OpenAPI** | Any REST API integration |
| **Connected Agents** | Agent-to-agent delegation |

---

## 6. EMADS-PR Integration với Foundry

### Mapping EMADS-PR → Foundry Agent Service

```
EMADS-PR Agent          →  Foundry Implementation
─────────────────────────────────────────────────
CEO (Input)             →  User prompt / trigger
Orchestrator            →  Workflow instruction (YAML)
CTO Agent               →  Prompt-based agent + Code tools
COO Agent               →  Prompt-based agent + Logic Apps
Legal Agent             →  Prompt-based agent + Search tools
Risk Agent              →  Prompt-based agent + AI Search
Cost Agent              →  Prompt-based agent + Functions
ReconcileGPT            →  Connected agent (consolidator)
Human Review            →  Human-in-the-loop (Logic Apps)
Execute                 →  Azure Functions + GitHub API
Monitor                 →  Application Insights + Metrics
```

### Hybrid Architecture: Foundry + Self-Hosted

```
┌─────────────────────────────────┐
│     Azure Foundry (Cloud)       │
│  ┌──────┐ ┌──────┐ ┌──────┐   │
│  │ CTO  │ │ COO  │ │Legal │   │
│  │Agent │ │Agent │ │Agent │   │
│  └──┬───┘ └──┬───┘ └──┬───┘   │
│     └────┬───┘────────┘        │
│     ┌────▼────┐                │
│     │Reconcile│                │
│     │  GPT    │                │
│     └────┬────┘                │
└──────────┼─────────────────────┘
           │ API
┌──────────▼─────────────────────┐
│    Self-Hosted (n8n/LangGraph) │
│  ┌──────────┐ ┌─────────────┐ │
│  │ n8n      │ │ GitHub      │ │
│  │ Workflow │ │ Actions     │ │
│  └──────────┘ └─────────────┘ │
└────────────────────────────────┘
```

**Khi nào dùng Foundry vs Self-Hosted:**

| Criteria | Azure Foundry | Self-Hosted (n8n/LangGraph) |
|----------|--------------|----------------------------|
| Scale | >1000 rps, multi-region | <1000 rps, single region |
| Compliance | SOC2, HIPAA, GDPR built-in | Tự setup |
| Cost | Pay-per-use (có thể đắt) | Fixed infra cost |
| Data sensitivity | Azure trusted cloud | Full control on-prem |
| Setup time | Nhanh (managed) | Chậm hơn (DIY) |
| Customization | Giới hạn trong framework | Không giới hạn |
| Agent-to-agent | Built-in messaging | Custom implementation |

---

## 7. Pricing & Cost Considerations

```
Foundry Platform    → FREE to explore
Model deployment    → Pay per token (Azure OpenAI pricing)
Agent Service       → Pay for underlying resources
Storage             → Azure Storage pricing
Search              → Azure AI Search pricing
Cosmos DB           → Azure Cosmos DB pricing
```

### Cost-Aware Decision (mở rộng từ File 07):

```
Budget healthy (>50%)  → Azure Foundry + GPT-4o (full features)
Budget tight (20-50%)  → Azure Foundry + GPT-4o-mini (balanced)
Budget critical (<20%) → Self-hosted n8n + local model
Budget empty (0%)      → STOP & report
```

---

## 8. Quickstart Guide

### Step 1: Tạo Foundry Project
```bash
# Azure CLI
az ai foundry project create \
  --name "emads-pr-agents" \
  --resource-group "rg-ai-agents" \
  --location "eastus"
```

### Step 2: Deploy Model
```python
# Python SDK
from azure.ai.foundry import FoundryClient
from azure.identity import DefaultAzureCredential

client = FoundryClient(
    endpoint="https://your-project.api.azureml.ms",
    credential=DefaultAzureCredential()
)

# Deploy GPT-4o for agent reasoning
deployment = client.deployments.create(
    model="gpt-4o",
    name="emads-orchestrator"
)
```

### Step 3: Tạo Agent
```python
from azure.ai.foundry.agents import AgentClient

agent_client = AgentClient(
    endpoint="https://your-project.api.azureml.ms",
    credential=DefaultAzureCredential()
)

# Tạo CTO Agent
cto_agent = agent_client.agents.create(
    model="gpt-4o",
    name="CTO-Agent",
    instructions="""
    Bạn là CTO Agent trong EMADS-PR system.
    Nhiệm vụ: Đánh giá technical feasibility.
    Rules: Xem file 01-EMADS-PR-Architecture.md
    """,
    tools=[
        {"type": "code_interpreter"},
        {"type": "file_search"}
    ]
)
```

### Step 4: Connected Agents (Multi-Agent)
```python
# Tạo Orchestrator với connected agents
orchestrator = agent_client.agents.create(
    model="gpt-4o",
    name="EMADS-Orchestrator",
    instructions="Route tasks to specialist agents...",
    tools=[
        {
            "type": "connected_agent",
            "connected_agent": {"id": cto_agent.id}
        },
        {
            "type": "connected_agent", 
            "connected_agent": {"id": coo_agent.id}
        }
    ]
)
```

---

## 9. Monitoring & Observability

### Application Insights Integration
```python
# Trace agent decisions
from azure.ai.foundry.agents import TraceConfig

trace_config = TraceConfig(
    enable_content_recording=True,
    application_insights_connection_string="InstrumentationKey=..."
)

# Mọi tool call, message, decision đều được logged
```

### Key Metrics to Monitor:
- **Token usage** per agent per conversation
- **Tool call success/failure** rates
- **Response latency** (P50, P95, P99)
- **Content filter triggers** (safety events)
- **Agent-to-agent message** patterns

---

## 10. So sánh Foundry vs Alternatives

| Feature | Azure Foundry | LangGraph | CrewAI | AutoGen |
|---------|--------------|-----------|--------|---------|
| Managed service | ✅ | ❌ | ❌ | ❌ |
| Multi-agent built-in | ✅ | ✅ | ✅ | ✅ |
| Enterprise security | ✅ (SOC2, HIPAA) | DIY | DIY | DIY |
| Observability | ✅ (App Insights) | Custom | Custom | Custom |
| Content filters | ✅ Built-in | ❌ | ❌ | ❌ |
| BCDR | ✅ (Cosmos DB) | DIY | ❌ | ❌ |
| Cost | Pay-per-use | Free framework | Free/Paid | Free |
| Vendor lock-in | Azure | None | None | None |

---

## 🔗 Liên kết trong hệ thống training

| File | Mối liên hệ |
|------|-------------|
| [01](01-EMADS-PR-Architecture.md) | EMADS-PR architecture → maps to Foundry Agent Factory |
| [07](07-Cost-Aware-Planning-Agent.md) | Cost-aware planning → Foundry pricing model |
| [12](12-LangGraph-Implementation.md) | LangGraph implementation → Foundry alternative |
| [13](13-Multi-Agent-Evaluation-Testing.md) | Evaluation → Foundry built-in evaluations |
| [17](17-Agent-Supply-Chain-Security.md) | Security → Foundry enterprise trust features |
| [18](18-Open-Source-LLMs-Agentic-Tools.md) | Model selection → Foundry model catalog |
| [19](19-Codegen-n8n-Agent-DevOps-Toolchain.md) | n8n/Codegen → Foundry hybrid architecture |
