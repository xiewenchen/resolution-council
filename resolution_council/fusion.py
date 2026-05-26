"""
Fusion Engine — Score, rank, resolve conflicts, produce single FinalPlan.
The ONLY decision layer. Outputs exactly one plan.
"""

from __future__ import annotations

from .types import (
    CouncilOutput,
    DecomposedTask,
    FinalPlan,
    FusionResult,
    Perspective,
    ScoredItem,
)


WEIGHTS = {
    "feasibility": 0.30,
    "compatibility": 0.20,
    "cost": 0.25,
    "innovation": 0.10,
    "risk": 0.15,
}


def _score(item: ScoredItem) -> float:
    return (
        WEIGHTS["feasibility"] * item.feasibility
        + WEIGHTS["compatibility"] * item.compatibility
        + WEIGHTS["cost"] * item.cost
        + WEIGHTS["innovation"] * item.innovation
        + WEIGHTS["risk"] * (1.0 if "risk" in item.source else 0.5)
    )


def _deduplicate(items: list[ScoredItem]) -> list[ScoredItem]:
    seen: set[str] = set()
    unique: list[ScoredItem] = []
    for item in items:
        key = " ".join(item.content.lower().split()[:5])
        if key not in seen:
            seen.add(key)
            unique.append(item)
        else:
            for existing in unique:
                ek = " ".join(existing.content.lower().split()[:5])
                if ek == key and _score(item) > _score(existing):
                    unique.remove(existing)
                    unique.append(item)
                    break
    return unique


def fuse(
    council_outputs: list[CouncilOutput],
    task: DecomposedTask,
) -> FusionResult:
    """Score and rank all council outputs. Detect conflicts and synergies."""

    items: list[ScoredItem] = []
    conflicts: list[str] = []
    synergies: list[str] = []

    for output in council_outputs:
        source = output.perspective.value

        for rec in output.recommendations:
            cost_s = 0.7
            innov_s = 0.5
            feas_s = 0.75

            if output.perspective == Perspective.COST:
                cost_s = 0.85
            elif output.perspective == Perspective.INNOVATION:
                innov_s = 0.85
                feas_s = 0.60
            elif output.perspective == Perspective.RISK:
                feas_s = 0.65

            items.append(ScoredItem(
                content=rec, source=source,
                feasibility=feas_s, compatibility=0.80,
                cost=cost_s, innovation=innov_s,
            ))

        for tech in output.tech_choices:
            items.append(ScoredItem(
                content=tech, source=source,
                feasibility=0.85, compatibility=0.75,
                cost=0.70, innovation=0.55,
            ))

    items = _deduplicate(items)
    for item in items:
        item.total = _score(item)
    items.sort(key=lambda x: x.total, reverse=True)

    # Conflict: innovation vs risk
    innov_items = [i for i in items if i.source == "innovation"]
    risk_items = [i for i in items if i.source == "risk"]
    if innov_items and risk_items:
        conflicts.append(
            "Innovation prefers novel approaches; Risk prefers proven solutions. "
            "Resolution: novel tech in non-critical paths, proven tech in critical paths."
        )

    # Synergy: architecture ↔ scalability alignment
    arch_items = [i for i in items if i.source == "architecture"]
    scale_items = [i for i in items if i.source == "scalability"]
    if arch_items and scale_items:
        synergies.append(
            "Architecture and scalability perspectives aligned: "
            "stateless services enable horizontal scaling."
        )

    return FusionResult(items=items, conflicts=conflicts, synergy_notes=synergies)


def render_plan(
    task: DecomposedTask,
    council_outputs: list[CouncilOutput],
    fusion_result: FusionResult,
) -> FinalPlan:
    """Produce the single FinalPlan from all pipeline outputs."""

    # ── Architecture ──
    architecture: list[str] = []
    for output in council_outputs:
        if output.perspective in (Perspective.ARCHITECTURE, Perspective.SCALABILITY):
            for rec in output.recommendations[:2]:
                if rec not in architecture:
                    architecture.append(rec)
    if not architecture:
        architecture = ["Layered architecture: API Gateway → Services → Data Layer"]

    # ── Modules (from sub-problems) ──
    modules: list[str] = []
    for i, sp in enumerate(task.sub_problems):
        modules.append(f"Module {i+1}: {sp}")
    if not modules:
        modules = [
            "Core business logic module",
            "Data persistence layer",
            "API / interface layer",
            "Infrastructure & deployment",
        ]

    # ── Data Flow ──
    arch_outputs = [o for o in council_outputs if o.perspective == Perspective.ARCHITECTURE]
    if arch_outputs and arch_outputs[0].summary:
        data_flow = [arch_outputs[0].summary]
    else:
        data_flow = ["Request → API Gateway → Service Layer → Data Store"]
    # Add pipeline details from cost/scalability
    for output in council_outputs:
        if output.perspective in (Perspective.COST, Perspective.SCALABILITY):
            for rec in output.recommendations[:1]:
                if "cache" in rec.lower() or "pipeline" in rec.lower() or "queue" in rec.lower():
                    if rec not in data_flow:
                        data_flow.append(rec)

    # ── Trade-offs ──
    tradeoffs: list[str] = []
    # From risk warnings
    for output in council_outputs:
        if output.perspective == Perspective.RISK:
            for w in output.warnings[:2]:
                tradeoffs.append(w)
    # From fusion conflicts
    tradeoffs.extend(fusion_result.conflicts)
    # From cost
    for output in council_outputs:
        if output.perspective == Perspective.COST:
            for w in output.warnings[:2]:
                if w not in tradeoffs:
                    tradeoffs.append(w)
    # Defaults
    if not tradeoffs:
        tradeoffs = [
            "Latency vs accuracy: choose based on use case criticality",
            "Cost vs quality: open-source for core, paid APIs for edge cases",
            "Simplicity vs scalability: start simple, architect for growth",
        ]

    # ── Implementation Plan ──
    implementation_plan: list[str] = []

    # Top tech choices
    top_tech = fusion_result.items[:4]
    for item in top_tech:
        if item.total > 0.7:
            implementation_plan.append(f"Adopt: {item.content}")

    # Milestones from sub-problems
    phases = ["Core MVP"] if len(task.sub_problems) <= 2 else ["Core MVP", "Secondary modules"]
    for i, sp in enumerate(task.sub_problems[:4]):
        if i < len(phases):
            implementation_plan.append(f"{phases[i]}: implement {sp[:60]}")
        else:
            implementation_plan.append(f"Phase {i+1}: implement {sp[:60]}")

    # Standard phases
    implementation_plan.append("Integration: end-to-end pipeline, integration tests")
    implementation_plan.append("Hardening: monitoring, error handling, retry logic, logging")
    implementation_plan.append("Scale: load testing, bottleneck optimization, production deploy")

    return FinalPlan(
        architecture=architecture[:5],
        modules=modules[:5],
        data_flow=data_flow[:4],
        tradeoffs=tradeoffs[:5],
        implementation_plan=implementation_plan[:6],
    )
