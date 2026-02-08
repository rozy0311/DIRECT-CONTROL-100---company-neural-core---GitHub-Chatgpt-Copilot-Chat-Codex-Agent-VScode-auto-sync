# 09 — AgentScope: Framework xây dựng Multi-Agent System Scalable

> **Mục đích training:** Hiểu AgentScope framework — architecture, ReActAgent, MsgHub pipelines, và use cases thực tế cho enterprise multi-agent systems.

---

## 1. Tổng quan AgentScope

### 1.1 AgentScope là gì?
- **Open-source framework** cho multi-agent systems
- Developed by Alibaba DAMO Academy
- Focus: **Scalable, reliable, production-ready** multi-agent apps
- GitHub: https://github.com/modelscope/agentscope

### 1.2 Core Philosophy
```
SIMPLICITY → FLEXIBILITY → RELIABILITY
├─ Easy-to-use APIs
├─ Pluggable components
├─ Built-in fault tolerance
└─ Distributed execution support
```

---

## 2. Core Components

### 2.1 Agent Types

```python
from agentscope.agents import (
    DialogAgent,       # Basic conversational agent
    ReActAgent,        # Reasoning + Acting agent
    UserAgent,         # Human-in-the-loop
    DictDialogAgent,   # Structured output agent
)
```

### 2.2 ReActAgent — Reasoning + Acting

```python
from agentscope.agents import ReActAgent

# Create a ReActAgent with tools
agent = ReActAgent(
    name="CTO_Agent",
    model_config_name="gpt-4.1",  # specialist → fast + cheap
    sys_prompt="""You are a CTO Agent responsible for:
    - Evaluating technical architectures
    - Assessing technology risks
    - Recommending tech stack decisions
    Always provide structured analysis with trade-offs.""",
    tools=[
        "web_search",        # Search for tech trends
        "code_analyzer",     # Analyze code quality
        "benchmark_runner",  # Run performance benchmarks
    ],
    max_iters=10,           # Max reasoning steps
    verbose=True            # Show reasoning process
)
```

### 2.3 ReAct Loop

```
Observation → Thought → Action → Observation → ...

Step 1: OBSERVE
  "User asks: Should we migrate to microservices?"

Step 2: THINK
  "I need to analyze current architecture, team size, 
   and traffic patterns before recommending."

Step 3: ACT
  → Call web_search("microservices pros cons 2025")
  → Call code_analyzer(current_repo)

Step 4: OBSERVE (tool results)
  "Current repo: monolith, 500K LOC, 5 developers..."

Step 5: THINK
  "Team too small for microservices. Recommend modular monolith."

Step 6: ACT
  → Generate final recommendation
```

---

## 3. MsgHub — Multi-Agent Communication

### 3.1 MsgHub Pipeline

```python
from agentscope.msghub import msghub

# Create agents
cto = ReActAgent(name="CTO", ...)
coo = ReActAgent(name="COO", ...)
reconcile = ReActAgent(name="ReconcileGPT", ...)

# MsgHub = shared communication channel
with msghub(
    participants=[cto, coo, reconcile],
    announcement="Discuss: Should we expand to APAC market?"
) as hub:
    # Round 1: Each agent gives initial analysis
    cto_response = cto()    # CTO analyzes tech requirements
    coo_response = coo()    # COO analyzes operational impact
    
    # Round 2: ReconcileGPT synthesizes
    decision = reconcile()  # Reconcile different viewpoints
    
    # Round 3: Review and consensus
    cto_review = cto()      # CTO reviews decision
    coo_review = coo()      # COO reviews decision
```

### 3.2 Message Flow Patterns

```
SEQUENTIAL (Pipe):
  Agent A → Agent B → Agent C → Output

PARALLEL (Fan-out/Fan-in):
  Input → [Agent A, Agent B, Agent C] → Merge → Output

DEBATE (MsgHub):
  Topic → Agent A argues → Agent B counters → 
  Agent C mediates → Consensus

HIERARCHICAL (EMADS-PR):
  CEO → Orchestrator → [Specialists] → ReconcileGPT → 
  Human Review → Execute
```

---

## 4. Practical Examples

### 4.1 Debate Pattern: Claude vs GPT

```python
"""
Multi-agent debate: Which LLM is better for enterprise?
Demonstrates how agents can argue and reach consensus.
"""

claude_advocate = DialogAgent(
    name="Claude_Advocate",
    sys_prompt="You advocate for Claude/Anthropic. Present strong arguments.",
    model_config_name="claude-3-5-sonnet"
)

gpt_advocate = DialogAgent(
    name="GPT_Advocate", 
    sys_prompt="You advocate for GPT/OpenAI. Present strong arguments.",
    model_config_name="gpt-4.1"
)

judge = DialogAgent(
    name="Judge",
    sys_prompt="""You are an impartial judge. Evaluate both arguments 
    based on: accuracy, cost, enterprise features, security. 
    Provide final scoring.""",
    model_config_name="gpt-5"  # judge needs best reasoning
)

with msghub(
    participants=[claude_advocate, gpt_advocate, judge],
    announcement="Debate: Claude vs GPT for enterprise automation"
) as hub:
    for round in range(3):
        claude_advocate()
        gpt_advocate()
    
    final_verdict = judge()
```

### 4.2 Research Pipeline

```python
"""
Multi-agent research pipeline:
1. Researcher finds information
2. Analyst extracts insights
3. Writer produces report
"""

researcher = ReActAgent(
    name="Researcher",
    tools=["web_search", "arxiv_search", "github_search"],
    sys_prompt="Find comprehensive information on the given topic."
)

analyst = DialogAgent(
    name="Analyst",
    sys_prompt="Analyze research findings. Extract key insights, trends, risks."
)

writer = DialogAgent(
    name="Writer",
    sys_prompt="Write a professional report from the analysis."
)

# Sequential pipeline
research_results = researcher(topic)
analysis = analyst(research_results)
report = writer(analysis)
```

### 4.3 Data Processing Pipeline

```python
"""
Multi-agent data processing:
1. Extractor pulls raw data
2. Cleaner validates and cleans
3. Analyzer produces insights
"""

extractor = ReActAgent(
    name="DataExtractor",
    tools=["read_csv", "query_api", "scrape_web"],
    sys_prompt="Extract data from specified sources."
)

cleaner = ReActAgent(
    name="DataCleaner",
    tools=["pandas_operations", "validation_rules"],
    sys_prompt="Clean and validate data. Remove duplicates, fix formats."
)

analyzer = ReActAgent(
    name="DataAnalyzer",
    tools=["statistics", "visualization", "ml_models"],
    sys_prompt="Analyze clean data. Produce insights with charts."
)

# Pipeline execution
raw_data = extractor(data_sources)
clean_data = cleaner(raw_data)
insights = analyzer(clean_data)
```

---

## 5. Configuration & Model Support

### 5.1 Model Configuration

```python
import agentscope

# Initialize with multiple model configs
agentscope.init(
    model_configs=[
        {
            "config_name": "gpt-4.1",
            "model_type": "openai_chat",
            "model_name": "gpt-4.1",
            "api_key": "sk-...",
        },
        {
            "config_name": "claude-3-5-sonnet",
            "model_type": "anthropic_chat",
            "model_name": "claude-3-5-sonnet-20241022",
            "api_key": "sk-ant-...",
        },
        {
            "config_name": "local-llama",
            "model_type": "ollama_chat",
            "model_name": "llama3.1:8b",
        }
    ]
)
```

### 5.2 Distributed Execution

```python
# AgentScope supports distributed multi-agent execution
from agentscope.agents import DistributedDialogAgent

# Agents can run on different machines
agent_a = DistributedDialogAgent(
    name="Agent_A",
    host="server-1.internal",
    port=12345
)

agent_b = DistributedDialogAgent(
    name="Agent_B", 
    host="server-2.internal",
    port=12346
)
```

---

## 6. Enterprise Use Cases

### 6.1 Enterprise Workflow Automation
```
Customer Inquiry → Classifier Agent → Route to:
├─ Sales Agent (product questions)
├─ Support Agent (technical issues)
├─ Billing Agent (payment questions)
└─ Escalation Agent (complex/sensitive)
```

### 6.2 Competitive Intelligence
```
Monitor → [
  News Agent (track industry news),
  Patent Agent (track filings),
  Social Agent (track sentiment)
] → Analyst Agent → Weekly Report
```

### 6.3 Code Review Pipeline
```
PR Submitted → [
  Security Agent (vulnerability scan),
  Style Agent (code quality),
  Performance Agent (efficiency check),
  Test Agent (coverage analysis)
] → Review Summary Agent → Human Reviewer
```

---

## 7. AgentScope vs Alternatives

| Feature | AgentScope | LangGraph | CrewAI | AutoGen |
|---------|-----------|-----------|--------|---------|
| **Ease of use** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Scalability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Distributed** | ✅ Built-in | ❌ (needs LangServe) | ❌ | ✅ |
| **Fault tolerance** | ✅ | ❌ | ❌ | Partial |
| **Model agnostic** | ✅ | ✅ | ✅ | ✅ |
| **Production ready** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 8. Key Takeaways cho Training

1. **AgentScope** = scalable, distributed multi-agent framework từ Alibaba
2. **ReActAgent** = Reasoning + Acting loop, tự suy luận + gọi tools
3. **MsgHub** = shared communication channel cho multi-agent debate/collaboration
4. **4 message patterns:** Sequential, Parallel, Debate, Hierarchical
5. **Multi-model support** — GPT, Claude, Ollama, custom models
6. **Distributed execution** — agents chạy trên nhiều máy
7. **Enterprise use cases** — workflow automation, competitive intelligence, code review

---

## Nguồn tham khảo
- AnalyticsVidhya: "Complete Guide to AgentScope"
- AgentScope GitHub: modelscope/agentscope
- AgentScope Paper: arXiv
- Alibaba DAMO Academy
