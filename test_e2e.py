"""Tests for Resolution Council AI — Final."""
from resolution_council import ResolutionCouncil, FinalPlan
from resolution_council.dean import analyze, DeanMode
from resolution_council.council import deliberate
from resolution_council.fusion import fuse, render_plan


def test_dean():
    # Known → Engineering/Analogy
    r = analyze("build a real-time translation system with subtitles")
    assert r.mode in (DeanMode.ENGINEERING, DeanMode.ANALOGY)
    assert len(r.sub_problems) > 0

    # Novel → First Principles
    r = analyze("design an unprecedented quantum computing recommendation engine")
    assert r.mode == DeanMode.FIRST_PRINCIPLES

    print("PASS: DEAN modes")


def test_council():
    task = analyze("build a real-time translation system")
    outputs = deliberate(task)
    assert len(outputs) == 5
    perspectives = {o.perspective.value for o in outputs}
    assert perspectives == {"architecture", "cost", "risk", "scalability", "innovation"}
    for o in outputs:
        assert o.confidence > 0
    print("PASS: COUNCIL 5 perspectives")


def test_fusion():
    task = analyze("build a real-time translation system")
    outputs = deliberate(task)
    result = fuse(outputs, task)
    assert len(result.items) > 0
    scores = [i.total for i in result.items]
    assert scores == sorted(scores, reverse=True)
    print(f"PASS: FUSION — {len(result.items)} items ranked")


def test_pipeline():
    council = ResolutionCouncil()

    # Case 1: Translation
    plan = council.resolve("build a real-time translation system", verbose=False)
    assert isinstance(plan, FinalPlan)
    assert len(plan.architecture) > 0
    assert len(plan.modules) > 0
    assert len(plan.tradeoffs) > 0
    assert len(plan.implementation_plan) > 0

    # Case 2: AI assistant
    plan = council.resolve("design an AI coding assistant", verbose=False)
    assert any("llm" in t.lower() or "agent" in t.lower() for t in plan.modules)

    # Case 3: Distributed (no AI leak)
    plan = council.resolve("create a distributed task scheduling system", verbose=False)
    tradeoff_text = " ".join(plan.tradeoffs).lower()
    assert "prompt injection" not in tradeoff_text
    assert "hallucination" not in tradeoff_text

    print("PASS: Full pipeline — 3 cases, no AI leak")


def test_render():
    plan = ResolutionCouncil().resolve("build a translation system", verbose=False)
    rendered = plan.render()
    assert "ARCHITECTURE" in rendered
    assert "MODULES" in rendered
    assert "DATA FLOW" in rendered
    assert "TRADE-OFFS" in rendered
    assert "IMPLEMENTATION PLAN" in rendered
    assert plan.final_plan == plan.render()
    print("PASS: Render format + final_plan property")


if __name__ == "__main__":
    test_dean()
    test_council()
    test_fusion()
    test_pipeline()
    test_render()
    print("\nAll 5 tests passed!")
