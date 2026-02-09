````instructions
# Copilot Instructions — EMADS-PR Enterprise Multi-Agent System

> Tự động áp dụng cho MỌI cuộc chat với GitHub Copilot trong repo này.

---

## 🧠 Knowledge Base

Trước khi giải quyết bất kỳ bài toán doanh nghiệp nào, **đọc training files** tại:

```
D:\active-projects\Training Multi Agent\
```

### Thứ tự ưu tiên đọc:

| Priority | File | Khi nào đọc |
|----------|------|-------------|
| 🔴 LUÔN ĐỌC | `14-CHEAT-SHEET.md` | Mọi bài toán — quick reference tất cả concepts |
| 🔴 LUÔN ĐỌC | `01-EMADS-PR-Architecture.md` | Mọi bài toán — kiến trúc tổng thể |
| 🟡 KHI CẦN | `03-Rosie-System-Prompt-Framework.md` | Khi cần decision framework, scoring |
| 🟡 KHI CẦN | `12-LangGraph-Implementation.md` | Khi cần code multi-agent |
| 🟡 KHI CẦN | `02-Agent-Automation-Headless-Patterns.md` | Khi cần automation, CI/CD, PR workflow |
| 🟡 KHI CẦN | `07-Cost-Aware-Planning-Agent.md` | Khi cần budget/cost analysis |
| 🟡 KHI CẦN | `04-AI-Agent-Security-Defense.md` | Khi cần security review |
| 🟡 KHI CẦN | `13-Multi-Agent-Evaluation-Testing.md` | Khi cần testing strategy |
| 🟡 KHI CẦN | `15-Spec-Driven-Dev-Copilot-CLI.md` | Khi dùng Copilot CLI, spec-driven dev, /delegate |
| 🟡 KHI CẦN | `17-Agent-Supply-Chain-Security.md` | Khi cần MCP security, supply chain, SLSA |
| 🟡 KHI CẦN | `18-Open-Source-LLMs-Agentic-Tools.md` | Khi chọn model, pricing, self-hosted LLM |
| 🟡 KHI CẦN | `19-Codegen-n8n-Agent-DevOps-Toolchain.md` | Khi cần n8n workflow, Codegen SDK, DevOps |
| � KHI CẦN | `20-Azure-Foundry-Agent-Service.md` | Khi cần Azure cloud agent, Foundry, enterprise scale, hybrid architecture |
| �🟢 THAM KHẢO | `05-Agentic-AI-Ecosystem-Strategy.md` | Market & strategy context |
| 🟢 THAM KHẢO | `06-LLM-in-Sandbox-Research.md` | Research references |
| 🟢 THAM KHẢO | `08-Training-Agents-SDG-RL.md` | Training pipeline design |
| 🟢 THAM KHẢO | `09-AgentScope-Framework.md` | Framework alternatives |
| 🟢 THAM KHẢO | `10-Moltbook-Agent-Social-Networks.md` | Emergent behavior awareness |
| 🟢 THAM KHẢO | `11-Qwen3-ASR-Voice-Integration.md` | Voice/multimodal features |
| 🟢 THAM KHẢO | `16-Agent-Memory-Orchestration-Research.md` | ReasoningBank, evolving orchestration research |

---

## 📐 Core Architecture: EMADS-PR v1.0

Mọi bài toán doanh nghiệp phải tuân theo flow:

```
CEO Input
  → Orchestrator (route + memory)
    → [CTO + COO + Legal + Risk + Cost] (PARALLEL)
      → ReconcileGPT (analyze trade-offs, KHÔNG ra quyết định)
        → Human Review (BẮT BUỘC)
          → Execute (PR-only, KHÔNG direct commit)
            → Monitor (KPI check)
```

### Rules bắt buộc:
- **ReconcileGPT = TOOL**, không phải decision maker
- **Human Review = BẮT BUỘC** cho mọi task có risk score ≥ 4
- **PR-only workflow** — không bao giờ direct commit
- **Max 3 re-plan loops** — prevent infinite iteration

---

## 🎯 Automation Complexity Score (0-12)

Tính cho MỌI task trước khi thực hiện:

- **Data Sources (0-4):** Số nguồn dữ liệu cần truy cập
- **Logic Complexity (0-4):** Độ phức tạp logic xử lý
- **Integration Points (0-4):** Số hệ thống cần tích hợp

| Score | Level | Action Required |
|-------|-------|-----------------|
| 0-3 | 🟢 LOW | Auto-execute OK, 1 reviewer |
| 4-7 | 🟡 MEDIUM | Explicit approval, staging test |
| 8-12 | 🔴 HIGH | Multi-stakeholder, phased rollout |

---

## 🔒 Security Rules

1. ❌ NEVER plaintext credentials
2. ❌ NEVER expose agent ports to public
3. ❌ NEVER skip human review
4. ❌ NEVER execute untrusted code without sandbox
5. ✅ ALWAYS sanitize inputs (prompt injection defense)
6. ✅ ALWAYS use least privilege
7. ✅ ALWAYS log agent actions for audit
8. ✅ ALWAYS scan MCP servers before connecting (supply chain risk)
9. ✅ ALWAYS verify artifact attestations (SLSA Level 3)
10. ✅ ALWAYS pin dependencies with hash verification

---

## 🔗 Supply Chain & MCP Security

Khi tích hợp MCP servers hoặc external tools:

1. **Scan trước khi connect** — Kiểm tra tool poisoning, rug pull, shadowing
2. **Pin versions** — Lock MCP server versions, không auto-update
3. **Verify attestations** — SLSA Level 3 cho mọi artifact
4. **CodeQL + Dependabot** — Bật cho mọi repo
5. **Least privilege** — MCP server chỉ được access resources cần thiết

---

## 🤖 LLM Selection Guide (2026)

| Scenario | Model | Lý do |
|----------|-------|-------|
| Orchestrator / Complex reasoning | GPT-5 | Best quality, multi-agent orchestration |
| Specialist / Code generation | GPT-4.1 | Optimized for code + tool-use |
| Cost-balanced production | GPT-4.1-mini / o4-mini | 90% quality, 1/10 cost |
| Open-source fallback | Llama 4 / DeepSeek V3 | Self-hosted, no API cost |
| Ultra-budget / Air-gapped | Qwen3 Flash / Phi-4 | Zero API cost, full control |

---

## 💰 Cost-Aware Decision

```
Budget healthy (>50%)  → GPT-5 (orchestrator) + GPT-4.1 (specialist)
Budget moderate (20-50%) → GPT-4.1-mini / o4-mini (balanced)
Budget tight (<20%)    → Llama 4 / DeepSeek V3 (open-source)
Budget critical (<5%)  → Qwen3 Flash / local heuristics
Budget empty (0%)      → STOP & report to human
```

---

## 🛠️ Decision Matrix

Cho MỌI technology choice, chạy qua 3 filters:

1. **FUNDAMENTALS** → Giải quyết đúng vấn đề chưa?
2. **LOCAL-FIRST** → Data sensitive? Low latency? Cost tight?
3. **CLOUD-ONLY** → Scale >1000 rps? Multi-region? GPU needed?

Nếu không có rollback plan → **KHÔNG deploy**.

---

## 📋 Response Format

Khi giải quyết bài toán doanh nghiệp, cấu trúc response:

```markdown
## 📊 Phân tích bài toán
- Automation Score: X/12 (breakdown: Data Y + Logic Z + Integration W)
- Risk Level: 🟢/🟡/🔴

## 🏗️ Kiến trúc đề xuất
(agents involved, data flow)

## ⚖️ Trade-off Analysis (ReconcileGPT style)
- Option A: ...
- Option B: ...
- Conflicts: ...

## ✅ Recommendation
- Best option + conditions
- Estimated cost & timeline

## ⚠️ Risks & Mitigations
(risk table with probability/impact/mitigation)

## 📝 Next Steps
(actionable items, ordered by priority)
```

---

## 📝 Spec-Driven Development

Khi tạo feature mới, dùng Markdown-as-Code workflow:

```
1. main.md (spec)  →  2. compile.prompt.md  →  3. Code generation
```

- Viết spec trước, code sau — **spec = single source of truth**
- Dùng Copilot CLI `/delegate` cho autonomous multi-file implementation
- Mọi spec phải có: Problem, Constraints, Acceptance Criteria, EMADS-PR agent mapping

---

## 🔧 DevOps Toolchain

| Layer | Tool | Mục đích |
|-------|------|----------|
| Workflow Automation | n8n (self-hosted) | Agent orchestration, webhook triggers |
| Code Generation | Codegen SDK | API-driven SWE at scale |
| Vector Memory | Milvus/Qdrant | Agent long-term memory |
| CI/CD | GitHub Actions | Build, test, deploy pipeline |
| Security | CodeQL + Dependabot | Vulnerability scanning |
| Monitoring | Azure Monitor | Agent performance tracking |

---

## 🏢 Project Context

- **Repo:** (your-org/your-repo)
- **Branch:** main
- **System:** EMADS-PR Enterprise Multi-Agent AI
- **Agent:** Rosie — Dual Brain Ops OS (Level-6 Hybrid) COO-CTO Agent v2.3
- **Language:** Vietnamese (primary) + English (technical terms)

````
