"""
COUNCIL — Five lightweight perspective generators.
Each produces structured recommendations from one angle.
No voting. No hierarchy. Pure generation.
"""

from __future__ import annotations

import re

from .types import CouncilOutput, DecomposedTask, Perspective


_TECH = {
    "whisper":              "Whisper (OpenAI) — 99 languages, offline capable, free",
    "faster-whisper":       "Faster Whisper (CTranslate2) — 4x speedup, lower memory, free",
    "deepgram":             "Deepgram — lowest latency, cloud-only, paid",
    "deepseek":             "DeepSeek — strong coding + translation, self-hostable, low cost",
    "gpt-4o":               "GPT-4o — best quality, multimodal, API-only, high cost",
    "llama":                "Llama 3 — fully local, good for privacy, free",
    "chroma":               "Chroma — embedded vector DB, local-first, free",
    "qdrant":               "Qdrant — production vector DB, filtering, free/paid",
    "bge-large":            "BGE Large — best Chinese embedding model, free",
    "nats":                 "NATS — sub-ms pub/sub, lightweight, free",
    "kafka":                "Kafka — high throughput event streaming, ops-heavy",
    "fastapi":              "FastAPI — async Python, auto OpenAPI docs, free",
    "redis":                "Redis — caching, pub/sub, queue, ubiquitous, free",
    "docker":               "Docker — standard containerization, free",
    "kubernetes":           "Kubernetes — container orchestration, auto-scaling",
    "svelte":               "Svelte — compile-time framework, minimal bundle, free",
    "react":                "React — largest ecosystem, component library, free",
    "paddle-ocr":           "PaddleOCR — best Chinese OCR, free",
    "langchain":            "LangChain — rich LLM integrations, agent framework, free",
    "postgres":             "PostgreSQL — ACID, full-text search, extensions, free",
    "celery":               "Celery — distributed task queue, Python-native, free",
    "prometheus":           "Prometheus + Grafana — metrics, alerting, dashboards, free",
}


def architecture_view(task: DecomposedTask) -> CouncilOutput:
    recs: list[str] = []
    tech: list[str] = []
    t = task.original.lower()

    # Pattern selection
    is_streaming = any(k in t for k in ["stream", "real.time", "pipeline", "实时"])
    is_agent = any(k in t for k in ["agent", "assistant", "coding"])
    is_distributed = any(k in t for k in ["distributed", "task", "schedul"])

    if is_streaming:
        recs.append("Event-driven pipeline: each stage as independent async service")
        tech.append("NATS — sub-ms inter-service messaging")
    elif is_agent:
        recs.append("Agent loop architecture: observe → plan → execute → validate")
        recs.append("Tool-use layer with sandboxed execution environment")
        tech.append("LangChain or custom agent runtime")
    elif is_distributed:
        recs.append("Task queue + worker pool architecture")
        recs.append("State persisted in PostgreSQL, tasks dispatched via Redis")
        tech.append("Celery + Redis for task queue")
        tech.append("PostgreSQL for persistent state")
    else:
        recs.append("Layered architecture: API Gateway → Services → Data Layer")

    # Decomposition
    if task.sub_problems:
        recs.append(f"Decompose into {len(task.sub_problems)} bounded contexts")

    # Deployment
    needs_offline = any(c in " ".join(task.constraints).lower()
                        for c in ["offline", "local", "without internet"])
    if needs_offline:
        recs.append("Self-contained deployment: Docker Compose, all local")
        tech.append("Docker + docker-compose")
    else:
        recs.append("Cloud-native deployment: containerized with auto-scaling")
        tech.append("Docker + Kubernetes")

    tech.append("FastAPI — async, auto-docs, type-safe")
    tech.append("PostgreSQL — primary database + Redis — cache/queue")

    if any(k in t for k in ["ui", "frontend", "web", "界面"]):
        tech.append("Svelte + Tailwind CSS — minimal bundle, fast")

    return CouncilOutput(
        perspective=Perspective.ARCHITECTURE,
        summary="Event-driven pipeline architecture" if is_streaming
        else "Layered service architecture",
        recommendations=recs,
        tech_choices=tech,
        confidence=0.85,
    )


def cost_view(task: DecomposedTask) -> CouncilOutput:
    recs: list[str] = []
    warnings: list[str] = []
    tech: list[str] = []
    t = task.original.lower()
    all_text = " ".join([task.original] + task.constraints).lower()

    needs_offline = any(k in all_text for k in ["offline", "local", "without internet"])
    is_small = any(k in t for k in ["personal", "prototype", "small", "个人"])
    has_ai = bool(re.search(r'\b(ai|llm|agents?|gpt)\b', t)) or any(k in t for k in ["translat", "speech"])

    if needs_offline and has_ai:
        recs.append("Prefer open-source self-hosted models: DeepSeek, Llama, Whisper")
        recs.append("One-time GPU investment ($2-5K) vs recurring API costs")
        tech.append("Faster Whisper — 4x cheaper inference than vanilla")
        tech.append("DeepSeek — competitive quality, fraction of GPT-4o cost")
        warnings.append("Self-hosting requires GPU server: ~$2-5K one-time")
    elif has_ai:
        recs.append("API-first: pay-per-use, zero infra burden for MVP")
        recs.append("GPT-4o Mini for cost-sensitive, GPT-4o for critical quality")
        tech.append("GPT-4o Mini — cost-effective for 90% of requests")
        warnings.append("API costs scale linearly — budget for growth")
    else:
        recs.append("Standard cloud infrastructure: no special compute needed")

    recs.append("Implement multi-tier caching to reduce redundant compute")
    tech.append("Redis — translation cache, embedding cache, session store")

    if is_small:
        recs.append("Estimate: $0-50/month self-hosted, $50-200/month API-based")
    else:
        recs.append("Estimate: $200-2000/month depending on scale")

    return CouncilOutput(
        perspective=Perspective.COST,
        summary="Optimize total cost of ownership: open-source where parity exists",
        recommendations=recs,
        tech_choices=tech,
        warnings=warnings,
        confidence=0.80,
    )


def risk_view(task: DecomposedTask) -> CouncilOutput:
    recs: list[str] = []
    warnings: list[str] = []
    t = task.original.lower()

    # API / service risks
    if any(k in t for k in ["api", "service", "web", "gateway"]):
        recs.append("API authentication: JWT/OAuth2 with refresh tokens")
        recs.append("Rate limiting: per-user, per-IP, configurable tiers")
        warnings.append("Public endpoints are attack surface — always require auth")

    # AI-specific risks — word-boundary match to avoid false positives (e.g. "failure")
    if re.search(r'\b(ai|llm|agents?|gpt|openai|claude|chatbot)\b', t):
        recs.append("Prompt injection guard: input sanitization + output validation")
        recs.append("Hallucination check: validate LLM outputs in critical paths")
        warnings.append("LLM outputs are non-deterministic — always validate")
        warnings.append("External model APIs may log data — verify privacy policy")

    # Real-time risks
    if any(k in t for k in ["real.time", "stream", "实时"]):
        recs.append("Circuit breaker pattern for downstream failures")
        recs.append("Dead letter queue for failed/unprocessable messages")
        warnings.append("Real-time systems require failover strategy")

    # Data risks
    if any(k in t for k in ["data", "database", "user", "auth"]):
        recs.append("Automated backups with point-in-time recovery")
        warnings.append("Database is single point of failure — plan replication")

    # General hardening
    recs.append("Structured JSON logging with correlation IDs")
    recs.append("Health check endpoints on all services")

    return CouncilOutput(
        perspective=Perspective.RISK,
        summary=f"Identified {len(warnings)} key risk areas requiring mitigation",
        recommendations=recs,
        warnings=warnings,
        confidence=0.90,
    )


def scalability_view(task: DecomposedTask) -> CouncilOutput:
    recs: list[str] = []
    tech: list[str] = []
    t = task.original.lower()

    high_scale = any(k in t for k in ["million", "high.concurrency", "万", "亿", "scale"])

    if high_scale:
        recs.append("Horizontal scaling: stateless services behind load balancer")
        recs.append("Database: read replicas + connection pooling (PgBouncer)")
        tech.append("Kubernetes HPA for auto-scaling")
    else:
        recs.append("Vertical scaling sufficient for initial scale")
        recs.append("Design for horizontal scaling readiness: stateless services")

    if any(k in t for k in ["real.time", "stream", "low.latency", "实时"]):
        recs.append("Async non-blocking I/O throughout all stages")
        recs.append("gRPC for internal service communication (lower overhead than REST)")

    recs.append("Multi-tier caching: application, database, edge/CDN")
    tech.append("Redis for distributed caching")
    tech.append("Prometheus + Grafana for metrics and alerting")

    if bool(re.search(r'\b(ai|llm|agents?)\b', t)) or any(k in t for k in ["gpu"]):
        recs.append("GPU inference is the bottleneck — batch requests, use quantization")
        tech.append("vLLM or llama.cpp for optimized inference throughput")

    return CouncilOutput(
        perspective=Perspective.SCALABILITY,
        summary="Design for growth: stateless services, async I/O, tiered caching",
        recommendations=recs,
        tech_choices=tech,
        confidence=0.82,
    )


def innovation_view(task: DecomposedTask) -> CouncilOutput:
    recs: list[str] = []
    t = task.original.lower()

    has_speech = any(k in t for k in ["speech", "voice", "audio"])
    has_translation = any(k in t for k in ["translat"])
    has_agent = any(k in t for k in ["agent", "assistant", "autonomous"])
    has_multimodal = has_speech and has_translation

    if has_multimodal:
        recs.append("Fully local multimodal pipeline — competitive moat for privacy")
        recs.append("Streaming architecture: <500ms end-to-end as differentiator")
        recs.append("Modular design: swap ASR/Translation/TTS independently")

    if has_agent:
        recs.append("Reflection loop: agent self-corrects hallucinations")
        recs.append("Memory-augmented: persists conversation context for personalization")
        recs.append("Plugin system: community-contributed tool integrations")

    if not recs:
        recs.append("Open-core model: open-source core, premium features as paid add-ons")
        recs.append("Plugin architecture for community extensibility")

    # Differentiator
    if has_speech and has_translation:
        recs.append("Unique: lowest-latency fully-offline translation with speaker diarization")

    return CouncilOutput(
        perspective=Perspective.INNOVATION,
        summary="Maximize differentiation through unique technical combinations",
        recommendations=recs,
        confidence=0.75,
    )


def deliberate(task: DecomposedTask) -> list[CouncilOutput]:
    """Run all 5 perspectives. Pure generation, no decision-making."""
    return [
        architecture_view(task),
        cost_view(task),
        risk_view(task),
        scalability_view(task),
        innovation_view(task),
    ]
