# 11 — Qwen3-ASR: Speech Recognition cho Multi-Agent System

> **Mục đích training:** Hiểu Qwen3-ASR model — multi-language ASR supporting 52 languages/dialects, deployment patterns, và cách tích hợp voice input cho enterprise agents.

---

## 1. Tổng quan Qwen3-ASR

### 1.1 Model Family
- **Qwen3-ASR-1.7B** — Full-size, state-of-the-art accuracy
- **Qwen3-ASR-0.6B** — Lightweight, 2000x throughput at concurrency 128
- **Qwen3-ForcedAligner-0.6B** — Timestamp prediction cho 11 languages
- **Base:** Qwen3-Omni foundation model

### 1.2 Supported Languages (52 total)

**30 Languages:**
Chinese, English, Cantonese, Arabic, German, French, Spanish, Portuguese, Indonesian, Italian, Korean, Russian, Thai, Vietnamese, Japanese, Turkish, Hindi, Malay, Dutch, Swedish, Danish, Finnish, Polish, Czech, Filipino, Persian, Greek, Hungarian, Macedonian, Romanian

**22 Chinese Dialects:**
Anhui, Dongbei, Fujian, Gansu, Guizhou, Hebei, Henan, Hubei, Hunan, Jiangxi, Ningxia, Shandong, Shaanxi, Shanxi, Sichuan, Tianjin, Yunnan, and more

### 1.3 Key Features
```
ALL-IN-ONE: Language ID + ASR in single model
EXCELLENT:  SOTA accuracy + robust in noisy environments
FAST:       0.6B version = 2000x throughput (concurrent 128)
STREAMING:  Real-time inference support
ALIGNMENT:  Forced aligner for word-level timestamps
```

---

## 2. Quick Start

### 2.1 Installation

```bash
# Create clean environment
conda create -n qwen3-asr python=3.12 -y
conda activate qwen3-asr

# Install with transformers backend
pip install -U qwen-asr

# Install with vLLM backend (faster)
pip install -U qwen-asr[vllm]

# Optional: FlashAttention 2 (recommended)
pip install -U flash-attn --no-build-isolation
```

### 2.2 Basic Usage (Transformers)

```python
import torch
from qwen_asr import Qwen3ASRModel

model = Qwen3ASRModel.from_pretrained(
    "Qwen/Qwen3-ASR-1.7B",
    dtype=torch.bfloat16,
    device_map="cuda:0",
    max_inference_batch_size=32,
    max_new_tokens=256,
)

# Transcribe audio
results = model.transcribe(
    audio="path/to/audio.wav",
    language=None,  # Auto-detect language
)

print(results[0].language)  # e.g., "English"
print(results[0].text)       # Transcribed text
```

### 2.3 With Timestamps (Forced Aligner)

```python
model = Qwen3ASRModel.from_pretrained(
    "Qwen/Qwen3-ASR-1.7B",
    dtype=torch.bfloat16,
    device_map="cuda:0",
    max_inference_batch_size=32,
    max_new_tokens=256,
    forced_aligner="Qwen/Qwen3-ForcedAligner-0.6B",
    forced_aligner_kwargs=dict(
        dtype=torch.bfloat16,
        device_map="cuda:0",
    ),
)

results = model.transcribe(
    audio=["audio_zh.wav", "audio_en.wav"],
    language=["Chinese", "English"],
    return_time_stamps=True,
)

for r in results:
    print(r.language, r.text)
    for ts in r.time_stamps[0]:
        print(f"  {ts.text}: {ts.start_time:.2f}s - {ts.end_time:.2f}s")
```

---

## 3. vLLM Deployment (Production)

### 3.1 Start Server

```bash
# Simple server start
qwen-asr-serve Qwen/Qwen3-ASR-1.7B \
    --gpu-memory-utilization 0.8 \
    --host 0.0.0.0 \
    --port 8000
```

### 3.2 OpenAI-Compatible API

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

# Chat completions API
response = client.chat.completions.create(
    model="Qwen/Qwen3-ASR-1.7B",
    messages=[{
        "role": "user",
        "content": [{
            "type": "audio_url",
            "audio_url": {"url": "https://example.com/audio.wav"}
        }]
    }]
)
print(response.choices[0].message.content)

# Transcription API
transcription = client.audio.transcriptions.create(
    model="Qwen/Qwen3-ASR-1.7B",
    file=audio_bytes,
)
print(transcription.text)
```

### 3.3 Docker Deployment

```bash
docker run --gpus all --name qwen3-asr \
    -p 8000:80 \
    --shm-size=4gb \
    -it qwenllm/qwen3-asr:latest
```

### 3.4 Streaming Inference

```bash
# Launch streaming web demo
qwen-asr-demo-streaming \
    --asr-model-path Qwen/Qwen3-ASR-1.7B \
    --host 0.0.0.0 \
    --port 8000 \
    --gpu-memory-utilization 0.9
```

---

## 4. Integration vào Multi-Agent System

### 4.1 Voice-Enabled Agent Architecture

```
┌─────────────────────────────────────────────┐
│          VOICE-ENABLED AGENT SYSTEM          │
├─────────────────────────────────────────────┤
│                                             │
│  AUDIO INPUT                                │
│  ├─ Microphone (real-time)                  │
│  ├─ Audio file upload                       │
│  └─ Phone call (VoIP)                       │
│       │                                     │
│  QWEN3-ASR (Speech-to-Text)                │
│  ├─ Language detection                      │
│  ├─ Transcription                          │
│  ├─ Timestamps                             │
│  └─ Speaker diarization (future)            │
│       │                                     │
│  ORCHESTRATOR AGENT                         │
│  ├─ Parse intent from transcript            │
│  ├─ Route to appropriate agent              │
│  └─ Maintain conversation context           │
│       │                                     │
│  [CTO / COO / ReconcileGPT / ...]          │
│       │                                     │
│  TTS (Text-to-Speech) → Audio output       │
│                                             │
└─────────────────────────────────────────────┘
```

### 4.2 Implementation Pattern

```python
class VoiceEnabledAgent:
    """Agent that accepts voice input via Qwen3-ASR"""
    
    def __init__(self, agent, asr_model):
        self.agent = agent  # Any EMADS-PR agent
        self.asr = asr_model
    
    async def process_voice(self, audio_input):
        # Step 1: Speech to text
        transcription = self.asr.transcribe(
            audio=audio_input,
            language=None  # Auto-detect
        )
        
        text = transcription[0].text
        language = transcription[0].language
        
        # Step 2: Log for audit
        log_voice_input(
            text=text,
            language=language,
            timestamp=datetime.now()
        )
        
        # Step 3: Pass to agent
        response = await self.agent.process(text)
        
        return {
            "transcription": text,
            "language": language,
            "agent_response": response
        }
```

### 4.3 Vietnamese Language Support
- Qwen3-ASR hỗ trợ **Vietnamese** natively
- Quan trọng cho **EMADS-PR triển khai tại VN**
- Voice commands bằng tiếng Việt → agents hiểu và thực thi

---

## 5. Use Cases

### 5.1 Meeting Transcription + Agent Analysis
```
Meeting Audio → Qwen3-ASR → Transcript
    ↓
Analyst Agent → Extract action items
    ↓
Scheduler Agent → Create calendar events
    ↓
Summary Agent → Generate meeting notes
```

### 5.2 Customer Service Voice Agent
```
Customer Call → Qwen3-ASR (streaming)
    ↓
Intent Detection → Route to specialist
    ↓
Agent resolves issue (text-based reasoning)
    ↓
TTS → Voice response to customer
```

### 5.3 Quality Assurance
```
Agent Conversations (recorded) → Qwen3-ASR
    ↓
Compliance Agent → Check for violations
    ↓
Quality Agent → Score interaction quality
    ↓
Training Agent → Generate improvement suggestions
```

---

## 6. Performance & Sizing

| Model | Params | Accuracy | Throughput | GPU Memory |
|-------|--------|----------|-----------|------------|
| Qwen3-ASR-1.7B | 1.7B | SOTA | Standard | ~4GB |
| Qwen3-ASR-0.6B | 0.6B | Near-SOTA | 2000x (concurrent) | ~2GB |
| ForcedAligner-0.6B | 0.6B | High timestamp accuracy | Fast | ~2GB |

### Sizing Recommendation cho Enterprise:
- **Development/Testing:** 0.6B on single GPU
- **Production (low traffic):** 1.7B on single A100
- **Production (high traffic):** 0.6B + vLLM + multiple GPUs
- **Edge deployment:** 0.6B on consumer GPU (RTX 3090+)

---

## 7. Key Takeaways cho Training

1. **Qwen3-ASR** = state-of-the-art ASR supporting 52 languages including Vietnamese
2. **Two sizes:** 1.7B (accuracy) vs 0.6B (throughput — 2000x faster)
3. **Forced Aligner** = word-level timestamps cho 11 languages
4. **vLLM deployment** = OpenAI-compatible API, production-ready
5. **Voice-enabled agents** = audio input → ASR → agent → response
6. **Vietnamese support** = critical cho EMADS-PR deployment tại VN
7. **Streaming inference** = real-time transcription cho live conversations

---

## Nguồn tham khảo
- HuggingFace: Qwen/Qwen3-ASR-0.6B Model Card
- Qwen3-ASR Technical Report (arXiv:2601.21337)
- GitHub: QwenLM/Qwen3-ASR
- vLLM Documentation
