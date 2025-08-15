from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple
from .prompt_chains import load_chat_model, load_prompts, run_llm
from .search_tools import web_search, SearchResult
from .utils import credibility_score, simple_confidence
from config.settings import settings
import json
import pathlib

@dataclass
class AssumptionCheck:
    assumption: str
    verdict: str  # supported/contradicted/uncertain
    evidence: List[Dict[str, str]]  # {title,url,snippet}
    rationale: str

@dataclass
class FactCheckResult:
    preliminary: str
    assumptions: List[str]
    checks: List[AssumptionCheck]
    final_verdict: str
    confidence: int
    synthesis: str

class FactChecker:
    def __init__(self, model_name: str | None = None, temperature: float | None = None):
        self.prompts = load_prompts(str(pathlib.Path("config/prompts.yaml")))
        self.llm = load_chat_model(model_name or settings.model_name, temperature or settings.temperature)

    def initial_response(self, claim: str) -> str:
        sys = self.prompts["initial_response"]
        return run_llm(self.llm, sys, claim)

    def extract_assumptions(self, claim: str, preliminary: str) -> List[str]:
        sys = self.prompts["assumption_extraction"]
        text = f"CLAIM:\n{claim}\n\nPRELIMINARY:\n{preliminary}"
        out = run_llm(self.llm, sys, text)
        # grab bullets
        lines = [l.strip("-• ").strip() for l in out.splitlines() if l.strip()]
        return [l for l in lines if len(l) > 3]

    def plan_verification(self, assumption: str) -> List[str]:
        sys = self.prompts["verification_planner"]
        out = run_llm(self.llm, sys, assumption)
        qs = [l.strip("-• ").strip() for l in out.splitlines() if l.strip()]
        return [q for q in qs if len(q) > 3][:3]

    def check_assumption(self, assumption: str) -> AssumptionCheck:
        queries = self.plan_verification(assumption)
        all_results: List[SearchResult] = []
        for q in queries:
            all_results.extend(web_search(q, region=settings.search_region, max_results=settings.search_k//len(queries) or 3))
        # sort by crude credibility
        ranked = sorted(all_results, key=lambda r: credibility_score(r.url, r.date), reverse=True)[:6]
        # build a compact block for the LLM
        packed = "\n".join([f"- {r.title}\n  {r.url}\n  {r.snippet}\n  date={r.date}" for r in ranked])
        sys = self.prompts["evidence_synthesis"]
        out = run_llm(self.llm, sys, f"ASSUMPTION: {assumption}\n\nEVIDENCE:\n{packed}")
        # naive parse: look for cited URLs within the text
        import re
        urls = re.findall(r"https?://\S+", out)
        evidence = []
        for r in ranked:
            if any(r.url.startswith(u.rstrip(').,;')) for u in urls):
                evidence.append({"title": r.title, "url": r.url, "snippet": r.snippet})
            if len(evidence) >= 3:
                break
        # infer verdict keyword
        v = "uncertain"
        low = out.lower()
        if "supported" in low or "support" in low:
            v = "supported"
        if "contradict" in low or "refute" in low or "false" in low:
            v = "contradicted"
        return AssumptionCheck(assumption=assumption, verdict=v, evidence=evidence, rationale=out.strip())

    def final_synthesis(self, claim: str, checks: List[AssumptionCheck]) -> Tuple[str, int, str]:
        sys = self.prompts["final_synthesis"]
        # map to simple overall verdict
        votes = {"supported": 0, "contradicted": 0, "uncertain": 0}
        for c in checks:
            votes[c.verdict] = votes.get(c.verdict, 0) + 1
        if votes["contradicted"] > votes["supported"]:
            overall = "False"
        elif votes["supported"] > 0 and votes["contradicted"] == 0:
            overall = "True"
        elif votes["supported"] > 0 and votes["contradicted"] > 0:
            overall = "Mixed"
        else:
            overall = "Uncertain"
        conf = simple_confidence([c.verdict for c in checks])
        body = []
        for c in checks:
            cites = ", ".join(e["url"] for e in c.evidence[:3]) or "No strong citations found"
            body.append(f"- {c.assumption}\n  Verdict: {c.verdict}\n  Cites: {cites}")
        packed = "\n".join(body)
        out = run_llm(self.llm, sys, f"CLAIM: {claim}\n\nASSUMPTION VERDICTS:\n{packed}\n\nOVERALL SUGGESTED VERDICT: {overall}\nSUGGESTED CONFIDENCE: {conf}")
        # try to pull final verdict & confidence from the model output
        return overall, conf, out.strip()

    def run(self, claim: str) -> FactCheckResult:
        prelim = self.initial_response(claim)
        assumptions = self.extract_assumptions(claim, prelim)[:6]
        checks = [self.check_assumption(a) for a in assumptions]
        overall, conf, synthesis = self.final_synthesis(claim, checks)
        return FactCheckResult(
            preliminary=prelim,
            assumptions=assumptions,
            checks=checks,
            final_verdict=overall,
            confidence=conf,
            synthesis=synthesis
        )
