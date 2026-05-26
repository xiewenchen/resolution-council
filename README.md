# 🏛️ Resolution Council AI

> **Stop designing system architecture manually.**

One-call system design compiler. Natural language in → production architecture out.

```text
Before: Chat with LLM  →  vague prose, no structure, no trade-offs
After:  resolve(task)  →  architecture + cost + risk + roadmap + ranked trade-offs
```

```python
from resolution_council import ResolutionCouncil

plan = ResolutionCouncil().resolve("build a real-time translation system")
print(plan.final_plan)
```

**Zero dependencies. Deterministic. <1ms.**

---

## Output

**Input:**
> "Design a real-time voice translation system with subtitles, supporting Chinese and English, sub-500ms latency, offline capable"

**Output:**

```
================================================================
  Resolution Council AI · System Architecture Plan
================================================================

Executive Summary
  Constructed using pattern-matching against 3 known architectures.
  Evaluated through 5 independent perspectives. 34 recommendations ranked.

Architecture
  • Event-driven pipeline: ASR → Translation → Subtitle → Output
  • 5 bounded contexts, each independently scalable
  • Async non-blocking I/O throughout all stages

Tech Stack (ranked by feasibility × cost × compatibility)
  • [architecture] NATS — sub-ms inter-service messaging
  • [architecture] Docker + Kubernetes — containerized deployment
  • [cost] Faster Whisper — 4x cheaper than vanilla, offline capable
  • [cost] DeepSeek — competitive quality, self-hostable
  • [risk] Circuit breaker + dead letter queue for fault tolerance
  • [scalability] Horizontal scaling: stateless services + PgBouncer

Cost Estimate
  $200-2000/month depending on scale (self-hosted reduces to $0-50/month)

Risks & Mitigations
  ⚠ Real-time failover required → circuit breaker pattern
  ⚠ Innovation vs stability tension → novel tech in non-critical paths only

Execution Roadmap
  Phase 1: Core ASR pipeline
  Phase 2: Translation module integration
  Phase 3: End-to-end testing + latency optimization
  Phase 4: Monitoring + error handling
  Phase 5: Scale testing + production launch

================================================================
  ⚡ Generated in 0.002s
```

---

## How it works

Internally, the system uses a **three-stage reasoning pipeline**:

```
Natural Language Input
        │
        ▼
  ┌─────────────┐
  │ Central Brain│  Analyzes the task, selects reasoning mode:
  │              │  • First Principles (novel domains)
  │              │  • Engineering Patterns (known solutions)
  │              │  • Analogy Transfer (similar projects)
  └──────┬──────┘
         │ decomposed sub-problems
         ▼
  ┌─────────────┐
  │ 5-Perspective│  Each view independently evaluates the design:
  │  Evaluators  │  Architecture · Cost · Risk · Scalability · Innovation
  └──────┬──────┘
         │ structured perspectives
         ▼
  ┌─────────────┐
  │ Fusion Engine│  Scores, deduplicates, resolves conflicts,
  │              │  produces final ranked plan
  └──────┬──────┘
         │
         ▼
    Final Plan
```

**No LLM API required.** Pure deterministic reasoning. Runs locally in <5ms.

---

## Why it's different

| Traditional approach | Resolution Council AI |
|---------------------|----------------------|
| Chat with an LLM, get prose | **Structured architecture output** |
| One answer, no alternatives | **5 perspectives, ranked & compared** |
| No cost/risk analysis | **Explicit trade-offs quantified** |
| Hallucinates confidently | **Deterministic, reproducible results** |
| Requires prompt engineering | **Natural language input, zero configuration** |

**We built an AI that thinks like a system architect, not a chatbot.**

---

## Install

```bash
pip install resolution-council
```

- **Zero dependencies** — pure Python 3.10+
- **<5ms execution** — no API calls, no network
- **Deterministic** — same input always produces same output

---

## Demo

```bash
# Single task
python demo.py "build a real-time translation system"

# Run all preset demos
python demo.py --demo all
```

Preset demos: real-time translation · RAG knowledge base · multi-agent customer service · high-concurrency API gateway

---

## The core insight

```text
System architecture design is a structured reasoning problem,
not a language generation problem.
```

Resolution Council AI replaces "manual system design thinking" with "structured AI architecture generation."

---

## License

MIT


