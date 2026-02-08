# 16 — Agent Memory (ReasoningBank) & Evolving Orchestration

> **Mục đích training:** Hiểu ReasoningBank — framework memory cho AI agents học từ kinh nghiệm, và Evolving Orchestration — puppeteer paradigm cho multi-agent collaboration, kết hợp reinforcement learning.

---

## 1. ReasoningBank — Memory Framework cho AI Agents

### 1.1 Vấn đề
```
HIỆN TẠI — AGENTS KHÔNG CÓ MEMORY:
├─ Mỗi task xử lý độc lập (isolated)
├─ Lặp lại sai lầm cũ
├─ Bỏ phí insights từ tasks trước
├─ Không phát triển skills theo thời gian
└─ Các memory cũ chỉ là "passive record-keeping"

GIẢI PHÁP — REASONINGBANK:
├─ Distill strategies từ cả SUCCESS & FAILURE
├─ Structured memory items (không phải raw logs)
├─ Embedding-based retrieval khi gặp task mới
├─ Continuous learning loop
└─ "Actionable, generalizable guidance for future decisions"
```

- **Tác giả:** University of Illinois Urbana-Champaign + Google Cloud AI Research
- **Paper:** [ReasoningBank](https://arxiv.org/abs/2509.25140)
- **Nguồn:** VentureBeat — "New memory framework builds AI agents that can handle the real world's unpredictability"

### 1.2 Cách hoạt động

```
┌─────────────────────────────────────────────────┐
│              REASONINGBANK LOOP                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. AGENT FACES NEW TASK                        │
│     └─ Embedding search → retrieve memories     │
│     └─ Insert memories into system prompt        │
│        │                                        │
│  2. AGENT EXECUTES TASK                         │
│     └─ Uses memory hints to guide actions       │
│     └─ Makes decisions with past context        │
│        │                                        │
│  3. EVALUATE OUTCOME                            │
│     └─ LLM-as-judge: success or failure?        │
│     └─ No human labeling needed                 │
│        │                                        │
│  4. EXTRACT INSIGHTS                            │
│     └─ FROM SUCCESS: distill strategies         │
│     └─ FROM FAILURE: distill preventive lessons │
│        │                                        │
│  5. MERGE INTO REASONINGBANK                    │
│     └─ Analyze + consolidate new memories       │
│     └─ Remove redundant items                   │
│     └─ Update existing strategies               │
│        │                                        │
│  → REPEAT (virtuous cycle)                      │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 1.3 Ví dụ thực tế

```
TASK: "Tìm tai nghe Sony trên web"

AGENT KHÔNG CÓ MEMORY:
├─ Search broad query → 4000+ results irrelevant
├─ Trial-and-error 8 steps → vẫn chưa đúng
├─ Tốn 8x token costs
└─ User experience kém

AGENT VỚI REASONINGBANK:
├─ Retrieve memory: "optimize search query" + "use category filter"
├─ Search "Sony headphones" + filter Electronics
├─ 2 steps → đúng ngay
├─ Tiết kiệm ~2x operational costs
└─ User experience tốt hơn
```

### 1.4 Memory-aware Test-Time Scaling (MaTTS)

```
STANDARD TEST-TIME SCALING:
├─ Generate multiple answers
├─ Pick best one
└─ Independent attempts (no learning)

MaTTS — MEMORY + SCALING:
├─ PARALLEL: Generate N trajectories → compare → find patterns
├─ SEQUENTIAL: Iteratively refine within single attempt
├─ Memory guides toward promising solutions
├─ Diverse experiences → higher-quality memories
└─ POSITIVE FEEDBACK LOOP: better memory → better scaling → better memory
```

### 1.5 Benchmark Results

| Benchmark | Improvement | Domain |
|-----------|------------|--------|
| **WebArena** | +8.3% success rate | Web browsing |
| **SWE-Bench-Verified** | Consistent improvement | Software engineering |
| **Cross-domain tasks** | Best generalization | Multi-domain |
| **Steps needed** | Reduced significantly | Efficiency |

**Tested with:** Gemini 2.5 Pro, Claude 3.7 Sonnet

---

## 2. Evolving Orchestration — Puppeteer Paradigm

### 2.1 Paper Overview
- **Tên:** Multi-Agent Collaboration via Evolving Orchestration
- **Venue:** Accepted at **NeurIPS 2025**
- **Tác giả:** Yufan Dang, Chen Qian et al. (OpenBMB / ChatDev team)
- **Link:** [arxiv:2505.19591](https://arxiv.org/abs/2505.19591)
- **Code:** [github.com/OpenBMB/ChatDev/tree/puppeteer](https://github.com/OpenBMB/ChatDev/tree/puppeteer)

### 2.2 Ý tưởng cốt lõi

```
VẤN ĐỀ VỚI MULTI-AGENT HIỆN TẠI:
├─ Static organizational structures
├─ Không adapt khi task complexity tăng
├─ Coordination overhead tăng theo số agents
├─ Inefficiency khi agent numbers grow
└─ Pre-defined workflows = rigid

GIẢI PHÁP — PUPPETEER PARADIGM:
├─ Centralized orchestrator ("puppeteer")
├─ Agents = "puppets" được direct dynamically
├─ Orchestrator trained via Reinforcement Learning
├─ Adaptive sequencing & prioritizing agents
└─ Flexible, evolvable collective reasoning
```

### 2.3 Architecture

```
┌─────────────────────────────────────────────────┐
│           PUPPETEER PARADIGM                     │
├─────────────────────────────────────────────────┤
│                                                 │
│              ┌──────────────┐                   │
│              │ ORCHESTRATOR │ ← RL-trained      │
│              │ (Puppeteer)  │                   │
│              └──────┬───────┘                   │
│                     │                           │
│          ┌──────────┼──────────┐                │
│          │          │          │                 │
│     ┌────▼───┐ ┌───▼────┐ ┌──▼─────┐          │
│     │Agent A │ │Agent B │ │Agent C │          │
│     │(Puppet)│ │(Puppet)│ │(Puppet)│          │
│     └────────┘ └────────┘ └────────┘          │
│                                                 │
│  KEY INSIGHT:                                   │
│  Orchestrator learns WHEN and HOW to             │
│  sequence agents through RL training,            │
│  discovering CYCLIC reasoning structures.        │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 2.4 Key Findings

| Finding | Detail |
|---------|--------|
| **Superior performance** | Outperforms static multi-agent structures |
| **Reduced computational costs** | More efficient agent sequencing |
| **Cyclic reasoning** | Emerges naturally — agents revisit previous conclusions |
| **Evolvable** | Orchestrator improves over time via RL |
| **Scalable** | Handles growing task complexity + agent numbers |

### 2.5 Cyclic Reasoning Structures

```
STATIC APPROACH (Linear):
  A → B → C → Output

EVOLVED APPROACH (Cyclic):
  A → B → C → A → B → Output
  
  WHY? Some problems need agents to REVISIT
  and REFINE earlier conclusions based on 
  new information from later agents.
  
  The orchestrator LEARNS this pattern via RL,
  discovering that cycling back improves quality.
```

---

## 3. Áp dụng cho EMADS-PR

### 3.1 ReasoningBank cho mỗi Agent Role

```python
# Concept: Memory bank per agent role
reasoning_banks = {
    "CTO": ReasoningBank(
        strategies=["architecture patterns", "tech debt assessment"],
        failure_lessons=["over-engineering risks", "scaling bottlenecks"]
    ),
    "COO": ReasoningBank(
        strategies=["resource allocation", "timeline estimation"],
        failure_lessons=["understaffing patterns", "vendor risks"]
    ),
    "ReconcileGPT": ReasoningBank(
        strategies=["conflict resolution patterns", "trade-off analysis"],
        failure_lessons=["false consensus detection"]
    )
}

# When new task arrives:
def process_with_memory(agent_role, task):
    bank = reasoning_banks[agent_role]
    
    # 1. Retrieve relevant memories
    memories = bank.retrieve(task, top_k=5)
    
    # 2. Inject into system prompt
    enhanced_prompt = f"""
    {agent_system_prompt}
    
    PAST EXPERIENCE (apply if relevant):
    {format_memories(memories)}
    """
    
    # 3. Execute task
    result = agent.invoke(enhanced_prompt, task)
    
    # 4. Extract new insights
    insights = bank.extract_insights(task, result)
    bank.merge(insights)
    
    return result
```

### 3.2 Evolving Orchestration cho EMADS-PR

```python
# Current EMADS-PR: Static flow
# CEO → Orchestrator → [CTO + COO + Legal + Risk + Cost] → Reconcile → Human

# Evolved EMADS-PR: RL-trained orchestrator
class EvolvedOrchestrator:
    def __init__(self):
        self.policy = RLPolicy()  # Trained via RL
    
    def route(self, task, agent_outputs, iteration):
        """Dynamically decide next agent(s) to invoke"""
        state = {
            "task": task,
            "outputs_so_far": agent_outputs,
            "iteration": iteration,
            "complexity": self.assess_complexity(task)
        }
        
        # RL policy decides:
        # - Which agents to invoke next
        # - Whether to cycle back to previous agents
        # - When to finalize and send to ReconcileGPT
        action = self.policy.decide(state)
        
        return action  # e.g., {"invoke": ["CTO", "COO"], "cycle_back": False}
```

### 3.3 Shared Memory across Sessions

```
SESSION 1: "Migrate database?"
├─ CTO recommends PostgreSQL → approved → success
└─ Memory stored: "PostgreSQL good for structured data, team familiar"

SESSION 2: "New microservice needs database"  
├─ CTO retrieves memory → immediately suggests PostgreSQL
├─ Adds: "Consider read replicas for high-traffic"
└─ Faster decision, consistent with previous choices

SESSION 3: "Performance issues with PostgreSQL"
├─ CTO retrieves both success + failure memories
├─ Learns: "Add connection pooling when >100 concurrent"
└─ More nuanced recommendations over time
```

---

## 4. Compositional Intelligence — Tương lai

```
HIỆN TẠI: Mỗi task = isolated
TƯƠNG LAI: Agent builds modular skills over time

Ví dụ cho Coding Agent:
├─ Task 1: API integration → learn skill "API patterns"
├─ Task 2: Database management → learn skill "DB operations"
├─ Task 3: Both API + DB needed → RECOMBINE learned skills
├─ Task 4: + Authentication → ADD new skill, RECOMBINE 3 skills
└─ → Agent autonomously assembles knowledge for complex workflows

"Over time, these modular skills become building blocks 
the agent can flexibly recombine to solve more complex tasks"
— Jun Yan, Google Research
```

---

## 5. Key Takeaways cho Agent

```
✅ ReasoningBank: memory framework học từ cả success & failure
✅ LLM-as-judge: tự đánh giá outcome, không cần human labeling
✅ MaTTS: kết hợp memory + test-time scaling = positive feedback loop
✅ Puppeteer paradigm: RL-trained orchestrator > static workflows
✅ Cyclic reasoning: agents revisit conclusions → better quality
✅ Shared memory: agents improve across sessions
✅ Compositional intelligence: modular skills → recombine for new tasks
✅ EMADS-PR upgrade path: ReasoningBank per agent + RL orchestrator
```

---

## 📚 Sources

- VentureBeat: [ReasoningBank Memory Framework](https://venturebeat.com/ai/new-memory-framework-builds-ai-agents-that-can-handle-the-real-worlds)
- arXiv: [ReasoningBank Paper](https://arxiv.org/abs/2509.25140)
- arXiv: [Multi-Agent Collaboration via Evolving Orchestration](https://arxiv.org/abs/2505.19591) — NeurIPS 2025
- GitHub: [ChatDev Puppeteer](https://github.com/OpenBMB/ChatDev/tree/puppeteer)
