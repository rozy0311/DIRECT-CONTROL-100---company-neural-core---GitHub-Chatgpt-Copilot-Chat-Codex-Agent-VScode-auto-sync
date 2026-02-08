# 15 — Spec-Driven Development & GitHub Copilot CLI

> **Mục đích training:** Hiểu phương pháp viết app bằng Markdown (spec-driven), workflow compile.prompt.md, và cách sử dụng GitHub Copilot CLI cho agentic workflows trong terminal.

---

## 1. Spec-Driven Development — Markdown là Ngôn ngữ lập trình

### 1.1 Ý tưởng cốt lõi
> **Viết toàn bộ ứng dụng trong file Markdown → Để AI coding agent "compile" thành code thực tế**

- **Tác giả:** Tomas Vesely (GitHub Engineering)
- **Nguồn:** GitHub Blog — "Spec-driven development: Using Markdown as a programming language when building with AI"
- **Ví dụ:** GitHub Brain MCP Server — viết hoàn toàn bằng Markdown, compile sang Go

### 1.2 Tại sao cần?
```
VẤN ĐỀ VỚI AI CODING AGENTS:
├─ Context loss — Agent quên purpose + past decisions
├─ Repetition — Phải giải thích lại đã nói gì
├─ Inconsistency — Suggest changes contradict earlier choices
├─ copilot-instructions.md — Giải quyết phần nào nhưng dễ quên update
└─ Spec drift — Specification & implementation out of sync

GIẢI PHÁP SPEC-DRIVEN:
├─ main.md = "source code" thực sự (Markdown)
├─ Agent luôn có full context khi compile
├─ Documentation = Implementation (luôn in sync)
├─ Dễ iterate: edit spec → recompile → test
└─ Language-agnostic: có thể compile sang bất kỳ ngôn ngữ
```

---

## 2. File Structure — 4 Files cốt lõi

### 2.1 Cấu trúc project

```
.
├── .github/
│   └── prompts/
│       ├── compile.prompt.md    # Prompt để compile spec → code
│       └── lint.prompt.md       # Prompt để clean up spec
├── main.go                      # Code thực tế (AI-generated)
├── main.md                      # 📌 "Source code" = Markdown spec
└── README.md                    # User-facing documentation
```

### 2.2 main.md — The Actual Source Code

```markdown
# GitHub Brain MCP Server

AI coding agent specification. User-facing documentation in [README.md](README.md).

## CLI
Implement CLI from [Usage](README.md#usage) section. 
Follow exact argument/variable names. Support only `pull` and `mcp` commands.

## pull
- Resolve CLI arguments and environment variables into `Config` struct:
  - `Organization`: Organization name (required)
  - `GithubToken`: GitHub API token (required)
  - `DBDir`: SQLite database path (default: `./db`)
- Pull items: Repositories, Discussions, Issues, Pull Requests, Teams
- Use `log/slog` custom logger

## Database
SQLite database in `{Config.DbDir}/{Config.Organization}.db`
Avoid transactions. Save each GraphQL item immediately.

### Tables
#### table:repositories
- Primary key: `name`
- Index: `updated_at`
- `name`: Repository name (without organization prefix)
- `has_discussions_enabled`: Boolean
```

**Key patterns:**
- **Links = Imports:** `[README.md](README.md#usage)` → embed documentation
- **Keywords:** `if`, `foreach`, `continue` — dùng tự nhiên trong spec
- **Structural + Declarative:** Mix between structure and logic
- **Variables:** Dùng inline code cho field names: `` `Config.DbDir` ``

### 2.3 compile.prompt.md — AI Prompt

```yaml
---
mode: agent
---

- Update the app to follow [the specification](../../main.md)
- Build the code with the VS Code tasks
- Fetch the GitHub home page for each used library for docs
```

### 2.4 lint.prompt.md — Spec Cleanup

```yaml
---
mode: agent
---

- Optimize [the app specification](../../main.md) for clarity
- Treat English as a programming language
- Minimize synonyms (pull/get/fetch → pick one term)
- Remove duplicate content
- Preserve all important details
- Do NOT modify Go code. Only optimize Markdown file.
```

---

## 3. Development Workflow

### 3.1 Loop chính

```
┌─────────────────────────────────────────────┐
│         SPEC-DRIVEN DEVELOPMENT LOOP         │
├─────────────────────────────────────────────┤
│                                             │
│  1. EDIT SPEC                               │
│     └─ Sửa main.md hoặc README.md          │
│        │                                    │
│  2. COMPILE                                 │
│     └─ Invoke /compile.prompt.md            │
│     └─ Copilot reads spec → generates code  │
│        │                                    │
│  3. BUILD & TEST                            │
│     └─ go build / go test / run app         │
│     └─ Verify behavior matches spec         │
│        │                                    │
│  4. FIX (if needed)                         │
│     └─ Update spec (NOT code directly)      │
│     └─ Re-compile                           │
│        │                                    │
│  5. LINT (periodically)                     │
│     └─ Invoke /lint.prompt.md               │
│     └─ Clean up spec: remove duplicates,    │
│        minimize synonyms                    │
│        │                                    │
│  → REPEAT                                   │
│                                             │
└─────────────────────────────────────────────┘
```

### 3.2 Pro Tips

| Tip | Mô tả |
|-----|--------|
| **Focus hint** | Append "focus on \<the-change\>" khi spec lớn |
| **Use Copilot to edit spec** | Copilot có thể edit Markdown spec giống edit code |
| **Spec = single source of truth** | KHÔNG edit code trực tiếp — luôn edit spec |
| **Documentation stays in sync** | README.md được embed trong spec → auto-sync |
| **Language-portable** | Discard code, recompile sang ngôn ngữ khác |

### 3.3 Spec Kit — Open-Source Toolkit
- **GitHub:** [github.com/spec-kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- Provides structured process cho spec-driven development
- Works with: GitHub Copilot, Claude Code, Gemini CLI
- Open source, actively maintained

---

## 4. Áp dụng cho EMADS-PR

### 4.1 Mỗi agent có spec riêng

```
EMADS-PR-Specs/
├── agents/
│   ├── orchestrator.spec.md    # Orchestrator behavior spec
│   ├── cto-agent.spec.md       # CTO analysis patterns
│   ├── coo-agent.spec.md       # COO operations patterns
│   ├── legal-agent.spec.md     # Legal compliance rules
│   ├── risk-agent.spec.md      # Risk scoring rules
│   └── cost-agent.spec.md      # Budget management rules
├── reconcile/
│   └── reconcile-gpt.spec.md   # Trade-off analysis spec
├── workflows/
│   └── emads-pr-flow.spec.md   # Full flow specification
└── prompts/
    ├── compile-agent.prompt.md  # Compile agent from spec
    └── compile-flow.prompt.md   # Compile workflow from spec
```

### 4.2 Ví dụ: CTO Agent Spec

```markdown
# CTO Agent Specification

## Role
Technical architecture evaluator for EMADS-PR system.

## Input
- `task`: Business question from CEO via Orchestrator
- `context`: Previous decisions, current constraints

## Behavior
1. Analyze technical feasibility of proposed task
2. Evaluate architecture options with trade-offs
3. Score risk 0-4 for technical complexity
4. Return structured JSON output

## Output Schema
```json
{
  "tech_options": [{"name": "", "pros": [], "cons": [], "effort": ""}],
  "risks": [{"type": "", "severity": 0, "mitigation": ""}],
  "recommendation": "",
  "confidence": 0.0,
  "risk_score": 0
}
```

## Constraints
- MUST complete within 30 seconds
- MUST NOT exceed 2000 tokens
- MUST cite sources for technology claims
```

---

## 5. GitHub Copilot CLI — Agentic Workflows trong Terminal

### 5.1 Tổng quan
- **Copilot CLI** = AI coding agent chạy trực tiếp trong terminal
- Không cần IDE — hoạt động qua command line
- Ships with **GitHub MCP server** built-in
- Supports **headless mode** cho automation/scripting
- Available: Windows (WSL + PowerShell), macOS, Linux

### 5.2 Key Commands

```bash
# Clone repo + setup dependencies automatically
copilot "Clone the feedback repo and set us up to run it"

# Debug port conflicts
copilot "Find and kill the process on port 3000"

# Fix bugs from screenshots (image analysis)
copilot "Fix the bug shown in @FIX-THIS.PNG"

# Use custom agents
copilot "/agent"           # List available agents
copilot "Review our changes"  # Agent-specific tasks

# Search GitHub issues via MCP
copilot "Are there any open issues that map to our work?"

# Delegate to coding agent (background PR)
copilot "/delegate Finish fixing #1 and use playwright MCP to verify"
```

### 5.3 Headless Mode — Scripting & Automation

```bash
# Run Copilot without interactive prompts
copilot --allow-all-tools -p "Kill the process using port 3000"

# Safer: restrict tools and directories
copilot --allow-tools "shell,fs" --restrict-dir "/app" \
  -p "Run tests and report failures"

# Use in CI/CD pipeline
copilot --allow-tools "github" \
  -p "Create PR with summary of changes in staging branch"
```

### 5.4 Authentication

```bash
# Interactive login
copilot login

# Token-based (for automation)
export GITHUB_TOKEN="ghp_xxxx"
copilot -p "List open PRs in my repos"
```

### 5.5 Key Capabilities

| Capability | Mô tả |
|-----------|--------|
| **MCP Server** | Built-in GitHub MCP → search issues, PRs, repos |
| **Image Analysis** | Upload screenshots → analyze bugs |
| **Custom Agents** | `/agent` → select domain-specific agents |
| **/delegate** | Dispatch coding agent for background work |
| **Headless** | `-p` flag for scripting/automation |
| **Tool Restrictions** | `--allow-tools`, `--restrict-dir` for safety |

---

## 6. Kết hợp Spec-Driven + Copilot CLI

### 6.1 Workflow tích hợp

```bash
# 1. Edit spec
code main.md

# 2. Compile via CLI (headless)
copilot --allow-all-tools -p "/compile"

# 3. Build & test
go build && go test ./...

# 4. Create PR via CLI
copilot -p "Create a PR with changes, reference spec updates"

# 5. Delegate review
copilot "/delegate Review and improve test coverage for latest changes"
```

### 6.2 Ưu điểm cho EMADS-PR

| Benefit | Impact |
|---------|--------|
| **Spec = Single source of truth** | Agents luôn consistent |
| **CLI = Automation gateway** | Headless execution cho CI/CD |
| **MCP integration** | Connect to any external tool |
| **Delegate** | Background coding agents |
| **Language-portable** | Compile spec sang Python/Go/TypeScript |

---

## 7. Key Takeaways cho Agent

```
✅ main.md là "source code" — KHÔNG edit generated code trực tiếp
✅ compile.prompt.md để reproducible compilation
✅ lint.prompt.md để giữ spec clean
✅ Spec Kit là open-source toolkit cho workflow này
✅ Copilot CLI mở rộng agent capabilities vào terminal
✅ Headless mode cho CI/CD automation
✅ /delegate = coding agent chạy background
✅ MCP server built-in = GitHub integration sẵn
✅ Áp dụng cho EMADS-PR: mỗi agent có spec riêng
```

---

## 📚 Sources

- GitHub Blog: [Spec-driven development](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-using-markdown-as-a-programming-language-when-building-with-ai/)
- GitHub Blog: [Copilot CLI](https://github.blog/ai-and-ml/github-copilot/power-agentic-workflows-in-your-terminal-with-github-copilot-cli/)
- GitHub: [Spec Kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- GitHub: [Copilot CLI Repo](https://github.com/github/copilot-cli)
- GitHub: [GitHub Brain MCP Server](https://github.com/wham/github-brain)
