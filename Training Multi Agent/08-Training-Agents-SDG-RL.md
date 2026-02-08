# 08 — Training AI Agents với Synthetic Data Generation (SDG) & Reinforcement Learning (RL)

> **Mục đích training:** Hiểu phương pháp train agent từ NVIDIA: kết hợp Synthetic Data Generation + Reinforcement Learning with Verifiable Rewards (RLVR) + GRPO.

---

## 1. Tổng quan Pipeline

### 1.1 Vấn đề
- Training data cho AI agents rất khó thu thập (cần expert trajectories)
- Human annotation đắt đỏ và không scale được
- Real-world agent data có noise, bias, incomplete

### 1.2 Giải pháp: SDG + RL Pipeline

```
┌─────────────────────────────────────────────────┐
│             NVIDIA TRAINING PIPELINE             │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. BASE MODEL                                  │
│     └─ Nemotron-Nano-9B-V2 (or similar)        │
│        │                                        │
│  2. SYNTHETIC DATA GENERATION (SDG)             │
│     └─ NeMo Data Designer                      │
│     └─ Generate diverse training scenarios      │
│     └─ Auto-validate & filter                   │
│        │                                        │
│  3. SUPERVISED FINE-TUNING (SFT)               │
│     └─ Train on synthetic data                  │
│     └─ Learn basic tool use & reasoning         │
│        │                                        │
│  4. REINFORCEMENT LEARNING (RLVR)              │
│     └─ NeMo Gym environments                   │
│     └─ Verifiable rewards (no reward model)     │
│     └─ GRPO optimization                       │
│        │                                        │
│  5. EVALUATION & ITERATION                      │
│     └─ Benchmark against baselines              │
│     └─ Human-in-the-loop feedback               │
│     └─ Iterate & improve                        │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 2. Synthetic Data Generation (SDG)

### 2.1 NeMo Data Designer
- Tool để generate synthetic training data cho agents
- Input: task description + tool schemas + constraints
- Output: diverse (query, trajectory, answer) tuples

### 2.2 SDG Strategy

```python
# Concept: Generating synthetic agent training data
class SyntheticDataGenerator:
    def __init__(self, teacher_model, tools_schema):
        self.teacher = teacher_model  # Strong LLM (e.g., GPT-4)
        self.tools = tools_schema
    
    def generate_scenario(self, domain, difficulty):
        """Generate one training scenario"""
        
        # 1. Generate task
        task = self.teacher.generate(f"""
        Create a realistic {domain} task that requires 
        using these tools: {self.tools}
        Difficulty: {difficulty}/10
        Include: clear goal, constraints, expected outcome
        """)
        
        # 2. Generate expert trajectory  
        trajectory = self.teacher.generate(f"""
        Solve this task step by step:
        Task: {task}
        Available tools: {self.tools}
        Show reasoning + tool calls + final answer
        """)
        
        # 3. Validate
        is_valid = self.validate_trajectory(task, trajectory)
        
        return {
            "task": task,
            "trajectory": trajectory,
            "difficulty": difficulty,
            "valid": is_valid
        }
    
    def generate_dataset(self, domains, n_per_domain=1000):
        """Generate full training dataset"""
        dataset = []
        for domain in domains:
            for difficulty in range(1, 11):
                for _ in range(n_per_domain // 10):
                    sample = self.generate_scenario(domain, difficulty)
                    if sample["valid"]:
                        dataset.append(sample)
        return dataset
```

### 2.3 Quality Filters cho Synthetic Data

```python
def validate_trajectory(task, trajectory):
    """Multi-layer validation"""
    
    # Check 1: Tool calls are valid
    for call in trajectory.tool_calls:
        if call.tool not in AVAILABLE_TOOLS:
            return False
    
    # Check 2: Answer is verifiable
    if not can_verify_answer(task, trajectory.final_answer):
        return False
    
    # Check 3: Reasoning is coherent
    if not check_reasoning_chain(trajectory.steps):
        return False
    
    # Check 4: No hallucination in tool outputs
    for step in trajectory.steps:
        if step.type == "tool_call":
            actual = execute_tool(step.tool, step.args)
            if actual != step.expected_output:
                return False
    
    return True
```

---

## 3. Reinforcement Learning with Verifiable Rewards (RLVR)

### 3.1 Concept
- **Khác reward model truyền thống:** KHÔNG dùng learned reward model
- **Verifiable rewards:** reward dựa trên kết quả **kiểm chứng được**
- Ví dụ: đáp án đúng → reward 1, sai → reward 0

### 3.2 Reward Design cho Agents

```python
def compute_reward(task, agent_trajectory, ground_truth):
    """
    Verifiable reward function cho agent training.
    Không cần reward model — chỉ cần verify output.
    """
    reward = 0.0
    
    # Component 1: Correctness (0 or 1)
    if verify_answer(agent_trajectory.final_answer, ground_truth):
        reward += 1.0
    
    # Component 2: Efficiency bonus (0 to 0.3)
    if len(agent_trajectory.steps) <= OPTIMAL_STEPS:
        efficiency = 1 - (len(agent_trajectory.steps) / MAX_STEPS)
        reward += 0.3 * efficiency
    
    # Component 3: Tool usage quality (0 to 0.2)
    valid_tool_calls = sum(
        1 for call in agent_trajectory.tool_calls
        if call.successful
    )
    total_tool_calls = len(agent_trajectory.tool_calls)
    if total_tool_calls > 0:
        reward += 0.2 * (valid_tool_calls / total_tool_calls)
    
    # Penalty: Unnecessary actions (-0.1 each)
    unnecessary = count_unnecessary_steps(agent_trajectory)
    reward -= 0.1 * unnecessary
    
    return max(reward, 0.0)  # Clamp to non-negative
```

### 3.3 NeMo Gym Environments
- Simulated environments cho agent training
- Tool execution sandbox (safe to explore)
- Automatic reward computation
- Parallelized training across many environments

---

## 4. GRPO (Group Relative Policy Optimization)

### 4.1 Algorithm

```
For each training task:
1. Sample K responses from current policy
2. Compute verifiable reward for each response
3. Rank responses by reward
4. Update policy:
   - Increase probability of high-reward responses
   - Decrease probability of low-reward responses
   - Relative ranking, not absolute reward
```

### 4.2 Ưu điểm GRPO vs PPO

| Feature | PPO | GRPO |
|---------|-----|------|
| Reward model needed | Yes | No (verifiable) |
| Critic network | Yes | No |
| Training stability | Moderate | High |
| Compute requirement | High (2 models) | Lower (1 model) |
| Sample efficiency | Moderate | Good |

### 4.3 Pseudo-code

```python
def grpo_training_step(policy, tasks, K=8):
    """One GRPO training step"""
    
    all_samples = []
    
    for task in tasks:
        # 1. Sample K responses
        responses = [policy.generate(task) for _ in range(K)]
        
        # 2. Compute verifiable rewards
        rewards = [compute_reward(task, r) for r in responses]
        
        # 3. Group relative ranking
        mean_reward = sum(rewards) / len(rewards)
        std_reward = std(rewards)
        advantages = [(r - mean_reward) / (std_reward + 1e-8) 
                      for r in rewards]
        
        all_samples.extend(zip(responses, advantages))
    
    # 4. Policy gradient update
    loss = 0
    for response, advantage in all_samples:
        log_prob = policy.log_probability(response)
        loss -= log_prob * advantage  # Policy gradient
    
    loss.backward()
    optimizer.step()
```

---

## 5. Human-in-the-Loop Integration

### 5.1 Khi nào cần Human?
```
AUTO (No human needed):
├─ Verifiable answers (math, code, factual)
├─ Tool execution validation
└─ Format/structure checks

HUMAN REVIEW:
├─ Subjective quality assessment
├─ Edge cases & ambiguous scenarios
├─ Safety/ethics evaluation
└─ Domain expert validation
```

### 5.2 Active Learning Loop
```
Agent generates responses
    ↓
Auto-verify what's possible
    ↓
Flag uncertain/edge cases for human review
    ↓
Human labels → augment training data
    ↓
Retrain → better agent
    ↓
Fewer human reviews needed (virtuous cycle)
```

---

## 6. Application cho EMADS-PR Training

### 6.1 Training Data cho mỗi Agent Role

| Agent | SDG Focus | Reward Signal |
|-------|-----------|---------------|
| CTO Agent | Tech decision scenarios | Correct architecture choice + cost efficiency |
| COO Agent | Resource allocation problems | Optimal allocation + constraint satisfaction |
| ReconcileGPT | Conflict resolution cases | Fair trade-off + stakeholder satisfaction |
| Risk Agent | Threat assessment scenarios | Accurate risk identification + mitigation quality |
| Cost Agent | Budget optimization problems | Cost minimization + quality maintenance |

### 6.2 Training Schedule

```
Phase 1: SFT on Synthetic Data (Week 1-2)
├─ Generate 10K scenarios per agent role
├─ Fine-tune base model for each role
└─ Validate basic competency

Phase 2: RLVR Training (Week 3-4)
├─ NeMo Gym environments for each role
├─ GRPO optimization
└─ Focus on efficiency + accuracy

Phase 3: Multi-Agent RL (Week 5-6)
├─ Agents interact in simulated environment
├─ Reward for collaborative task completion
└─ Penalize conflicts, reward consensus

Phase 4: Human Evaluation (Week 7-8)
├─ Domain experts evaluate agent outputs
├─ Fine-tune on human feedback
└─ Final benchmarking
```

---

## 7. Key Takeaways cho Training

1. **SDG + RL pipeline** = generate data → SFT → RLVR → evaluate → iterate
2. **Synthetic data** giải quyết scarcity problem — dùng teacher model generate
3. **Verifiable rewards** = không cần reward model, verify output trực tiếp
4. **GRPO** = efficient RL training, compare K samples relatively
5. **NeMo tools** = Data Designer (SDG) + NeMo Gym (RL environments)
6. **Human-in-the-loop** chỉ cho uncertain/edge cases → active learning
7. **Multi-phase training** = SFT → RLVR → Multi-Agent RL → Human eval

---

## Nguồn tham khảo
- NVIDIA Blog: "Training an AI Agent with SDG and RL"
- NeMo Documentation: Data Designer & NeMo Gym
- GRPO: DeepSeek-Math paper
- RLVR: Reinforcement Learning with Verifiable Rewards
