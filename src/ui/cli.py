from __future__ import annotations
import argparse, json
from ..fact_checker import FactChecker

def main():
    p = argparse.ArgumentParser(description="AI Fact-Checker CLI")
    p.add_argument("claim", help="Claim or question to fact-check", nargs="+")
    args = p.parse_args()
    claim = " ".join(args.claim)
    fc = FactChecker()
    result = fc.run(claim)
    print("\n=== PRELIMINARY ===\n", result.preliminary)
    print("\n=== ASSUMPTIONS ===")
    for a in result.assumptions:
        print("-", a)
    print("\n=== CHECKS ===")
    for c in result.checks:
        print(f"* {c.assumption}\n  verdict={c.verdict}\n  cites={[e['url'] for e in c.evidence]}")
    print("\n=== FINAL SYNTHESIS ===\n", result.synthesis)
    print(f"\nVerdict: {result.final_verdict} | Confidence: {result.confidence}")

if __name__ == "__main__":
    main()
