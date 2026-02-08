# 02 — Agent Automation Patterns: Headless Execution, PR-Only Workflow & Guardrails

> **Mục đích training:** Hiểu cách agents tự động thực thi không cần UI, quy trình PR-only cho code changes, hệ thống guardrails/sandboxing bảo vệ hệ thống.

---

## 1. Headless Agent Execution

### 1.1 Khái niệm
- **Headless = Không cần giao diện người dùng (UI)**
- Agent chạy hoàn toàn tự động qua CLI/API/background process
- Trigger bởi: cron jobs, webhooks, GitHub Actions, event-driven

### 1.2 Kiến trúc Headless Agent
```
Trigger (Cron/Webhook/Event)
    ↓
Agent Runner (Background Process)
    ↓
Task Queue (Redis/RabbitMQ)
    ↓
Agent Execution (LLM + Tools)
    ↓
Output (PR/Report/Notification)
```

### 1.3 Ưu điểm
- **Scalable:** Chạy nhiều agent song song
- **Consistent:** Không phụ thuộc human interaction
- **Auditable:** Log mọi action, dễ trace
- **Cost-effective:** Không cần UI server

### 1.4 Best Practices
- Luôn có **timeout** cho mỗi task
- Implement **retry logic** với exponential backoff
- **Dead letter queue** cho failed tasks
- **Health check** endpoint cho monitoring

---

## 2. PR-Only Workflow

### 2.1 Nguyên tắc cốt lõi
> **Mọi thay đổi code PHẢI thông qua Pull Request — không bao giờ commit trực tiếp vào main/protected branches**

### 2.2 Luồng PR-Only
```
Agent phát hiện task cần thay đổi code
    ↓
Tạo branch mới (feature/fix-xxx)
    ↓
Thực hiện changes trên branch
    ↓
Tạo Pull Request với description chi tiết
    ↓
Automated checks (lint, test, security scan)
    ↓
Human review (approve/request changes)
    ↓
Merge vào main (sau khi approved)
```

### 2.3 Branch Protection Rules
```yaml
# .github/branch-protection.yml
protection_rules:
  main:
    required_reviews: 1
    required_status_checks:
      - lint
      - test
      - security-scan
    dismiss_stale_reviews: true
    require_code_owner_reviews: true
    restrict_pushes: true
```

### 2.4 Agent PR Creation Pattern
```python
# create_pr.py - Pattern cho agent tạo PR
def create_agent_pr(changes, task_description):
    branch_name = f"agent/{task_type}/{timestamp}"
    
    # 1. Create branch
    create_branch(branch_name, base="main")
    
    # 2. Apply changes
    for file_path, content in changes.items():
        commit_file(branch_name, file_path, content)
    
    # 3. Create PR with structured description
    pr = create_pull_request(
        title=f"[Agent] {task_description}",
        body=generate_pr_body(changes, task_description),
        base="main",
        head=branch_name,
        labels=["agent-generated", "auto-review"]
    )
    
    return pr
```

---

## 3. Allowlist & Permission System

### 3.1 File-Level Sandboxing
```python
# check_allowed_changes.py
ALLOWED_PATHS = [
    "content/**",           # Blog content
    "data/**",              # Data files
    "config/auto/**",       # Auto-generated config
]

FORBIDDEN_PATHS = [
    ".github/workflows/**", # CI/CD pipelines
    "scripts/deploy/**",    # Deployment scripts
    "*.env",                # Environment variables
    "secrets/**",           # Secrets
]

def check_allowed(file_path):
    """Agent chỉ được sửa files trong allowlist"""
    for pattern in FORBIDDEN_PATHS:
        if fnmatch(file_path, pattern):
            raise PermissionError(f"FORBIDDEN: {file_path}")
    
    for pattern in ALLOWED_PATHS:
        if fnmatch(file_path, pattern):
            return True
    
    raise PermissionError(f"NOT IN ALLOWLIST: {file_path}")
```

### 3.2 Action-Level Permissions
```yaml
# agents.yaml
agents:
  content_writer:
    allowed_actions:
      - read_file
      - write_file
      - create_pr
    forbidden_actions:
      - delete_repo
      - modify_workflow
      - access_secrets
    
  code_reviewer:
    allowed_actions:
      - read_file
      - comment_pr
      - approve_pr
    forbidden_actions:
      - write_file
      - merge_pr
```

---

## 4. Risk Scoring System

### 4.1 Risk Score Calculation
```python
def calculate_risk_score(changes):
    """Score 0-12: Higher = More risky"""
    score = 0
    
    # File sensitivity
    for file in changes:
        if file.endswith('.yml') or file.endswith('.yaml'):
            score += 2  # Config files
        if 'workflow' in file:
            score += 4  # CI/CD
        if 'secret' in file or '.env' in file:
            score += 6  # Secrets
        if file.endswith('.py') or file.endswith('.js'):
            score += 1  # Source code
    
    # Change magnitude
    total_lines = sum(c.lines_changed for c in changes)
    if total_lines > 500:
        score += 3
    elif total_lines > 100:
        score += 2
    elif total_lines > 20:
        score += 1
    
    return min(score, 12)

# Risk levels
# 0-3:  LOW    → Auto-approve possible
# 4-7:  MEDIUM → Requires 1 reviewer
# 8-12: HIGH   → Requires 2+ reviewers + senior approval
```

---

## 5. GitHub Actions cho Agent Automation

### 5.1 Autonomous Agent Workflow
```yaml
# .github/workflows/autonomous-agent.yml
name: Autonomous Agent

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:
    inputs:
      task:
        description: 'Task for agent'
        required: true

jobs:
  agent-run:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Agent
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python scripts/agent_runner.py \
            --task "${{ inputs.task || 'scheduled-check' }}" \
            --mode headless \
            --pr-only true
      
      - name: Validate Changes
        run: |
          python scripts/check_allowed_changes.py
      
      - name: Create PR if changes
        if: steps.agent-run.outputs.has_changes == 'true'
        run: |
          python scripts/create_pr.py \
            --risk-score ${{ steps.agent-run.outputs.risk_score }}
```

---

## 6. Guardrails Checklist

### 6.1 Pre-Execution Guardrails
- [ ] Task trong allowed scope?
- [ ] Budget (tokens/API calls) đủ?
- [ ] Không conflict với running tasks?
- [ ] Input đã sanitized?

### 6.2 During-Execution Guardrails
- [ ] File changes trong allowlist?
- [ ] Không access forbidden resources?
- [ ] Token usage trong budget?
- [ ] Timeout chưa vượt?

### 6.3 Post-Execution Guardrails
- [ ] Risk score đã tính?
- [ ] PR description đầy đủ?
- [ ] Automated tests pass?
- [ ] Security scan clean?

---

## 7. Key Takeaways cho Training

1. **Headless execution** = agent chạy background, trigger bởi events/cron
2. **PR-only workflow** = mọi thay đổi phải qua PR, không commit trực tiếp
3. **File-level sandboxing** = allowlist/blocklist kiểm soát agent sửa gì
4. **Risk scoring** = tự động đánh giá mức độ rủi ro của changes (0-12)
5. **GitHub Actions** = nền tảng cho autonomous agent execution
6. **Guardrails** = 3 lớp bảo vệ: pre/during/post execution

---

## Nguồn tham khảo
- Agent Automation Architecture (Internal Documentation)
- GitHub Actions for Autonomous Agents
- PR-Only Workflow Best Practices
