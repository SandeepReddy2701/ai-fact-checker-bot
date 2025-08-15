from __future__ import annotations
from typing import List, Dict, Any
from urllib.parse import urlparse
from dataclasses import dataclass
import re
import math
import datetime as dt

TRUSTED_DOMAINS = {
    "who.int": 95, "un.org": 90, "oecd.org": 85, "nature.com": 90, "science.org": 90,
    "ft.com": 80, "bbc.com": 80, "nytimes.com": 80, "reuters.com": 85, "apnews.com": 85,
    "nasa.gov": 95, "noaa.gov": 90, "esa.int": 90, "ec.europa.eu": 85, "census.gov": 85
}

def extract_domain(url: str) -> str:
    try:
        netloc = urlparse(url).netloc.lower()
        # strip subdomains to 2nd-level (rough heuristic)
        parts = netloc.split(".")
        if len(parts) >= 2:
            return ".".join(parts[-2:])
        return netloc
    except Exception:
        return ""

def credibility_score(url: str, date: str | None = None) -> int:
    domain = extract_domain(url)
    base = TRUSTED_DOMAINS.get(domain, 60)
    # recency boost (up to +10 within ~18 months)
    if date:
        try:
            # try a few date formats
            for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d %b %Y", "%b %d, %Y"):
                try:
                    d = dt.datetime.strptime(date, fmt)
                    break
                except Exception:
                    d = None
            if d:
                delta_days = (dt.datetime.utcnow() - d).days
                recency = max(0, 10 - delta_days / 55)  # ~ +10 if extremely recent
                base += int(recency)
        except Exception:
            pass
    return max(0, min(100, base))

def simple_confidence(verdicts: List[str]) -> int:
    # crude mapping: more 'supported' -> higher confidence
    score_map = {"supported": 90, "contradicted": 10, "uncertain": 40}
    if not verdicts:
        return 30
    avg = sum(score_map.get(v, 40) for v in verdicts) / len(verdicts)
    return int(avg)

