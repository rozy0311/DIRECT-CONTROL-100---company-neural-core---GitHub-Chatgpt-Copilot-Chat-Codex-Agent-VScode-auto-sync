# 06 — LLM-in-Sandbox: General Agentic Intelligence từ Code Sandbox

> **Mục đích training:** Hiểu research paper LLM-in-Sandbox — cách đặt LLM vào virtual computer để unlock general intelligence cho non-code tasks, và ứng dụng cho multi-agent system.

---

## 1. Tổng quan Paper

- **Tên:** LLM-in-Sandbox Elicits General Agentic Intelligence
- **Tác giả:** Microsoft Research (Daixuan Cheng et al.)
- **Published:** January 2026 — #1 Paper of the day trên HuggingFace
- **Link:** https://arxiv.org/abs/2601.16206
- **Code:** https://github.com/llm-in-sandbox/llm-in-sandbox
- **Install:** `pip install llm-in-sandbox`

---

## 2. Ý tưởng cốt lõi

### 2.1 Concept
> **Đặt LLM vào code sandbox (virtual computer) → LLM tự khám phá và sử dụng sandbox để giải quyết mọi loại bài toán, kể cả non-code tasks**

### 2.2 Tại sao đặc biệt?
```
TRƯỚC LLM-in-Sandbox:
├─ LLM chỉ "trả lời" text-based
├─ Cần tools cụ thể cho từng task
├─ Giới hạn bởi context window
└─ Không tự tìm kiếm thêm knowledge

SAU LLM-in-Sandbox:
├─ LLM tự viết code để giải quyết vấn đề
├─ Tự truy cập internet lấy thêm knowledge
├─ Dùng file system xử lý long contexts
├─ Tự install packages cần thiết
└─ KHÔNG CẦN training thêm (training-free)
```

---

## 3. Capabilities phát hiện được

### 3.1 Spontaneous Behaviors (tự phát)
LLM trong sandbox **tự động** làm những điều sau mà KHÔNG được chỉ dẫn:

| Behavior | Mô tả | Ví dụ |
|----------|--------|-------|
| **External Resource Access** | Tự tìm kiếm thông tin mới | `pip install wikipedia-api && python fetch_wiki.py` |
| **File System Leverage** | Dùng files để xử lý long context | Chia document dài thành chunks, lưu vào files, xử lý từng phần |
| **Script Execution** | Viết và chạy scripts phức tạp | Tạo Python script để format output theo yêu cầu |
| **Package Installation** | Tự install tools cần thiết | `pip install rdkit` cho chemistry tasks |

### 3.2 Benchmark Results

| Domain | Improvement | Task Types |
|--------|------------|-----------|
| **Mathematics** | +15-30% accuracy | Proof verification, computation |
| **Physics** | +10-20% accuracy | Simulation, formula validation |
| **Chemistry** | +25-40% accuracy | Molecule analysis (dùng RDKit) |
| **Biomedicine** | +10-15% accuracy | Drug interaction, pathway analysis |
| **Long-Context QA** | +20-35% accuracy | Document analysis beyond context window |
| **Instruction Following** | +15-25% accuracy | Complex format requirements |

---

## 4. LLM-in-Sandbox Reinforcement Learning (RL)

### 4.1 Concept
- Training LLM để **tốt hơn** trong việc sử dụng sandbox
- Dùng **non-agentic data** → train cho agentic behavior
- Không cần curated agent trajectories

### 4.2 Training Flow
```
Standard QA Dataset (non-agentic)
    ↓
LLM attempts to solve in sandbox
    ↓
Reward = correctness of final answer
    ↓
RL training updates LLM
    ↓
LLM learns WHEN and HOW to use sandbox tools
```

### 4.3 Key Insight
> Agent không cần "agent-specific training data". Chỉ cần RL reward cho đúng/sai → LLM tự học cách sử dụng tools.

---

## 5. Ứng dụng cho Multi-Agent System

### 5.1 Mỗi agent có sandbox riêng
```python
# Concept: Each agent in EMADS-PR gets own sandbox
agent_sandboxes = {
    "CTO_Agent": Sandbox(
        allowed_packages=["numpy", "pandas", "requests"],
        network_access=True,
        file_system="isolated",
        resource_limits={"cpu": "2 cores", "ram": "4GB"}
    ),
    "COO_Agent": Sandbox(
        allowed_packages=["openpyxl", "matplotlib"],
        network_access=False,  # Security: no external access
        file_system="isolated",
        resource_limits={"cpu": "1 core", "ram": "2GB"}
    ),
    "ReconcileGPT": Sandbox(
        allowed_packages=["scipy", "scikit-learn"],
        network_access=False,
        file_system="shared_read",  # Read outputs from other agents
        resource_limits={"cpu": "4 cores", "ram": "8GB"}
    )
}
```

### 5.2 Use Cases cụ thể

**CTO Agent + Sandbox:**
- Tự chạy benchmark tests cho tech options
- Install và test libraries trước khi recommend
- Simulate performance under load

**COO Agent + Sandbox:**
- Chạy financial models (Excel-like calculations)
- Generate reports với matplotlib
- Process large datasets

**ReconcileGPT + Sandbox:**
- Run optimization algorithms
- Statistical analysis trên outputs từ CTO/COO
- Generate scoring visualizations

---

## 6. Efficiency Analysis

### 6.1 Computational Cost
- Sandbox overhead: ~2-5x so với direct LLM response
- Trade-off: accuracy tăng đáng kể, đặc biệt cho complex tasks
- Mitigation: chỉ dùng sandbox khi task complexity > threshold

### 6.2 System Requirements
- Container runtime (Docker/Podman)
- GPU cho LLM inference
- Isolated network namespace
- File system quotas

### 6.3 Decision Logic: Khi nào dùng Sandbox?
```python
def should_use_sandbox(task):
    """Decide if task needs sandbox execution"""
    if task.requires_computation:
        return True
    if task.requires_external_knowledge:
        return True
    if task.context_length > MAX_CONTEXT:
        return True  # Use file system for long context
    if task.requires_specific_tools:
        return True
    return False  # Simple Q&A → direct LLM response
```

---

## 7. Key Takeaways cho Training

1. **LLM-in-Sandbox** = đặt LLM vào virtual computer → unlock general agentic intelligence
2. **Training-free** — strong LLMs tự biết cách dùng sandbox mà không cần train thêm
3. **Spontaneous behaviors** — tự install packages, access internet, dùng file system
4. **RL enhancement** — dùng non-agentic data + reward signal → train cho agentic behavior
5. **Multi-domain gains** — math, physics, chemistry, biomedicine, long-context QA
6. **Application cho EMADS-PR** — mỗi agent có sandbox riêng, isolated nhưng có thể share outputs
7. **Cost/Benefit** — 2-5x overhead nhưng accuracy tăng 15-40% cho complex tasks

---

## Nguồn tham khảo
- Paper: "LLM-in-Sandbox Elicits General Agentic Intelligence" (arXiv:2601.16206)
- Microsoft Research
- HuggingFace Papers
- GitHub: llm-in-sandbox/llm-in-sandbox
