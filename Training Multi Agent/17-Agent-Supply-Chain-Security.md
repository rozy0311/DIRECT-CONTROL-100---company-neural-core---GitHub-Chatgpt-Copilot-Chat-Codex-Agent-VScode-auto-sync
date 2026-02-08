# 17 — Agent Supply Chain Security & AI Code Security

> **Mục đích training:** Hiểu các mối đe dọa supply chain cho AI agents (MCP scanning, npm security, SLSA, artifact attestations) và bảo mật code AI-generated (CodeGuard, CodeQL, Dependabot).

---

## 1. AI Agent Supply Chain — Attack Surface mới

### 1.1 Tại sao Supply Chain Security quan trọng cho Agents?

```
TRADITIONAL APP:
├─ Source code → Build → Deploy
├─ Attack vectors: dependencies, CI/CD, registry
└─ Tools: npm audit, Dependabot, SLSA

AI AGENT APP — THÊM ATTACK SURFACE:
├─ MCP Servers (external tools) — ĐẶC BIỆT NGUY HIỂM
├─ LLM Provider APIs
├─ Vector databases / RAG sources
├─ Fine-tuned model weights
├─ Prompt templates / System prompts
├─ Agent-to-Agent communication
└─ Tool schemas / function definitions

→ SUPPLY CHAIN cho AI Agents RỘng hơn nhiều so với traditional apps
```

### 1.2 MCP Supply Chain Threats

```
┌─────────────────────────────────────────────────┐
│        MCP SERVER THREAT TAXONOMY                │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. MALICIOUS MCP SERVERS                       │
│     ├─ Tool Poisoning — fake tools inject code  │
│     ├─ Data Exfiltration — steal agent context  │
│     └─ Prompt Injection via tool responses      │
│                                                 │
│  2. COMPROMISED MCP SERVERS                     │
│     ├─ Supply chain attack on MCP dependencies  │
│     ├─ Typosquatting MCP server names           │
│     └─ Backdoored MCP server updates            │
│                                                 │
│  3. MISCONFIGURED MCP SERVERS                   │
│     ├─ Overly permissive tool access            │
│     ├─ No input validation on tool args         │
│     └─ Sensitive data in tool responses         │
│                                                 │
│  4. MAN-IN-THE-MIDDLE                           │
│     ├─ Intercepted MCP communications           │
│     ├─ Modified tool responses in transit       │
│     └─ Session hijacking                        │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 2. Cisco MCP Scanner — Open Source Security Tool

### 2.1 Overview
- **Tên:** Cisco MCP Scanner
- **Mục đích:** Scan MCP servers cho security vulnerabilities
- **License:** Open Source
- **Nguồn:** Cisco AI Security Team
- **Blog:** [Securing the AI Agent Supply Chain](https://blogs.cisco.com/ai/securing-the-ai-agent-supply-chain-with-ciscos-open-source-mcp-scanner)

### 2.2 Scan Categories

```
MCP SCANNER CHECKS:
├─ 1. SERVER IDENTITY
│     ├─ Verify server authenticity
│     ├─ Check for typosquatting
│     └─ Validate certificates
│
├─ 2. TOOL SECURITY
│     ├─ Analyze tool schemas for injection risks
│     ├─ Check for overprivileged tools
│     └─ Detect suspicious tool patterns
│
├─ 3. DATA FLOW
│     ├─ Identify data exfiltration risks
│     ├─ Check for sensitive data exposure
│     └─ Validate input/output sanitization
│
├─ 4. DEPENDENCY AUDIT
│     ├─ Scan MCP server dependencies
│     ├─ Check for known CVEs
│     └─ Verify package integrity
│
└─ 5. CONFIGURATION
      ├─ Check for secure defaults
      ├─ Validate access controls
      └─ Review logging/monitoring setup
```

### 2.3 Tích hợp vào EMADS-PR

```python
# Before adding any MCP server to agent system
def approve_mcp_server(server_config):
    # 1. Run Cisco MCP Scanner
    scan_result = mcp_scanner.scan(server_config)
    
    if scan_result.critical_issues > 0:
        return REJECT(f"Critical: {scan_result.critical_issues} issues found")
    
    if scan_result.high_issues > 0:
        return ESCALATE(f"High severity: requires Security Agent review")
    
    # 2. Add to allowlist with restrictions
    allowlist.add(server_config, {
        "allowed_tools": scan_result.safe_tools,
        "blocked_tools": scan_result.risky_tools,
        "max_calls_per_minute": 60,
        "data_classification": "internal_only"
    })
    
    return APPROVE("MCP server added with restrictions")
```

---

## 3. Cisco Project CodeGuard — Bảo mật Code AI-Generated

### 3.1 Concept
- **Project CodeGuard** = framework bảo mật cho code được AI viết
- Focus: AI-generated code thường có vulnerabilities mà developer không review kỹ
- Nguồn: [Cisco Blog](https://blogs.cisco.com/ai/project-codeguard-securing-the-ai-written-software-frontier)

### 3.2 Vấn đề với AI-Generated Code

```
AI CODE RISKS:
├─ HALLUCINATED APIS
│   └─ AI gọi functions không tồn tại → runtime errors
│
├─ INSECURE DEFAULTS
│   └─ AI thường generate code không có input validation
│   └─ Default configs insecure (open ports, weak auth)
│
├─ DEPENDENCY CONFUSION
│   └─ AI suggest packages có tên tương tự package thật
│   └─ Typosquatting risk tăng cao
│
├─ KNOWN VULNERABLE PATTERNS
│   └─ AI trained trên code cũ có vulnerabilities
│   └─ SQL injection, XSS, path traversal
│
└─ LICENSE COMPLIANCE
    └─ AI mix code từ different licenses
    └─ GPL + MIT confusion
```

### 3.3 CodeGuard Approach

| Layer | Action | Tool |
|-------|--------|------|
| **Pre-generation** | Secure prompts + constraints | Prompt Engineering |
| **Post-generation** | Static analysis + vulnerability scan | CodeQL, Semgrep |
| **Pre-merge** | Human + AI review | GitHub PR review |
| **Runtime** | Monitor for anomalous behavior | SIEM, runtime protection |

---

## 4. GitHub Security Tools cho Agent Development

### 4.1 CodeQL — Vulnerability Research

```yaml
# .github/workflows/codeql-analysis.yml
name: "CodeQL"
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 8 * * 1'  # Weekly scan

jobs:
  analyze:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        language: ['python', 'javascript']
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: security-extended,security-and-quality
      - uses: github/codeql-action/autobuild@v3
      - uses: github/codeql-action/analyze@v3
```

### 4.2 Dependabot — Dependency Security

```yaml
# .github/dependabot.yml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    reviewers:
      - "rozy0311"
    labels:
      - "dependencies"
      - "security"
    
  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 4.3 SLSA Level 3 — Supply Chain Integrity

```
SLSA (Supply chain Levels for Software Artifacts):
├─ Level 1: Documentation of build process
├─ Level 2: Tamper resistance of build service
├─ Level 3: Extra resistance to specific threats ← TARGET
└─ Level 4: Highest level of confidence

SLSA Level 3 yêu cầu:
├─ Build as code (definable, automatable)
├─ Isolated builds (hermetic)
├─ Provenance (signed, non-falsifiable)
└─ Artifact attestations (verifiable chain)
```

### 4.4 Artifact Attestations

```yaml
# Generate attestation for build artifacts
- uses: actions/attest-build-provenance@v2
  with:
    subject-path: 'dist/*.whl'
    
# Verify attestation before deployment
- run: |
    gh attestation verify dist/mypackage-1.0.whl \
      --owner rozy0311 \
      --repo shopify-blog-automation
```

### 4.5 npm Security Insights API

```
NPM SECURITY FEATURES:
├─ Security Insights API — query vulnerability data
├─ Package provenance — verify publisher identity
├─ npm audit signatures — verify package integrity
├─ Socket integration — detect supply chain attacks
└─ Dependency review action — block vulnerable deps in PRs
```

---

## 5. Security Checklist cho AI Agent Projects

### 5.1 Pre-Development

```
□ Enable Dependabot alerts + auto-fix PRs
□ Enable CodeQL analysis (schedule + PR triggers)
□ Enable secret scanning + push protection
□ Set up branch protection rules (require reviews)
□ Configure artifact attestations for releases
□ Pin all GitHub Actions to commit SHAs (not tags)
```

### 5.2 MCP Server Security

```
□ Scan all MCP servers with Cisco MCP Scanner
□ Allowlist approved MCP servers only
□ Restrict tool permissions per agent role
□ Validate all tool inputs/outputs
□ Monitor MCP server for anomalous behavior
□ Rate-limit MCP tool calls
□ Encrypt MCP communications (TLS/mTLS)
□ Audit MCP server dependencies weekly
```

### 5.3 AI-Generated Code Security

```
□ Run CodeQL on all AI-generated code
□ Require human review for security-sensitive files
□ Validate dependencies against known-good list
□ Check for hallucinated API calls
□ Verify license compliance
□ Test for common vulnerability patterns
□ Monitor runtime behavior post-deployment
```

### 5.4 Supply Chain Integrity

```
□ SLSA Level 3 compliance for all builds
□ Artifact attestations for all releases
□ Signed commits (GPG or SSH)
□ Dependency pinning (lock files)
□ Provenance verification in CI/CD
□ Regular dependency audits
```

---

## 6. EMADS-PR Security Integration

### 6.1 Security Agent Enhancement

```python
class SecurityAgent:
    """Enhanced with supply chain security checks"""
    
    def analyze(self, task, code_changes):
        results = {
            # Existing checks
            "prompt_injection": self.check_prompt_injection(task),
            "data_exposure": self.check_data_exposure(code_changes),
            
            # NEW: Supply chain checks
            "dependency_vulns": self.scan_dependencies(code_changes),
            "mcp_server_safety": self.scan_mcp_servers(code_changes),
            "ai_code_quality": self.scan_ai_generated_code(code_changes),
            "slsa_compliance": self.check_slsa_level(code_changes),
            "license_compliance": self.check_licenses(code_changes),
        }
        
        risk_score = self.calculate_risk(results)
        return {
            "results": results,
            "risk_score": risk_score,  # 0-4
            "recommendations": self.generate_recommendations(results)
        }
```

---

## 7. Key Takeaways cho Agent

```
✅ AI Agent supply chain = RỘNG hơn traditional app supply chain
✅ MCP servers = attack vector #1 — luôn scan trước khi dùng
✅ Cisco MCP Scanner = open-source tool scan MCP vulnerabilities
✅ CodeGuard = framework bảo mật AI-generated code
✅ CodeQL + Dependabot + SLSA = GitHub security stack
✅ Artifact attestations = verify supply chain integrity
✅ Pin GitHub Actions to commit SHAs (KHÔNG dùng tags)
✅ AI-generated code cần extra scrutiny: hallucinated APIs, insecure defaults
✅ Security Agent trong EMADS-PR nên include supply chain checks
```

---

## 📚 Sources

- Cisco Blog: [Securing AI Agent Supply Chain — MCP Scanner](https://blogs.cisco.com/ai/securing-the-ai-agent-supply-chain-with-ciscos-open-source-mcp-scanner)
- Cisco Blog: [Project CodeGuard](https://blogs.cisco.com/ai/project-codeguard-securing-the-ai-written-software-frontier)
- GitHub Blog: [State of Open Source Supply Chain Security 2025](https://github.blog/security/supply-chain-security/the-state-of-open-source-supply-chain-security-2025/)
- GitHub Blog: [npm Security Insights API](https://github.blog/security/supply-chain-security/introducing-npm-security-insights-api/)
- GitHub Blog: [JFrog Integration](https://github.blog/security/supply-chain-security/the-jfrog-github-integration-enables-developer-centric-security-with-code-to-runtime-visibility/)
- GitHub: [CodeQL Documentation](https://codeql.github.com/docs/)
- GitHub: [SLSA + Artifact Attestations](https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations)
