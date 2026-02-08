# 12 — LangGraph Implementation: Xây dựng EMADS-PR trong thực tế

> **Mục đích training:** Hướng dẫn triển khai EMADS-PR v1.0 bằng LangGraph — state machines, parallel dispatch, conditional routing, human-in-the-loop, và production patterns.

---

## 1. Tại sao LangGraph?

### 1.1 So sánh Frameworks

| Feature | LangGraph | CrewAI | AutoGen | AgentScope |
|---------|-----------|--------|---------|------------|
| **State machine** | ✅ Native | ❌ | ❌ | Partial |
| **Conditional routing** | ✅ Native | Partial | Partial | ✅ |
| **Human-in-the-loop** | ✅ Built-in | Manual | Partial | Manual |
| **Parallel nodes** | ✅ Native | ✅ | ✅ | ✅ |
| **Persistence** | ✅ Checkpoints | ❌ | ❌ | Partial |
| **Streaming** | ✅ | ❌ | ❌ | Partial |
| **Production ready** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

### 1.2 LangGraph = Đúng tool cho EMADS-PR
- **State machine** → Model luồng CEO → Orchestrator → Specialists → ReconcileGPT
- **Conditional edges** → Route dựa trên risk score, agent type
- **Parallel execution** → CTO + COO + Legal + Risk + Cost chạy cùng lúc
- **Checkpoints** → Resume từ bất kỳ điểm nào nếu crash
- **Human-in-the-loop** → Governance gate built-in

---

## 2. State Definition

### 2.1 EMADS State

```python
from typing import TypedDict, Annotated, List, Optional
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import operator

class AgentOutput(TypedDict):
    """Output từ mỗi specialist agent"""
    agent_name: str
    analysis: str
    recommendations: list[str]
    risks: list[dict]
    cost_estimate: dict
    confidence: float

class EMADSState(TypedDict):
    """State chính của EMADS-PR system"""
    
    # Input
    task: str
    ceo_input: str
    constraints: dict
    
    # Memory & Context
    messages: Annotated[list, add_messages]
    memory_context: str
    
    # Specialist Outputs
    cto_output: Optional[AgentOutput]
    coo_output: Optional[AgentOutput]
    legal_output: Optional[AgentOutput]
    risk_output: Optional[AgentOutput]
    cost_output: Optional[AgentOutput]
    
    # ReconcileGPT Output
    reconcile_decision: Optional[dict]
    reconcile_score: float
    
    # Human Review
    human_approved: Optional[bool]
    human_feedback: Optional[str]
    
    # Execution
    execution_plan: Optional[dict]
    execution_result: Optional[dict]
    
    # Monitoring
    risk_score: int  # 0-12
    automation_score: int  # 0-12
    total_cost_usd: float
    iteration_count: int
```

---

## 3. Node Definitions

### 3.1 Orchestrator Node

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-5", temperature=0)  # orchestrator → best reasoning

def orchestrator_node(state: EMADSState) -> dict:
    """
    Orchestrator: Route + Coordinate + State Management
    Quyết định dispatch tới specialists nào.
    """
    
    # Retrieve memory context
    memory = retrieve_memory(state["task"])
    
    # Analyze task to determine which specialists needed
    response = llm.invoke([
        {"role": "system", "content": """You are the Orchestrator.
        Analyze the task and determine:
        1. Which specialist agents are needed
        2. Priority and dependencies
        3. Initial constraints
        Output JSON with: needed_agents, priority, constraints"""},
        {"role": "user", "content": f"""
        Task: {state['task']}
        CEO Input: {state['ceo_input']}
        Constraints: {state['constraints']}
        Historical Context: {memory}
        """}
    ])
    
    return {
        "memory_context": memory,
        "messages": [response],
        "iteration_count": state.get("iteration_count", 0) + 1
    }
```

### 3.2 Specialist Agent Nodes

```python
def cto_agent_node(state: EMADSState) -> dict:
    """CTO Agent: Tech strategy, architecture, risks"""
    
    response = llm.invoke([
        {"role": "system", "content": """You are the CTO Agent.
        Responsibilities:
        - Evaluate technical architectures (options A/B/C)
        - Assess technology risks and dependencies
        - Estimate effort, timeline, and technical debt
        - Recommend tech stack decisions
        
        Output STRUCTURED analysis with:
        - tech_options: [{name, pros, cons, effort, timeline}]
        - risks: [{risk, probability, impact, mitigation}]
        - recommendation: string
        - confidence: 0.0-1.0"""},
        {"role": "user", "content": f"""
        Task: {state['task']}
        Constraints: {state['constraints']}
        Context: {state.get('memory_context', '')}
        """}
    ])
    
    return {
        "cto_output": parse_agent_output("CTO", response),
        "messages": [response]
    }

def coo_agent_node(state: EMADSState) -> dict:
    """COO Agent: Operations, resources, process"""
    
    response = llm.invoke([
        {"role": "system", "content": """You are the COO Agent.
        Responsibilities:
        - Analyze operational impact (resources, SLA, OPEX)
        - Evaluate process changes needed
        - Assess team capacity and skills gap
        - Estimate operational costs and timeline
        
        Output STRUCTURED analysis with:
        - ops_impact: [{area, current_state, required_changes}]
        - resource_needs: [{type, quantity, cost}]
        - risks: [{risk, probability, impact}]
        - recommendation: string
        - confidence: 0.0-1.0"""},
        {"role": "user", "content": f"""
        Task: {state['task']}
        Constraints: {state['constraints']}
        """}
    ])
    
    return {
        "coo_output": parse_agent_output("COO", response),
        "messages": [response]
    }

def legal_agent_node(state: EMADSState) -> dict:
    """Legal Agent: Compliance, regulatory"""
    response = llm.invoke([
        {"role": "system", "content": "You are the Legal/Compliance Agent..."},
        {"role": "user", "content": f"Task: {state['task']}"}
    ])
    return {"legal_output": parse_agent_output("Legal", response)}

def risk_agent_node(state: EMADSState) -> dict:
    """Risk Agent: Threat assessment"""
    response = llm.invoke([
        {"role": "system", "content": "You are the Risk Assessment Agent..."},
        {"role": "user", "content": f"Task: {state['task']}"}
    ])
    return {"risk_output": parse_agent_output("Risk", response)}

def cost_agent_node(state: EMADSState) -> dict:
    """Cost Agent: Budget, ROI"""
    response = llm.invoke([
        {"role": "system", "content": "You are the Cost Management Agent..."},
        {"role": "user", "content": f"Task: {state['task']}"}
    ])
    return {"cost_output": parse_agent_output("Cost", response)}
```

### 3.3 ReconcileGPT Node

```python
def reconcile_gpt_node(state: EMADSState) -> dict:
    """
    ReconcileGPT: Decision Engine
    Tổng hợp outputs từ tất cả specialists → recommend
    """
    
    response = llm.invoke([
        {"role": "system", "content": """You are ReconcileGPT — the Decision Engine.
        
        CRITICAL RULES:
        1. You are a TOOL, not a decision maker
        2. Analyze ALL specialist outputs objectively
        3. Identify conflicts and trade-offs
        4. Score each option (0-100)
        5. Recommend top 1-2 options with conditions
        6. Flag anything requiring human escalation
        
        Output STRUCTURED decision:
        - trade_off_analysis: string
        - option_scores: [{option, score, reasoning}]
        - conflicts_detected: [{between, issue, resolution}]
        - recommendation: {option, confidence, conditions}
        - escalation_needed: bool
        - risk_score: 0-12
        """},
        {"role": "user", "content": f"""
        TASK: {state['task']}
        
        CTO ANALYSIS:
        {state.get('cto_output', 'Not available')}
        
        COO ANALYSIS:
        {state.get('coo_output', 'Not available')}
        
        LEGAL ANALYSIS:
        {state.get('legal_output', 'Not available')}
        
        RISK ANALYSIS:
        {state.get('risk_output', 'Not available')}
        
        COST ANALYSIS:
        {state.get('cost_output', 'Not available')}
        """}
    ])
    
    decision = parse_reconcile_output(response)
    
    return {
        "reconcile_decision": decision,
        "reconcile_score": decision.get("confidence", 0),
        "risk_score": decision.get("risk_score", 0),
        "messages": [response]
    }
```

### 3.4 Human Review Node

```python
from langgraph.types import interrupt

def human_review_node(state: EMADSState) -> dict:
    """
    Human Review Gate — BẮT BUỘC trước khi execute.
    Dùng LangGraph interrupt() để pause và chờ human input.
    """
    
    # Prepare review summary
    review_summary = f"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📋 REVIEW REQUIRED
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Task: {state['task']}
    Risk Score: {state['risk_score']}/12
    
    ReconcileGPT Recommendation:
    {state['reconcile_decision']}
    
    Options: APPROVE / EDIT / REJECT
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    
    # Interrupt execution — wait for human
    human_response = interrupt(review_summary)
    
    return {
        "human_approved": human_response.get("approved", False),
        "human_feedback": human_response.get("feedback", ""),
    }
```

### 3.5 Execution & Monitor Nodes

```python
def execution_node(state: EMADSState) -> dict:
    """Execute the approved plan"""
    plan = state["reconcile_decision"]["recommendation"]
    
    # Execute based on plan type
    if plan.get("requires_pr"):
        result = create_agent_pr(plan)
    else:
        result = execute_plan_direct(plan)
    
    return {
        "execution_result": result,
        "total_cost_usd": state.get("total_cost_usd", 0) + result.get("cost", 0)
    }

def monitor_node(state: EMADSState) -> dict:
    """Monitor execution results, decide if re-plan needed"""
    result = state["execution_result"]
    
    success = evaluate_execution(result)
    
    if success:
        return {"messages": [{"role": "system", "content": "✅ Execution complete"}]}
    else:
        return {
            "messages": [{"role": "system", "content": "⚠️ Re-plan needed"}],
            "iteration_count": state["iteration_count"] + 1
        }
```

---

## 4. Graph Construction

### 4.1 Full EMADS-PR Graph

```python
from langgraph.graph import StateGraph, END, START

def build_emads_graph():
    """Build the complete EMADS-PR LangGraph"""
    
    graph = StateGraph(EMADSState)
    
    # ── Add Nodes ──
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("cto_agent", cto_agent_node)
    graph.add_node("coo_agent", coo_agent_node)
    graph.add_node("legal_agent", legal_agent_node)
    graph.add_node("risk_agent", risk_agent_node)
    graph.add_node("cost_agent", cost_agent_node)
    graph.add_node("reconcile_gpt", reconcile_gpt_node)
    graph.add_node("human_review", human_review_node)
    graph.add_node("execution", execution_node)
    graph.add_node("monitor", monitor_node)
    
    # ── Entry Point ──
    graph.add_edge(START, "orchestrator")
    
    # ── Orchestrator → Parallel Specialists ──
    # Fan-out: Orchestrator dispatches to ALL specialists in parallel
    graph.add_edge("orchestrator", "cto_agent")
    graph.add_edge("orchestrator", "coo_agent")
    graph.add_edge("orchestrator", "legal_agent")
    graph.add_edge("orchestrator", "risk_agent")
    graph.add_edge("orchestrator", "cost_agent")
    
    # ── Fan-in: All specialists → ReconcileGPT ──
    graph.add_edge("cto_agent", "reconcile_gpt")
    graph.add_edge("coo_agent", "reconcile_gpt")
    graph.add_edge("legal_agent", "reconcile_gpt")
    graph.add_edge("risk_agent", "reconcile_gpt")
    graph.add_edge("cost_agent", "reconcile_gpt")
    
    # ── ReconcileGPT → Human Review ──
    graph.add_edge("reconcile_gpt", "human_review")
    
    # ── Human Review → Conditional Routing ──
    graph.add_conditional_edges(
        "human_review",
        route_after_review,
        {
            "execute": "execution",
            "replan": "orchestrator",
            "end": END
        }
    )
    
    # ── Execution → Monitor ──
    graph.add_edge("execution", "monitor")
    
    # ── Monitor → Conditional ──
    graph.add_conditional_edges(
        "monitor",
        route_after_monitor,
        {
            "complete": END,
            "replan": "orchestrator"
        }
    )
    
    return graph.compile(
        checkpointer=MemorySaver(),  # Persistence
        interrupt_before=["human_review"]  # Pause for human
    )

# ── Routing Functions ──

def route_after_review(state: EMADSState) -> str:
    """Route based on human review decision"""
    if state.get("human_approved"):
        return "execute"
    elif state.get("human_feedback"):
        return "replan"  # Re-plan with feedback
    else:
        return "end"  # Rejected

def route_after_monitor(state: EMADSState) -> str:
    """Route based on monitoring results"""
    if state.get("iteration_count", 0) > 3:
        return "complete"  # Max iterations
    
    result = state.get("execution_result", {})
    if result.get("success"):
        return "complete"
    else:
        return "replan"
```

### 4.2 Visual Graph

```
                    START
                      │
                      ▼
               ┌──────────────┐
               │ Orchestrator │
               └──────┬───────┘
                      │ (fan-out parallel)
          ┌───┬───┬───┼───┬───┐
          ▼   ▼   ▼   ▼   ▼   ▼
        CTO COO Legal Risk Cost
          │   │   │   │   │
          └───┴───┴───┼───┴───┘
                      │ (fan-in)
                      ▼
              ┌───────────────┐
              │ ReconcileGPT  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Human Review  │ ← interrupt()
              └───────┬───────┘
                 ┌────┼────┐
              approve edit reject
                 │    │    │
                 ▼    │    ▼
            Execution │   END
                 │    │
                 ▼    │
              Monitor │
                 │    │
            ┌────┴────┘
         success  fail
            │      │
            ▼      ▼
           END  → Orchestrator (re-plan loop)
```

---

## 5. Running the Graph

### 5.1 Basic Execution

```python
from langgraph.checkpoint.memory import MemorySaver

# Build graph
app = build_emads_graph()

# Run with input
config = {"configurable": {"thread_id": "task-001"}}

result = app.invoke(
    {
        "task": "Should we migrate our monolith to microservices?",
        "ceo_input": "Budget: $200K, Timeline: 6 months, Team: 8 devs",
        "constraints": {
            "budget_usd": 200000,
            "timeline_months": 6,
            "team_size": 8,
            "risk_tolerance": "medium"
        },
        "iteration_count": 0,
        "total_cost_usd": 0.0,
        "risk_score": 0,
        "automation_score": 0
    },
    config=config
)
```

### 5.2 Handling Human Review (Resume after interrupt)

```python
# Graph pauses at human_review node
# Get current state
state = app.get_state(config)

# Human provides feedback
app.update_state(
    config,
    {
        "human_approved": True,
        "human_feedback": "Approved with condition: start with 2 services only"
    }
)

# Resume execution
result = app.invoke(None, config=config)
```

### 5.3 Streaming Execution

```python
async for event in app.astream(initial_state, config=config):
    for node_name, output in event.items():
        print(f"🔄 {node_name}:")
        if "messages" in output:
            print(f"   {output['messages'][-1].content[:200]}...")
        if "risk_score" in output:
            print(f"   Risk Score: {output['risk_score']}/12")
```

---

## 6. Production Patterns

### 6.1 Persistence (Checkpoint)

```python
# PostgreSQL checkpointer cho production
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost:5432/emads"
)

app = build_emads_graph().compile(checkpointer=checkpointer)
```

### 6.2 LangSmith Tracing

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls-..."
os.environ["LANGCHAIN_PROJECT"] = "EMADS-PR-v1"

# All LangGraph runs automatically traced
# View at: https://smith.langchain.com
```

### 6.3 Error Recovery

```python
from langgraph.errors import GraphRecursionError

try:
    result = app.invoke(state, config=config)
except GraphRecursionError:
    # Max iterations reached
    state = app.get_state(config)
    alert("EMADS-PR max iterations reached", state)
except Exception as e:
    # Recover from checkpoint
    state = app.get_state(config)
    log_error(e, state)
    # Can resume from last successful checkpoint
```

---

## 7. Key Takeaways cho Training

1. **LangGraph = best framework** cho EMADS-PR — native state machine, parallel, human-in-the-loop
2. **State = single source of truth** — TypedDict tracking mọi thứ
3. **Parallel fan-out** — 5 specialists chạy đồng thời, fan-in vào ReconcileGPT
4. **interrupt()** — pause graph tại human review, resume khi approved
5. **Conditional routing** — approve → execute, edit → re-plan, reject → end
6. **Checkpoints** — persistence cho recovery, resume from crash
7. **LangSmith** — tracing mọi run, debug production issues
8. **Max 3 re-plan loops** — prevent infinite iteration

---

## Nguồn tham khảo
- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
- LangGraph Examples: Multi-Agent Patterns
- LangSmith: Observability for LLM Apps
- EMADS-PR Architecture (File 01)
