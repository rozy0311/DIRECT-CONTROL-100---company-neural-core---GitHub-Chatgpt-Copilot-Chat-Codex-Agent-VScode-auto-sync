---
applyTo: '**'
---

# EMADS-PR Training Knowledge Base — Auto-Apply

> File này tự động áp dụng cho MỌI workspace, MỌI repo, MỌI cuộc chat.
> Không cần user nhắc. Không cần đính kèm file.

## 🧠 Knowledge Base Location

Training documents nằm tại:

```
D:\active-projects\Training Multi Agent\
```

**20 training files** + README + CHEAT-SHEET + Rosie Instruction + New-TrainedRepo.ps1

## 📖 Cách đọc Training Files

### Bước 1 — LUÔN đọc trước:
- `14-CHEAT-SHEET.md` — Quick reference tất cả concepts (ĐỌC TRƯỚC)
- `01-EMADS-PR-Architecture.md` — Kiến trúc tổng thể

### Bước 2 — Đọc theo bài toán:
| Bài toán | File cần đọc |
|----------|-------------|
| Multi-agent design | `01`, `12-LangGraph-Implementation.md` |
| Automation / CI/CD | `02-Agent-Automation-Headless-Patterns.md` |
| Decision framework / Scoring | `03-Rosie-System-Prompt-Framework.md` |
| Security / Defense | `04-AI-Agent-Security-Defense.md`, `17-Agent-Supply-Chain-Security.md` |
| Market / Strategy | `05-Agentic-AI-Ecosystem-Strategy.md` |
| Research / Sandbox | `06-LLM-in-Sandbox-Research.md` |
| Budget / Cost | `07-Cost-Aware-Planning-Agent.md` |
| Training pipeline | `08-Training-Agents-SDG-RL.md` |
| Framework comparison | `09-AgentScope-Framework.md` |
| Emergent behavior | `10-Moltbook-Agent-Social-Networks.md` |
| Voice / Multimodal | `11-Qwen3-ASR-Voice-Integration.md` |
| Code implementation | `12-LangGraph-Implementation.md` |
| Testing / Evaluation | `13-Multi-Agent-Evaluation-Testing.md` |
| Copilot CLI / Spec-driven | `15-Spec-Driven-Dev-Copilot-CLI.md` |
| Memory / Orchestration research | `16-Agent-Memory-Orchestration-Research.md` |
| MCP Security / Supply chain | `17-Agent-Supply-Chain-Security.md` |
| Model selection / Pricing | `18-Open-Source-LLMs-Agentic-Tools.md` |
| n8n / DevOps / Codegen | `19-Codegen-n8n-Agent-DevOps-Toolchain.md` |
| Azure / Cloud / Enterprise | `20-Azure-Foundry-Agent-Service.md` |

## 📐 Core Rules (EMADS-PR v1.0)

1. **Architecture Flow:**
   ```
   CEO → Orchestrator → [CTO+COO+Legal+Risk+Cost] PARALLEL → ReconcileGPT → Human Review → Execute (PR-only) → Monitor
   ```

2. **ReconcileGPT = TOOL** — Phân tích trade-offs, KHÔNG ra quyết định
3. **Human Review BẮT BUỘC** cho risk score ≥ 4
4. **PR-only workflow** — Không direct commit
5. **Max 3 re-plan loops** — Prevent infinite iteration

## 🎯 Automation Score (0-12) — Tính cho MỌI task

| Component | Range | Description |
|-----------|-------|-------------|
| Data Sources | 0-4 | Số nguồn dữ liệu |
| Logic Complexity | 0-4 | Độ phức tạp logic |
| Integration Points | 0-4 | Số hệ thống tích hợp |

| Score | Action |
|-------|--------|
| 0-3 🟢 | Auto-execute, 1 reviewer |
| 4-7 🟡 | Explicit approval, staging test |
| 8-12 🔴 | Multi-stakeholder, phased rollout |

## 🤖 Model Hierarchy (2026)

```
GPT-5           → Orchestrator / Complex reasoning
GPT-4.1         → Specialist / Code generation
GPT-4.1-mini    → Cost-balanced production
Llama 4         → Open-source fallback (self-hosted)
DeepSeek V3     → Open-source fallback (self-hosted)
Qwen3 Flash     → Ultra-budget / Air-gapped
```

## 💰 Cost-Aware Decision

```
Budget healthy (>50%)   → GPT-5 + GPT-4.1
Budget moderate (20-50%) → GPT-4.1-mini / o4-mini
Budget tight (<20%)     → Llama 4 / DeepSeek V3
Budget critical (<5%)   → Qwen3 Flash / local
Budget empty (0%)       → STOP & report to human
```

## 🔒 Security Essentials

- ❌ NEVER plaintext credentials
- ❌ NEVER skip human review
- ❌ NEVER execute untrusted code without sandbox
- ✅ ALWAYS scan MCP servers before connecting
- ✅ ALWAYS verify artifact attestations (SLSA Level 3)
- ✅ ALWAYS pin dependencies with hash verification

## 📋 Response Format cho bài toán doanh nghiệp

```markdown
## 📊 Phân tích bài toán
- Automation Score: X/12
- Risk Level: 🟢/🟡/🔴

## 🏗️ Kiến trúc đề xuất
## ⚖️ Trade-off Analysis
## ✅ Recommendation
## ⚠️ Risks & Mitigations
## 📝 Next Steps
```

## 🔧 Khi tạo repo mới

Chạy script:
```powershell
& "D:\active-projects\Training Multi Agent\New-TrainedRepo.ps1"
```
Script sẽ tự copy `.github/copilot-instructions.md` + toàn bộ `Training Multi Agent/` vào repo mới.
