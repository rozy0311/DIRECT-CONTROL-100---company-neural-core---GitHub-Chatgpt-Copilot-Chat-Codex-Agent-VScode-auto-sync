# 07 — Cost-Aware Planning Agent: Reasoning Under Budget Constraints

> **Mục đích training:** Hiểu cách xây dựng agent có khả năng lập kế hoạch tối ưu dưới ràng buộc ngân sách (tokens, latency, tool-calls), với code examples thực tế.

---

## 1. Tổng quan

### 1.1 Vấn đề
- AI agents thường optimize cho **accuracy** mà bỏ qua **cost**
- Trong production, resources có giới hạn: token budget, API call limits, latency SLA
- Cần agent biết **trade-off** giữa quality vs cost

### 1.2 Giải pháp: Cost-Aware Planning
- Agent lập kế hoạch **trước khi hành động**
- Mỗi bước có cost estimate
- Beam search tìm plan tối ưu trong budget constraints

---

## 2. Data Structures

### 2.1 Budget & Spend Tracking

```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Budget:
    """Ngân sách tổng cho một task"""
    max_tokens: int = 10000       # Token limit
    max_latency_ms: float = 5000  # Latency limit (ms)
    max_tool_calls: int = 5       # Max external API calls
    max_cost_usd: float = 0.50    # Max cost in USD

@dataclass
class Spend:
    """Chi tiêu hiện tại"""
    tokens_used: int = 0
    latency_ms: float = 0
    tool_calls: int = 0
    cost_usd: float = 0.0
    
    def within_budget(self, budget: Budget) -> bool:
        """Check if still within budget"""
        return (
            self.tokens_used <= budget.max_tokens and
            self.latency_ms <= budget.max_latency_ms and
            self.tool_calls <= budget.max_tool_calls and
            self.cost_usd <= budget.max_cost_usd
        )
    
    def remaining(self, budget: Budget) -> dict:
        """Get remaining budget"""
        return {
            "tokens": budget.max_tokens - self.tokens_used,
            "latency_ms": budget.max_latency_ms - self.latency_ms,
            "tool_calls": budget.max_tool_calls - self.tool_calls,
            "cost_usd": budget.max_cost_usd - self.cost_usd
        }
```

### 2.2 Step Options

```python
@dataclass
class StepOption:
    """Một option cho một bước trong kế hoạch"""
    name: str
    description: str
    execution_path: str  # "llm" hoặc "local" hoặc "tool"
    
    # Cost estimates
    estimated_tokens: int = 0
    estimated_latency_ms: float = 0
    estimated_tool_calls: int = 0
    estimated_cost_usd: float = 0.0
    
    # Quality estimate (0-1)
    expected_quality: float = 0.5
    
    # Dependencies
    requires: List[str] = field(default_factory=list)

@dataclass
class PlanCandidate:
    """Một plan hoàn chỉnh (sequence of steps)"""
    steps: List[StepOption]
    total_spend: Spend = field(default_factory=Spend)
    expected_quality: float = 0.0
    
    def calculate_totals(self):
        """Tính tổng cost/quality"""
        self.total_spend = Spend(
            tokens_used=sum(s.estimated_tokens for s in self.steps),
            latency_ms=sum(s.estimated_latency_ms for s in self.steps),
            tool_calls=sum(s.estimated_tool_calls for s in self.steps),
            cost_usd=sum(s.estimated_cost_usd for s in self.steps)
        )
        # Quality = product of step qualities (chain probability)
        self.expected_quality = 1.0
        for s in self.steps:
            self.expected_quality *= s.expected_quality
```

---

## 3. Planning Algorithm: Beam Search

### 3.1 Core Algorithm

```python
def beam_search_plan(
    task: str,
    budget: Budget,
    beam_width: int = 3,
    max_steps: int = 10
) -> PlanCandidate:
    """
    Beam search để tìm plan tối ưu trong budget.
    
    Strategy:
    - Expand top-k candidates at each step
    - Prune candidates that exceed budget
    - Select plan with highest quality within budget
    """
    
    # Initialize with empty plans
    candidates = [PlanCandidate(steps=[])]
    
    for step_num in range(max_steps):
        new_candidates = []
        
        for candidate in candidates:
            # Generate possible next steps
            options = generate_step_options(
                task=task,
                current_plan=candidate,
                remaining_budget=candidate.total_spend.remaining(budget)
            )
            
            for option in options:
                # Create new candidate with this option
                new_plan = PlanCandidate(
                    steps=candidate.steps + [option]
                )
                new_plan.calculate_totals()
                
                # Only keep if within budget
                if new_plan.total_spend.within_budget(budget):
                    new_candidates.append(new_plan)
        
        if not new_candidates:
            break  # No more valid plans
        
        # Keep top beam_width candidates by quality
        candidates = sorted(
            new_candidates,
            key=lambda c: c.expected_quality,
            reverse=True
        )[:beam_width]
        
        # Check if any candidate is "complete"
        complete = [c for c in candidates if is_plan_complete(c, task)]
        if complete:
            return max(complete, key=lambda c: c.expected_quality)
    
    # Return best candidate even if incomplete
    return max(candidates, key=lambda c: c.expected_quality)
```

### 3.2 Generate Step Options

```python
def generate_step_options(
    task: str,
    current_plan: PlanCandidate,
    remaining_budget: dict
) -> List[StepOption]:
    """
    Generate possible next steps, considering budget.
    Each step has LLM vs Local execution path.
    """
    
    options = []
    
    # Option 1: Use LLM (high quality, high cost)
    if remaining_budget["tokens"] > 1000:
        options.append(StepOption(
            name="llm_analysis",
            description="Use LLM for deep analysis",
            execution_path="llm",
            estimated_tokens=1500,
            estimated_latency_ms=2000,
            estimated_cost_usd=0.015,
            expected_quality=0.9
        ))
    
    # Option 2: Local execution (lower quality, no cost)
    options.append(StepOption(
        name="local_processing",
        description="Use local rules/heuristics",
        execution_path="local",
        estimated_tokens=0,
        estimated_latency_ms=50,
        estimated_cost_usd=0.0,
        expected_quality=0.6
    ))
    
    # Option 3: Tool call (medium cost, specific capability)
    if remaining_budget["tool_calls"] > 0:
        options.append(StepOption(
            name="tool_search",
            description="Use search tool for information",
            execution_path="tool",
            estimated_tokens=500,
            estimated_latency_ms=1000,
            estimated_tool_calls=1,
            estimated_cost_usd=0.005,
            expected_quality=0.85
        ))
    
    return options
```

---

## 4. LLM vs Local Execution Paths

### 4.1 Decision Matrix

```
TASK COMPLEXITY → LLM vs LOCAL

┌──────────────────────────────────────────────┐
│  Complexity     │  Budget OK  │  Budget Tight │
├─────────────────┼─────────────┼───────────────┤
│  Simple query   │  Local      │  Local        │
│  Analysis       │  LLM        │  Local+Cache  │
│  Creative       │  LLM        │  LLM (lower)  │
│  Computation    │  Local      │  Local        │
│  External data  │  Tool+LLM   │  Tool+Local   │
└──────────────────────────────────────────────┘
```

### 4.2 Hybrid Execution Pattern

```python
async def execute_step_adaptive(
    step: StepOption,
    spend: Spend,
    budget: Budget
) -> dict:
    """Execute step, adapting based on remaining budget"""
    
    remaining = spend.remaining(budget)
    budget_ratio = remaining["cost_usd"] / budget.max_cost_usd
    
    if budget_ratio < 0.2:
        # Budget almost depleted → force local
        return execute_local(step)
    
    elif budget_ratio < 0.5:
        # Budget getting tight → use smaller model
        return await execute_llm(step, model="gpt-4o-mini")
    
    else:
        # Budget healthy → use best model
        return await execute_llm(step, model="gpt-4o")
```

---

## 5. GRPO-Style Optimization

### 5.1 Concept
- **GRPO (Group Relative Policy Optimization)** — RL technique cho LLMs
- Thay vì reward model, so sánh **nhóm outputs** với nhau
- Agent học: "Plan A tốn ít hơn Plan B mà quality tương đương → prefer A"

### 5.2 Application cho Cost-Aware Planning
```
Training Loop:
1. Generate K plans cho cùng 1 task
2. Execute tất cả, measure actual cost + quality
3. Rank plans by (quality / cost) ratio
4. Update policy: prefer plans với ratio cao hơn
5. Over time: agent tự học optimize cost/quality trade-off
```

---

## 6. Integration vào EMADS-PR

### 6.1 Budget cho mỗi Agent

```python
# agents_budget.yaml
budgets:
  orchestrator:
    max_tokens: 50000
    max_latency_ms: 10000
    max_tool_calls: 20
    max_cost_usd: 5.00
  
  cto_agent:
    max_tokens: 20000
    max_latency_ms: 5000
    max_tool_calls: 10
    max_cost_usd: 2.00
  
  coo_agent:
    max_tokens: 15000
    max_latency_ms: 5000
    max_tool_calls: 5
    max_cost_usd: 1.50
  
  reconcile_gpt:
    max_tokens: 30000
    max_latency_ms: 8000
    max_tool_calls: 5
    max_cost_usd: 3.00
  
  total_task_budget:
    max_tokens: 200000
    max_cost_usd: 20.00
```

### 6.2 Cost Monitoring Dashboard

```python
def log_agent_spend(agent_name, step_name, spend: Spend):
    """Log spend for monitoring"""
    metrics.gauge(f"agent.{agent_name}.tokens_used", spend.tokens_used)
    metrics.gauge(f"agent.{agent_name}.cost_usd", spend.cost_usd)
    metrics.counter(f"agent.{agent_name}.tool_calls", spend.tool_calls)
    
    if spend.cost_usd > WARNING_THRESHOLD:
        alert(f"⚠️ {agent_name} cost warning: ${spend.cost_usd:.2f}")
```

---

## 7. Key Takeaways cho Training

1. **Cost-aware planning** = agent lập kế hoạch trước, tính cost mỗi bước
2. **Budget dataclass** — track tokens, latency, tool calls, cost USD
3. **Beam search** — tìm plan tối ưu quality/cost trong constraints
4. **LLM vs Local** — adaptive: budget tight → dùng local/small model
5. **GRPO optimization** — RL train agent prefer efficient plans
6. **Per-agent budgets** — mỗi agent trong EMADS-PR có budget riêng
7. **Real-time monitoring** — alert khi gần vượt budget

---

## Nguồn tham khảo
- MarkTechPost: "Building a Cost-Aware Planning Agent"
- GRPO Paper: "DeepSeek-Math: Group Relative Policy Optimization"
- LangChain: Token Usage Tracking
