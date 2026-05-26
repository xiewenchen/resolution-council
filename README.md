# 🏛️ Resolution Council AI

> Turn requirements into system architecture in one call.

```text
Before: LLM chat → vague answer
After:  resolve(task) → architecture + trade-offs + roadmap
```

```python
from resolution_council import ResolutionCouncil
ResolutionCouncil().resolve("build a real-time translation system").final_plan
```

Zero dependencies. Deterministic. <1ms.

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

## Why this, not an LLM

| LLM chat | Resolution Council AI |
|----------|----------------------|
| Vague prose | **Structured architecture** |
| One opinion | **5 perspectives, ranked** |
| No trade-offs | **Cost, risk, scalability quantified** |
| Hallucinates | **Deterministic, reproducible** |
| Prompt engineering | **Natural language, zero config** |

---

## Install

```bash
pip install resolution-council
python demo.py "build a real-time translation system"
```

---

## License

MIT


