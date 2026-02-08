# 18 — Open-Source LLMs cho Agentic Tool Calling (MiniMax M2 & Alternatives)

> **Mục đích training:** Hiểu MiniMax M2 — LLM open-source mạnh nhất cho agentic tool calling, so sánh với các alternatives, và cách chọn LLM phù hợp cho multi-agent system.

---

## 1. MiniMax M2 — King of Open-Source LLMs cho Agents

### 1.1 Overview
- **Model:** MiniMax-M2
- **Architecture:** Sparse Mixture-of-Experts (MoE)
- **Total Parameters:** 230 tỷ
- **Active Parameters:** 10 tỷ (per inference) — rất hiệu quả
- **License:** MIT — enterprise-friendly, free for commercial use
- **Company:** MiniMax (China) — backed by Alibaba & Tencent
- **Released:** October 2025

### 1.2 Tại sao quan trọng cho Agents?

```
MINIMAX M2 = #1 OPEN-SOURCE MODEL FOR AGENTIC TASKS:

├─ INTELLIGENCE INDEX: 61 points — highest open-weight globally
│   (chỉ sau GPT-5 high và Grok 4)
│
├─ AGENTIC BENCHMARKS:
│   ├─ τ²-Bench: 77.2 (GPT-5: 80.1)
│   ├─ BrowseComp: 44.0 (strongest open model)
│   ├─ FinSearchComp: 65.5 (best open-weight)
│   └─ SWE-bench: 69.4 (GPT-5: 74.9)
│
├─ CODING:
│   ├─ ArtifactsBench: 66.8 (beats Claude Sonnet 4.5)
│   ├─ Terminal-Bench: strong recovery from errors
│   └─ Multi-file code edits, CI/CD integration
│
└─ COST: $0.30/1M input, $1.20/1M output
    (vs GPT-5: $1.25/$10.00)
    (vs Claude Sonnet 4.5: $3.00/$15.00)
```

### 1.3 Kiến trúc MoE — Tại sao hiệu quả

```
DENSE MODEL (e.g., GPT-4):
├─ Tất cả parameters active mọi lúc
├─ 1000B params = cần 1000B compute
└─ Tốn GPU, chậm

SPARSE MOE (MiniMax M2):
├─ 230B total params
├─ Chỉ 10B active per inference (4.3%)
├─ "Expert routing" — chọn expert phù hợp cho task
├─ Kết quả: near-frontier quality, fraction of compute
└─ Chạy trên 4x NVIDIA H100 GPUs (FP8)
```

### 1.4 Interleaved Thinking — Reasoning Traces

```xml
<!-- MiniMax M2 maintains reasoning traces between steps -->
User: "Find the cheapest flight from HCM to Tokyo next week"

<think>
I need to:
1. Determine date range for "next week"
2. Search flights HCM → Tokyo
3. Compare prices across airlines
4. Consider connection vs direct flights
</think>

<tool_call name="search_flights">
  <param name="from">SGN</param>
  <param name="to">TYO</param>
  <param name="date_from">2026-02-09</param>
  <param name="date_to">2026-02-15</param>
</tool_call>

<think>
Results show:
- VietJet: $350 direct
- Vietnam Airlines: $420 direct
- ANA: $380 via Osaka (connection)
The cheapest is VietJet at $350.
Let me verify availability...
</think>

<!-- Key: Retain <think> tags when passing history to preserve reasoning -->
```

---

## 2. So sánh Open-Source LLMs cho Agent Workflows

### 2.1 Pricing Comparison (USD per 1M tokens)

| Provider | Model | Input | Output | Best For |
|----------|-------|-------|--------|----------|
| **MiniMax** | M2 | $0.30 | $1.20 | 🏆 Best value for agentic |
| OpenAI | GPT-5 | $1.25 | $10.00 | Highest accuracy |
| OpenAI | GPT-5 mini | $0.25 | $2.00 | Budget-friendly OpenAI |
| Anthropic | Claude Sonnet 4.5 | $3.00 | $15.00 | Safety + reasoning |
| Google | Gemini 2.5 Flash | $0.30 | $2.50 | Speed + multimodal |
| xAI | Grok-4 Fast | $0.20 | $0.50 | Cheapest frontier |
| DeepSeek | V3.2 | $0.28 | $0.42 | Cheapest overall |
| Alibaba | Qwen3 Flash | $0.022 | $0.216 | Ultra-budget |

### 2.2 Agentic Benchmark Comparison

| Benchmark | MiniMax M2 | GPT-5 | Claude 4.5 | DeepSeek V3.2 |
|-----------|-----------|-------|-------------|---------------|
| **τ²-Bench** | 77.2 | 80.1 | ~72 | ~68 |
| **SWE-bench** | 69.4 | 74.9 | ~65 | ~62 |
| **BrowseComp** | 44.0 | ~50 | ~35 | ~30 |
| **ArtifactsBench** | 66.8 | ~70 | 63.5 | ~58 |
| **Intelligence Index** | 61 | 72 | 58 | 52 |

### 2.3 Deployment Options

```
SELF-HOSTED (Open-Source):
├─ MiniMax M2 — 4x H100 GPUs (FP8)
├─ DeepSeek V3.2 — 8x H100 GPUs  
├─ Qwen3 — Various sizes, 1-8x GPUs
├─ Serve with: SGLang, vLLM (day-one support)
└─ Full control, no vendor lock-in

API-BASED:
├─ MiniMax Open Platform (free limited time)
├─ OpenAI API
├─ Anthropic API
├─ Google Vertex AI
└─ Compatible: OpenAI + Anthropic API standards
```

---

## 3. Chọn LLM cho EMADS-PR — Decision Matrix

### 3.1 Decision Tree

```
CHỌN LLM CHO AGENT:

Q1: Budget constraint?
├─ TIGHT (<$100/month) → DeepSeek V3.2 hoặc Qwen3 Flash
├─ MODERATE ($100-500) → MiniMax M2 API ⭐
└─ FLEXIBLE (>$500) → GPT-5 hoặc Claude Sonnet 4.5

Q2: Self-hosted or API?
├─ SELF-HOSTED (privacy, control)
│   ├─ Have 4+ H100 → MiniMax M2
│   ├─ Have 1-2 H100 → Qwen3 (smaller variants)
│   └─ No GPUs → API only
└─ API (convenience, scale)
    ├─ Best agentic → MiniMax M2 API
    ├─ Best overall → GPT-5
    └─ Best safety → Claude Sonnet 4.5

Q3: Primary use case?
├─ AGENTIC TOOL CALLING → MiniMax M2 ⭐
├─ CODING TASKS → GPT-5 or Claude
├─ REASONING/MATH → GPT-5 or Gemini 2.5 Pro
├─ COST-SENSITIVE AUTOMATION → DeepSeek V3.2
└─ MULTILINGUAL + VIETNAMESE → Qwen3 (good Vietnamese)
```

### 3.2 EMADS-PR Agent-Model Mapping

```python
# Dynamic model selection based on agent role + budget
MODEL_CONFIG = {
    "orchestrator": {
        "primary": "gpt-5-mini",       # Fast routing
        "fallback": "qwen3-flash"
    },
    "cto_agent": {
        "primary": "minimax-m2",       # Strong agentic + tool use
        "fallback": "deepseek-v3.2"
    },
    "coo_agent": {
        "primary": "minimax-m2",       # Cost-effective + capable
        "fallback": "deepseek-v3.2"
    },
    "legal_agent": {
        "primary": "claude-sonnet-4.5", # Best for safety/compliance
        "fallback": "gpt-5-mini"
    },
    "risk_agent": {
        "primary": "minimax-m2",       # Good reasoning
        "fallback": "deepseek-v3.2"
    },
    "cost_agent": {
        "primary": "qwen3-flash",      # Cheapest, simple calculations
        "fallback": "deepseek-v3.2"
    },
    "reconcile_gpt": {
        "primary": "gpt-5",           # Best accuracy for decisions
        "fallback": "minimax-m2"
    }
}

def select_model(agent_role, budget_remaining):
    config = MODEL_CONFIG[agent_role]
    
    if budget_remaining > budget_threshold * 0.5:
        return config["primary"]
    else:
        return config["fallback"]
```

---

## 4. MiniMax M2 — Tool Calling Guide

### 4.1 Setup

```python
from openai import OpenAI

# MiniMax supports OpenAI API standard
client = OpenAI(
    api_key="YOUR_MINIMAX_API_KEY",
    base_url="https://api.minimax.chat/v1"
)

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search product catalog",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "category": {"type": "string"},
                    "max_price": {"type": "number"}
                },
                "required": ["query"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="minimax-m2",
    messages=[{"role": "user", "content": "Find Sony headphones under $200"}],
    tools=tools,
    tool_choice="auto"
)
```

### 4.2 Self-Hosted Deployment

```bash
# Option 1: SGLang (recommended by MiniMax)
pip install sglang
python -m sglang.launch_server \
    --model MiniMaxAI/MiniMax-M2 \
    --tp 4 \
    --dtype float16

# Option 2: vLLM
pip install vllm
vllm serve MiniMaxAI/MiniMax-M2 \
    --tensor-parallel-size 4 \
    --dtype float16
```

---

## 5. MiniMax Timeline — Rapid Innovation

```
2024 Q4: MiniMax video-01 — viral AI video generation
2025 Q1: MiniMax-01 — 4M token context (industry record)
2025 Q2: MiniMax-M1 — 1M context, CISPO RL ($534K training cost!)
2025 Q4: MiniMax-M2 — #1 open-source for agentic tasks

KEY INSIGHT: Training costs dropping dramatically
├─ MiniMax M1: ~$534,700 (1/10th of DeepSeek R1)
├─ vs typical frontier models: $10M-$100M+
└─ Democratization of frontier AI capabilities
```

---

## 6. Key Takeaways cho Agent

```
✅ MiniMax M2 = #1 open-source LLM cho agentic tool calling
✅ 230B total / 10B active = frontier quality, fraction of compute
✅ MIT License = tự do deploy, fine-tune, thương mại
✅ Pricing: $0.30/$1.20 per 1M tokens = rất cạnh tranh
✅ Interleaved thinking = visible reasoning traces
✅ OpenAI + Anthropic API compatible = easy migration
✅ Self-host trên 4x H100 = full privacy + control
✅ EMADS-PR: dùng MiniMax M2 cho CTO/COO/Risk agents (cost-effective)
✅ DeepSeek V3.2 / Qwen3 Flash = budget fallback options
✅ Training costs đang giảm nhanh = AI democratization
```

---

## 📚 Sources

- VentureBeat: [MiniMax M2 — King of Open Source LLMs](https://venturebeat.com/ai/minimax-m2-is-the-new-king-of-open-source-llms-especially-for-agentic-tool)
- HuggingFace: [MiniMax M2 Model](https://huggingface.co/MiniMaxAI/MiniMax-M2)
- HuggingFace: [Tool Calling Guide](https://huggingface.co/MiniMaxAI/MiniMax-M2/blob/main/docs/tool_calling_guide.md)
- MiniMax: [Open Platform API](https://platform.minimax.io/docs/guides/platform-intro)
- MiniMax: [Agent Interface](https://agent.minimax.io/)
- Artificial Analysis: [Intelligence Index v3.0](https://artificialanalysis.ai/)
