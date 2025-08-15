from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass
class Settings:
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    temperature: float = float(os.getenv("TEMPERATURE", "0.2"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "800"))
            search_k: int = int(os.getenv("SEARCH_K", "8"))
    search_region: str = os.getenv("SEARCH_REGION", "wt-wt")

settings = Settings()
