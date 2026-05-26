#!/usr/bin/env python3
"""
Resolution Council AI — Demo
3 cases. Each: architecture, trade-offs, implementation plan.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resolution_council import ResolutionCouncil

CASES = [
    "Build a real-time translation system with Chinese/English support, "
    "sub-500ms latency, offline capable, with synchronized subtitles",

    "Design an AI coding assistant that understands project context, "
    "generates code, runs tests, and self-corrects errors",

    "Create a distributed task scheduling system with priority queues, "
    "failure recovery, worker pools, and real-time monitoring dashboard",
]


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Resolution Council AI — System Design Compiler"
    )
    parser.add_argument("task", nargs="?", help="Custom task description")
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()

    council = ResolutionCouncil()

    if args.task:
        t0 = time.time()
        plan = council.resolve(args.task, verbose=not args.quiet)
        elapsed = time.time() - t0
        print(plan.final_plan)
        print(f"\n  Generated in {elapsed:.3f}s")
        return

    # Default: run all 3 cases
    print("  Resolution Council AI")
    print("  System Design Compiler — 3 cases")
    print()

    for i, case in enumerate(CASES, 1):
        label = [
            "REAL-TIME TRANSLATION",
            "AI CODING ASSISTANT",
            "DISTRIBUTED TASK SYSTEM",
        ][i - 1]

        t0 = time.time()
        plan = council.resolve(case, verbose=False)
        elapsed = time.time() - t0

        print(f"  Case {i}: {label}")
        print(f"  {'─' * 50}")
        print(plan.final_plan)
        print()

    print(f"  3 architectures. Zero dependencies. pip install resolution-council")


if __name__ == "__main__":
    main()
