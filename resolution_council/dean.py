"""
DEAN — Central Intelligence Core.
Single reasoning engine with 3 internal modes.
All internal reasoning in English. Deterministic output.
"""

from __future__ import annotations

import re

from .types import DeanMode, DecomposedTask


# ── Engineering Pattern Library ───────────────────────────────────────

PATTERNS: dict[str, dict] = {
    # Speech / Translation
    r"(speech|voice|audio|asr|stt).*(translat|字幕|subtitle|caption)": {
        "pattern": "Streaming ASR → Translation Engine → Subtitle Renderer → Output",
        "similar": ["OpenAI Whisper + WebVTT pipeline", "Google STT + Translate cascade"],
        "constraints": ["sub-500ms end-to-end latency", "multi-language support"],
        "tech_hints": ["faster-whisper", "deepseek", "nats"],
    },
    r"(speech|voice|audio|asr|stt)": {
        "pattern": "Audio Input → Streaming ASR → Text Output",
        "similar": ["Whisper streaming pipeline", "Deepgram real-time API"],
        "constraints": ["low latency streaming", "noise robustness"],
        "tech_hints": ["whisper", "faster-whisper"],
    },
    r"translat": {
        "pattern": "Input Text → Translation Model → Post-process → Output",
        "similar": ["DeepL API integration", "LLM-based translation pipeline"],
        "constraints": ["terminology consistency", "context awareness"],
        "tech_hints": ["deepseek", "gpt-4o", "llama"],
    },

    # RAG / Knowledge
    r"(rag|retriev|knowledge.*base|知识库|search)": {
        "pattern": "Ingest → Embed → Store → Hybrid Retrieve → Generate",
        "similar": ["Danswer enterprise RAG", "LlamaIndex chunking pipeline"],
        "constraints": ["hybrid search (dense + sparse)", "source citation"],
        "tech_hints": ["chroma", "qdrant", "bge-large", "rerank"],
    },

    # Agent / Assistant
    r"(agent|assistant|customer.*service|客服|chatbot)": {
        "pattern": "Intent Router → Knowledge Base → LLM → Response → Feedback Loop",
        "similar": ["Rasa + LLM hybrid agent", "LangChain tool-use agent"],
        "constraints": ["multi-turn dialogue", "hallucination guard", "fallback handling"],
        "tech_hints": ["langchain", "function-calling", "rag"],
    },

    # API Gateway
    r"(api.*gateway|gateway|网关|proxy)": {
        "pattern": "Edge → Auth → Rate Limit → Route → Backend Services",
        "similar": ["Kong API Gateway", "Envoy proxy mesh"],
        "constraints": ["high concurrency", "sub-ms routing overhead"],
        "tech_hints": ["fastapi", "nginx", "redis"],
    },

    # Real-time / Streaming
    r"(real.?time|realtime|stream|实时)": {
        "pattern": "Event Source → Stream Processor → Real-time Output",
        "similar": ["Kafka Streams topology", "NATS JetStream pipeline"],
        "constraints": ["sub-second processing", "exactly-once semantics"],
        "tech_hints": ["nats", "kafka", "websocket"],
    },

    # Distributed / Task
    r"(distributed|task.*schedul|分布式|调度)": {
        "pattern": "Task Queue → Workers → Result Store → Scheduler",
        "similar": ["Celery task queue", "Temporal workflow engine"],
        "constraints": ["at-least-once delivery", "failure recovery"],
        "tech_hints": ["redis", "celery", "postgres"],
    },

    # Coding assistant
    r"(coding.*assistant|code.*generat|编程助手)": {
        "pattern": "Context Gatherer → LLM → Code Generator → Validator → Output",
        "similar": ["GitHub Copilot architecture", "Cursor IDE integration"],
        "constraints": ["code safety validation", "context window management"],
        "tech_hints": ["deepseek", "gpt-4o", "sandbox"],
    },

    # SaaS / Multi-tenant
    r"(saas|multi.?tenant|platform|多租户)": {
        "pattern": "Tenant Router → Isolated Services → Shared Data Layer",
        "similar": ["Auth0 multi-tenant architecture", "Stripe isolation model"],
        "constraints": ["data isolation", "per-tenant rate limiting"],
        "tech_hints": ["postgres", "redis", "docker"],
    },
}


# ── First Principles Decomposition ────────────────────────────────────

def _first_principles(task: str) -> DecomposedTask:
    """Decompose a novel task into irreducible sub-problems."""
    sub_problems: list[str] = []
    constraints: list[str] = []
    hints: list[str] = []

    t = task.lower()

    if any(k in t for k in ["speech", "voice", "audio"]):
        sub_problems.append("Audio capture and streaming: buffer management, chunking, real-time I/O")
        constraints.append("sub-500ms end-to-end latency")

    if any(k in t for k in ["asr", "speech.to.text", "transcribe", "recognize"]):
        sub_problems.append("Speech recognition: acoustic model, streaming decoder, language model integration")
        hints.append("AI > Speech > ASR")

    if any(k in t for k in ["translat"]):
        sub_problems.append("Machine translation: encoder-decoder, terminology consistency, context window")
        hints.append("AI > NLP > Translation")

    if any(k in t for k in ["subtitle", "caption"]):
        sub_problems.append("Subtitle rendering: timing alignment, text overlay, format encoding")
        hints.append("Multimodal > Subtitle")

    if any(k in t for k in ["real.time", "stream", "实时"]):
        sub_problems.append("Real-time pipeline: backpressure handling, buffer management, async I/O")
        constraints.append("streaming architecture required")

    if any(k in t for k in ["offline", "local"]):
        constraints.append("must operate without internet connectivity")
        constraints.append("all models must run locally")

    if any(k in t for k in ["multilingual", "multi.language"]):
        constraints.append("support multiple languages simultaneously")

    if any(k in t for k in ["agent", "assistant", "coding"]):
        sub_problems.append("Agent reasoning loop: observe → plan → execute → validate")
        hints.append("Agent > Framework")

    if any(k in t for k in ["distributed", "task", "schedul", "queue"]):
        sub_problems.append("Distributed coordination: task queue, worker pool, state management")
        constraints.append("handle node failures gracefully")

    if any(k in t for k in ["rag", "retriev", "knowledge", "search"]):
        sub_problems.append("Knowledge retrieval pipeline: embed → index → search → rerank → generate")
        hints.append("AI > NLP > RAG")

    # Fallback: generic decomposition
    if not sub_problems:
        sub_problems = [
            "Core domain logic: identify the fundamental computation",
            "Data model: entities, relationships, state management",
            "Interface layer: user/system interaction surface",
            "Infrastructure: deployment, scaling, monitoring",
        ]

    return DecomposedTask(
        original=task,
        sub_problems=sub_problems,
        constraints=list(dict.fromkeys(constraints)),
        domain_hints=list(dict.fromkeys(hints)),
        mode=DeanMode.FIRST_PRINCIPLES,
        similar_patterns=[],
    )


# ── Engineering Pattern Matching ──────────────────────────────────────

def _engineering(task: str) -> DecomposedTask:
    """Match task against known engineering patterns."""
    sub_problems: list[str] = []
    constraints: list[str] = []
    hints: list[str] = []
    similar: list[str] = []
    matched: list[str] = []

    for pattern, info in PATTERNS.items():
        if re.search(pattern, task, re.IGNORECASE):
            matched.append(info["pattern"])
            similar.extend(info.get("similar", []))
            constraints.extend(info.get("constraints", []))
            hints.extend(info.get("tech_hints", []))

    if matched:
        sub_problems = list(dict.fromkeys(matched))  # deduplicate
    else:
        sub_problems = [
            "Define system boundaries and external interfaces",
            "Design core data flow and processing pipeline",
            "Identify infrastructure requirements",
            "Plan deployment and scaling strategy",
        ]

    return DecomposedTask(
        original=task,
        sub_problems=sub_problems,
        constraints=list(dict.fromkeys(constraints)),
        domain_hints=list(dict.fromkeys(hints)),
        mode=DeanMode.ENGINEERING,
        similar_patterns=list(dict.fromkeys(similar)),
    )


# ── Analogy Transfer ──────────────────────────────────────────────────

def _analogy(task: str) -> DecomposedTask:
    """Adapt structurally similar solutions to the current task."""
    result = _engineering(task)
    result.mode = DeanMode.ANALOGY
    if result.similar_patterns:
        for sp in result.similar_patterns[:2]:
            result.sub_problems.append(f"Adapt from: {sp}")
    return result


# ── DEAN API ──────────────────────────────────────────────────────────

def analyze(task: str) -> DecomposedTask:
    """Single entry point. Selects the best reasoning mode automatically.

    Mode selection:
    - No known patterns → First Principles (Creative Brain)
    - ≥2 pattern matches → Analogy Transfer
    - 1 pattern match → Engineering Pattern Matching
    """
    matches = sum(
        1 for p in PATTERNS if re.search(p, task, re.IGNORECASE)
    )

    novelty_triggers = [
        r"novel", r"unprecedented", r"breakthrough", r"first.of.its.kind",
        r"创新", r"突破", r"前所未有",
    ]
    is_novel = any(re.search(t, task, re.IGNORECASE) for t in novelty_triggers)

    if is_novel or matches == 0:
        return _first_principles(task)
    if matches >= 2:
        return _analogy(task)
    return _engineering(task)
