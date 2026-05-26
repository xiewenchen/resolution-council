"""
Resolution Council AI — Types (Final)
Minimal, production-grade type system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ── Internal Types ────────────────────────────────────────────────────

class DeanMode(str, Enum):
    FIRST_PRINCIPLES = "first_principles"
    ENGINEERING = "engineering"
    ANALOGY = "analogy"


class Perspective(str, Enum):
    ARCHITECTURE = "architecture"
    COST = "cost"
    RISK = "risk"
    SCALABILITY = "scalability"
    INNOVATION = "innovation"


@dataclass
class DecomposedTask:
    original: str
    sub_problems: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    domain_hints: list[str] = field(default_factory=list)
    mode: DeanMode = DeanMode.ENGINEERING
    similar_patterns: list[str] = field(default_factory=list)


@dataclass
class CouncilOutput:
    perspective: Perspective
    summary: str
    recommendations: list[str] = field(default_factory=list)
    tech_choices: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    confidence: float = 0.8


@dataclass
class ScoredItem:
    content: str
    source: str
    feasibility: float = 0.0
    compatibility: float = 0.0
    cost: float = 0.0
    innovation: float = 0.0
    total: float = 0.0


@dataclass
class FusionResult:
    items: list[ScoredItem] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    synergy_notes: list[str] = field(default_factory=list)


# ── Public Output Type ────────────────────────────────────────────────

@dataclass
class FinalPlan:
    """The single deterministic output. One plan, no alternatives."""

    architecture: list[str] = field(default_factory=list)
    modules: list[str] = field(default_factory=list)
    data_flow: list[str] = field(default_factory=list)
    tradeoffs: list[str] = field(default_factory=list)
    implementation_plan: list[str] = field(default_factory=list)

    @property
    def final_plan(self) -> str:
        return self.render()

    def render(self) -> str:
        lines = [
            "=" * 64,
            "  Resolution Council AI · System Architecture Plan",
            "=" * 64,
            "",
        ]
        if self.architecture:
            lines.append("ARCHITECTURE")
            lines.append("-" * 40)
            for item in self.architecture:
                lines.append(f"  • {item}")
            lines.append("")

        if self.modules:
            lines.append("MODULES")
            lines.append("-" * 40)
            for item in self.modules:
                lines.append(f"  • {item}")
            lines.append("")

        if self.data_flow:
            lines.append("DATA FLOW")
            lines.append("-" * 40)
            for item in self.data_flow:
                lines.append(f"  • {item}")
            lines.append("")

        if self.tradeoffs:
            lines.append("TRADE-OFFS")
            lines.append("-" * 40)
            for item in self.tradeoffs:
                lines.append(f"  ⚠ {item}")
            lines.append("")

        if self.implementation_plan:
            lines.append("IMPLEMENTATION PLAN")
            lines.append("-" * 40)
            for item in self.implementation_plan:
                lines.append(f"  {item}")
            lines.append("")

        lines.append("=" * 64)
        return "\n".join(lines)
