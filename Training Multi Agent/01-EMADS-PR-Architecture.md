# 01 — EMADS-PR v1.0: Enterprise Multi-Agent Decision System — Production Ready

> **Mục đích training:** Hiểu kiến trúc tổng thể Multi-Agent Enterprise AI, vai trò từng agent, luồng phối hợp, và cách ReconcileGPT hoạt động như decision engine trung lập.

---

## 1. Tổng quan kiến trúc

**Tên chính thức:** EMADS-PR v1.0 — Enterprise Multi-Agent Decision System — Production Ready  
**Tên pitch:** Agentic C-Suite: Hierarchical Decision Engine  
**Tên internal:** Orchestrator-CTO-COO-ReconcileGPT Framework

### Sơ đồ ASCII Production-Ready

```
+-------------------+  
|  CEO/User Input   |  Business Goal / Question
+-------------------+  
         |  
         v  
+-------------------+  ← Memory Agent (State/History Retrieval)
| Orchestrator/     |  Route + Coordinate + State Mgmt
| Supervisor Agent  |  
+-------------------+  
         | (parallel dispatch)  
   +-----+-----+-----+-------+-------+  
   |     |     |     |       |       |  
+-----+ +-----+ +---+ +-----+ +------+  
|CTO  | |COO  | |Legal| |Risk | |Cost  |  Specialists (.md/JSON outputs)
|Agent| |Agent| |Agent| |Agent| |Agent |  
+-----+ +-----+ +---+ +-----+ +------+  
         |  
         v (merge all outputs)  
+-----------------------+  
| ReconcileGPT          |  Analyze + Holistic Decision
| (Decision Engine)     |  
+-----------------------+  
         |  
         v  
+-----------------------+  
| Human Review Loop     |  Approve / Edit / Reject
| (Governance Gate)     |  
+-----------------------+  
         | (approved)  
         v  
   +-----+ +-----+  
   |CTO  | |COO  |  Parallel Executors
   |Exec | |Exec |  
   +-----+ +-----+  
         |  
         v  
+-----------------------+  
| Monitor / Validator   |  KPI Tracking + Alerts
+-----------------------+  
         |  
   +-----+-----+  
   |           |  
Complete   Re-plan ↑ (feedback loop via Orchestrator)
         |  
         v  
+-------------------------------------------------+
| Infra Layer: Autoscaling | Security | Eval Suite |
+-------------------------------------------------+
```

---

## 2. Vai trò từng Agent

### 2.1 CEO/User Input
- Đưa vấn đề / mục tiêu / constraint ban đầu
- Ví dụ: doanh thu, chi phí, deadline, mức rủi ro chấp nhận được

### 2.2 Orchestrator / Supervisor Agent
- **Route + Coordinate + State Management**
- Nhận input từ CEO → dispatch parallel tới các Specialist Agents
- Tích hợp Memory Agent để lấy lịch sử quyết định, context trước đó
- Quản lý state machine của toàn bộ workflow

### 2.3 Specialist Agents (5 agents chạy parallel)

| Agent | Vai trò | Output |
|-------|---------|--------|
| **CTO Agent** | Chiến lược công nghệ, kiến trúc hệ thống, phương án kỹ thuật + rủi ro/chi phí | Tech options A/B/C + risk + effort + timeline |
| **COO Agent** | Vận hành, quy trình, tài nguyên, SLA, chi phí OPEX | Ops impact + resource allocation + feasibility |
| **Legal Agent** | Compliance flags, regulatory requirements | Compliance report + flags |
| **Risk Agent** | Quantify threats, rủi ro tổng thể | Risk score + mitigation strategies |
| **Cost Agent** | Track token/API/GPU costs, enforce budgets, ROI projection | Cost score + budget flags + ROI |

### 2.4 ReconcileGPT (Decision Engine)
- **Vai trò:** Decision engine **trung lập**, KHÔNG phải "ông chủ ra lệnh"
- **Chức năng:**
  - Chuẩn hóa dữ liệu input (cost, benefit, risk, timeline, alignment với OKR)
  - Phân tích kịch bản, trade-off, scoring từng option
  - Đề xuất 1–2 phương án ưu tiên, kèm điều kiện & cảnh báo
  - Phát hiện xung đột giữa CTO và COO → reconcile

### 2.5 Human Review Loop (Governance Gate)
- Mọi đề xuất từ ReconcileGPT **bắt buộc** phải qua human-in-the-loop
- COO + CTO review → chỉnh lại giả định sai → chốt
- Tuỳ governance: CEO hoặc hội đồng quyết định cuối

### 2.6 Monitor / Validator
- KPI Tracking + Alerts
- Nếu Complete → kết thúc
- Nếu cần Re-plan → feedback loop quay về Orchestrator

### 2.7 Memory Agent
- Retrieve historical decisions, user preferences, lessons learned
- RAG cho Orchestrator/ReconcileGPT
- Vector DB query → Context enrichment

### 2.8 Infra Layer
- Autoscaling (K8s)
- Security (RBAC/Vault)
- Eval (accuracy/hallucination testing)
- System metrics → Alerts/scaling actions

---

## 3. Luồng làm việc chi tiết

### 3.1 Luồng chính (Happy Path)
```
CEO Input → Orchestrator → [CTO + COO + Legal + Risk + Cost] (parallel)
→ ReconcileGPT (merge + analyze + recommend)
→ Human Review (approve/edit/reject)
→ [CTO Exec + COO Exec] (parallel execution)
→ Monitor/Validator
→ Complete OR Re-plan (loop back to Orchestrator)
```

### 3.2 Khi quyết định thiên tech
- CTO "Accountable", COO "Consulted", ReconcileGPT "tool"
- Ví dụ: chọn kiến trúc, tech stack mới

### 3.3 Khi quyết định thiên vận hành
- COO "Accountable", CTO "Consulted", ReconcileGPT "tool"
- Ví dụ: phân bổ nguồn lực, tối ưu quy trình

### 3.4 Khi quyết định cross-functional lớn
- CEO "Accountable", COO/CTO "Responsible/Consulted", ReconcileGPT "tool hỗ trợ"
- Ví dụ: sản phẩm mới, pivot business model

---

## 4. RACI Matrix

| Quyết định | Responsible | Accountable | Consulted | Informed |
|-----------|-------------|-------------|-----------|----------|
| Phân bổ nguồn lực (nhân sự/budget) | Operations team | COO | Finance/HR | CEO/CTO |
| Tối ưu mô hình kinh doanh | COO | COO | ReconcileGPT (tool) | CEO |
| Scale operations (non-tech) | COO | COO | ReconcileGPT | CTO (nếu liên quan) |
| Kiến trúc, stack mới | CTO | CTO | COO | CEO |
| Sản phẩm mới, pivot | CTO + COO | CEO | ReconcileGPT | All |

---

## 5. Tại sao tách riêng ReconcileGPT?

### Ưu điểm Modular
- **Chuyên biệt hóa:** Mỗi agent focus riêng → giảm hallucination, tăng accuracy
- **Dễ bảo trì & scale:** Update độc lập, fault isolation
- **Hierarchical coordination:** ReconcileGPT làm supervisor nhận input → output recommendation → loop back review

### Nhược điểm Monolithic (gộp hết)
- Khó maintain khi hệ thống lớn
- Latency cao (reasoning phức tạp trong 1 model)
- Ít linh hoạt, khó A/B test

### Khi nào gộp?
- Chỉ khi prototype rất nhỏ, low-complexity decisions
- Ưu tiên speed/low-latency → monolithic nhanh deploy hơn

---

## 6. Format chuẩn hóa Input cho ReconcileGPT

```json
{
  "agent": "CTO|COO|Legal|Risk|Cost",
  "objective": "Mô tả mục tiêu",
  "constraints": ["budget", "deadline", "tech_stack"],
  "risks": [{"risk": "description", "probability": 0.3, "impact": "high"}],
  "cost_estimate": {"one_time": 50000, "monthly": 5000},
  "benefits": ["description"],
  "assumptions": ["assumption_1", "assumption_2"],
  "alignment_okr": "OKR liên quan"
}
```

---

## 7. Key Takeaways cho Training

1. **Multi-agent PHẢI modular** — mỗi agent 1 vai trò rõ ràng
2. **ReconcileGPT là TOOL hỗ trợ** — không thay quyền sở hữu quyết định
3. **Human-in-the-loop BẮT BUỘC** — mọi quyết định phải validate
4. **Parallel processing** — specialist agents chạy đồng thời, tăng throughput
5. **Feedback loop** — Monitor → Re-plan nếu cần, liên tục cải thiện
6. **Memory Agent** — context enrichment qua RAG, tránh mất kiến thức
7. **Infra Layer** — autoscaling, security, eval là nền tảng production

---

## Nguồn tham khảo
- Perplexity Research: Multi-Agent Enterprise AI Architecture
- LangGraph Documentation
- Azure AI Agent Design Patterns
- RACI Framework for AI Governance
