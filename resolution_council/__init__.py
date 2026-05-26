"""
Resolution Council AI
A minimal AI system design compiler.

Usage:
    >>> from resolution_council import ResolutionCouncil
    >>> plan = ResolutionCouncil().resolve("build a real-time translation system")
    >>> print(plan.final_plan)
"""

from .dean import analyze
from .council import deliberate
from .fusion import fuse, render_plan
from .types import FinalPlan


class ResolutionCouncil:
    """Single-entry API. Natural language → structured architecture.

    Pipeline: DEAN → COUNCIL → FUSION → FinalPlan
    """

    def resolve(self, task: str, verbose: bool = False) -> FinalPlan:
        """Convert a natural language requirement into a system architecture plan.

        Returns a FinalPlan with architecture, modules, data flow,
        trade-offs, and implementation plan.
        """
        if verbose:
            print(f"  [DEAN]   analyzing: {task[:60]}...")
        decomposed = analyze(task)

        if verbose:
            print(f"  [DEAN]   mode: {decomposed.mode.value}")
            print(f"  [DEAN]   sub-problems: {len(decomposed.sub_problems)}")
            for sp in decomposed.sub_problems:
                print(f"           • {sp[:80]}")

        if verbose:
            print(f"  [COUNCIL] generating 5 perspectives...")
        perspectives = deliberate(decomposed)

        if verbose:
            for p in perspectives:
                print(f"           [{p.perspective.value}] {p.summary[:60]}...")

        if verbose:
            print(f"  [FUSION]  scoring, ranking, resolving conflicts...")
        fused = fuse(perspectives, decomposed)

        if verbose:
            print(f"  [FUSION]  {len(fused.items)} items ranked")
            if fused.conflicts:
                print(f"  [FUSION]  {len(fused.conflicts)} conflicts resolved")

        plan = render_plan(decomposed, perspectives, fused)
        return plan


__all__ = ["ResolutionCouncil", "FinalPlan"]
