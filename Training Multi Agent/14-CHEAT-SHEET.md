# 14 — 🧠 CHEAT SHEET: Multi-Agent Enterprise AI — Tổng hợp nhanh

> **Dùng khi:** Cần tra cứu nhanh bất kỳ concept nào trong hệ thống EMADS-PR

---

## ⚡ EMADS-PR Flow (30 giây)

```
CEO Input
  → Orchestrator (route + memory)
    → [CTO + COO + Legal + Risk + Cost] (PARALLEL)
      → ReconcileGPT (analyze trade-offs + score)
        → Human Review (APPROVE / EDIT / REJECT)
          → Execute (PR-only)
            → Monitor (KPI check)
              → ✅ Done  OR  🔄 Re-plan (max 3 loops)
```

---

## 🎯 Automation Complexity Score (0-12)

| Score | Level | Action |
|-------|-------|--------|
| 0-3 | 🟢 LOW | Auto-execute OK, 1 reviewer |
| 4-7 | 🟡 MED | Explicit approval, staging test |
| 8-12 | 🔴 HIGH | Multi-stakeholder, phased rollout |

**Tiêu chí:** Data Sources (0-4) + Logic Complexity (0-4) + Integration Points (0-4)

---

## 🔐 Security 5 Layers

```
1. WAF/API Gateway     — Edge protection
2. OAuth2/OIDC         — Authentication
3. Agent Mesh (mTLS)   — Agent-to-agent encryption
4. Vault (HSM)         — Secret management
5. SIEM/SOC            — Detection & alerting
```

**Zero tolerance rules:**
- ❌ NEVER plaintext credentials
- ❌ NEVER expose agent ports to internet
- ❌ NEVER skip human review
- ✅ ALWAYS least privilege
- ✅ ALWAYS sanitize input

---

## 🏗️ RACI Quick Reference

| Decision Type | Accountable | Consulted |
|---------------|-------------|-----------|
| Tech/Architecture | CTO | COO |
| Operations/Resources | COO | CTO |
| Cross-functional | CEO | CTO + COO |
| ReconcileGPT role | — | Always TOOL, never decision maker |

---

## 💰 Cost-Aware Planning

```python
Budget healthy (>50%)  → GPT-4o (best quality)
Budget tight (20-50%)  → GPT-4o-mini (balanced)
Budget critical (<20%) → Local/heuristics (free)
Budget empty (0%)      → STOP & report
```

**Track:** tokens + latency + tool_calls + cost_usd

---

## 🛠️ Framework Comparison

| Need | Use |
|------|-----|
| State machine + Human-in-loop | **LangGraph** ⭐ |
| Quick prototype | **CrewAI** |
| Distributed agents | **AgentScope** |
| Research/experiment | **AutoGen** |

---

## 📊 LangGraph Code Pattern

```python
# 1. Define State
class EMADSState(TypedDict):
    task: str
    cto_output: Optional[dict]
    reconcile_decision: Optional[dict]
    human_approved: Optional[bool]
    risk_score: int

# 2. Build Graph
graph = StateGraph(EMADSState)
graph.add_node("orchestrator", orchestrator_fn)
graph.add_node("cto", cto_fn)
graph.add_node("reconcile", reconcile_fn)
graph.add_node("human_review", human_fn)

# 3. Add Edges (parallel + conditional)
graph.add_edge("orchestrator", "cto")  # fan-out
graph.add_edge("cto", "reconcile")     # fan-in
graph.add_conditional_edges("human_review", route_fn)

# 4. Compile with persistence
app = graph.compile(checkpointer=MemorySaver())

# 5. Run
result = app.invoke(state, config={"thread_id": "001"})

# 6. Resume after human review
app.update_state(config, {"human_approved": True})
app.invoke(None, config)
```

---

## 🧪 Testing Checklist

```
□ Component: Tools work correctly
□ Unit: Each agent produces structured output
□ Consistency: Same input → same direction (≥80%)
□ Integration: Agents communicate correctly
□ E2E: Full pipeline completes
□ Adversarial: Prompt injection blocked (100%)
□ Budget: Stays within cost limits
□ Recovery: Resume from checkpoint works
```

---

## 📐 Decision Matrix (LUÔN chạy trước khi chọn tech)

```
1. FUNDAMENTALS → Giải quyết đúng vấn đề chưa?
2. LOCAL-FIRST  → Data sensitive? Low latency? Cost tight?
3. CLOUD-ONLY   → Scale >1000 rps? Multi-region? GPU needed?
4. ROLLBACK     → Plan B có chưa? Không có = KHÔNG deploy
```

---

## 🌐 Market Numbers

- **$267B** — Agentic AI market by 2030
- **$120B** — AI impact on Vietnam GDP by 2040
- **22%** — Employees using Shadow AI (no IT approval)
- **2000x** — Qwen3-ASR-0.6B throughput at concurrency 128

---

## 🔬 Research Highlights

| Paper/Project | Key Insight |
|---------------|-------------|
| **LLM-in-Sandbox** | LLM tự dùng code sandbox giải non-code tasks (+15-40% accuracy) |
| **RLVR/GRPO** | Train agent không cần reward model, chỉ verify output |
| **Moltbook** | AI agents tự tạo "tôn giáo" (Crustafarianism) = emergent behavior |
| **ClawdBot** | Exposed port + plaintext creds = disaster in hours |

---

## 🎤 Qwen3-ASR Quick Deploy

```bash
# Install
pip install -U qwen-asr[vllm]

# Serve
qwen-asr-serve Qwen/Qwen3-ASR-1.7B --port 8000

# Use (OpenAI compatible)
curl http://localhost:8000/v1/chat/completions \
  -d '{"messages":[{"role":"user","content":[
    {"type":"audio_url","audio_url":{"url":"audio.wav"}}
  ]}]}'
```

---

## 📋 PR-Only Workflow

```
Agent detects change needed
  → Create branch: agent/type/timestamp
    → Apply changes (allowlist check)
      → Create PR with description
        → Auto checks: lint + test + security
          → Human review (risk-based)
            → Merge to main
```

**Risk-based review:**
- Score 0-3 → Auto-merge possible
- Score 4-7 → 1 reviewer required
- Score 8-12 → 2+ reviewers + senior approval

---

## 🚨 Escalation Triggers

| Trigger | Escalate to |
|---------|------------|
| Score > 8 | CTO + COO meeting |
| Budget > $10K | CFO/CEO approval |
| Legal flag | Legal Agent review |
| Data breach risk | Security team ASAP |
| CTO ↔ COO conflict | ReconcileGPT analysis |

---

## 📁 File Map

```
Training Multi Agent/
├── 01 EMADS-PR Architecture         ⭐⭐⭐⭐⭐
├── 02 Agent Automation Patterns      ⭐⭐⭐⭐⭐
├── 03 Rosie System Prompt            ⭐⭐⭐⭐⭐
├── 04 AI Agent Security              ⭐⭐⭐⭐⭐
├── 05 Agentic AI Ecosystem           ⭐⭐⭐⭐
├── 06 LLM-in-Sandbox Research        ⭐⭐⭐⭐
├── 07 Cost-Aware Planning            ⭐⭐⭐⭐⭐
├── 08 Training Agents SDG+RL         ⭐⭐⭐⭐
├── 09 AgentScope Framework           ⭐⭐⭐⭐
├── 10 Moltbook Social Networks       ⭐⭐⭐⭐⭐ (RẤT QUAN TRỌNG)
├── 11 Qwen3-ASR Voice                ⭐⭐⭐
├── 12 LangGraph Implementation       ⭐⭐⭐⭐⭐
├── 13 Evaluation & Testing           ⭐⭐⭐⭐⭐
├── 14 CHEAT SHEET (file này)         📌 Quick ref
├── 15 Spec-Driven Dev + Copilot CLI  ⭐⭐⭐⭐⭐ 🆕
├── 16 Agent Memory & Orchestration   ⭐⭐⭐⭐⭐ 🆕
├── 17 Supply Chain Security          ⭐⭐⭐⭐⭐ 🆕
├── 18 Open-Source LLMs (MiniMax M2)  ⭐⭐⭐⭐⭐ 🆕
├── 19 Codegen + n8n + DevOps Tools   ⭐⭐⭐⭐⭐ 🆕
└── README.md                         📋 Master index
```

---

## 📝 Spec-Driven Development (30 giây)

```
main.md (spec) → compile.prompt.md → AI generates code
Edit spec → Recompile → Test → Repeat
NEVER edit generated code directly — edit spec only
```

**Key files:**
- `main.md` = source code (Markdown)
- `compile.prompt.md` = repeatable AI prompt
- `lint.prompt.md` = clean up spec

---

## 🧠 Agent Memory (ReasoningBank)

```
Task → Retrieve memories → Execute → Evaluate → Extract insights → Store
├─ Learn from BOTH success AND failure
├─ LLM-as-judge (no human labeling)
├─ Embedding-based retrieval
└─ MaTTS = Memory + Test-Time Scaling (positive feedback loop)
```

---

## 🤖 Open-Source LLM Selection

```
AGENTIC TASKS:    MiniMax M2 ← #1 open-source ($0.30/$1.20 per 1M)
BUDGET FALLBACK:  DeepSeek V3.2 ($0.28/$0.42)
ULTRA-BUDGET:     Qwen3 Flash ($0.022/$0.216)
BEST ACCURACY:    GPT-5 ($1.25/$10.00)
BEST SAFETY:      Claude Sonnet 4.5 ($3.00/$15.00)
```

---

## 🛡️ Supply Chain Security Checklist

```
□ Cisco MCP Scanner — scan all MCP servers
□ CodeQL — static analysis on all code
□ Dependabot — auto-fix vulnerable dependencies
□ SLSA Level 3 — artifact attestations
□ Pin GitHub Actions to commit SHAs
□ Secret scanning + push protection
□ AI-generated code → extra review required
```

---

## 🔧 Agent DevOps Toolchain

```
DEVELOP:  VS Code + Copilot + Spec-Driven Dev
AUTOMATE: n8n (self-hosted) + GitHub Actions
EXECUTE:  Codegen SDK (SWE at scale)
MEMORY:   Milvus vector DB + ReasoningBank
SECURE:   MCP Scanner + CodeQL + SLSA
MONITOR:  Telegram Bot + Prometheus/Grafana
TERMINAL: Copilot CLI (headless + /delegate)
```

---

*Last updated: 2026-02-08 | EMADS-PR v1.0 + v1.1 supplements*
