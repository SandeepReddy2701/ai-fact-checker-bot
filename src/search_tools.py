from __future__ import annotations
from duckduckgo_search import DDGS
from typing import List, Dict, Any
from dataclasses import dataclass
import time

@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    date: str | None = None

def web_search(query: str, region: str = "wt-wt", max_results: int = 8) -> List[SearchResult]:
    results: List[SearchResult] = []
    with DDGS() as ddgs:
        # Safe search off by default; you can change per your needs
        for r in ddgs.text(query, region=region, max_results=max_results):
            results.append(SearchResult(
                title=r.get("title") or "",
                url=r.get("href") or r.get("url") or "",
                snippet=r.get("body") or r.get("snippet") or "",
                date=r.get("date")
            ))
            time.sleep(0.05)  # gentle pacing to avoid rate limits
    return results
