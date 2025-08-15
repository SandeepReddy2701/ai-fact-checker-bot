from __future__ import annotations
from typing import List, Dict, Any, Optional
import yaml
from pathlib import Path

# Gemini model loader
def load_chat_model(model_name: str, temperature: float = 0.2):
    import google.generativeai as genai
    import os

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables")

    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    class GeminiWrapper:
        def invoke(self, msgs):
            # msgs is a list of SystemMessage and HumanMessage
            # We join all message contents with blank lines
            full_prompt = "\n\n".join(m.content for m in msgs)
            resp = model.generate_content(
                full_prompt,
                generation_config={"temperature": temperature}
            )
            return type("Obj", (), {"content": resp.text})

    return GeminiWrapper()

def load_prompts(path: str) -> Dict[str, str]:
    """Load prompt templates from a YAML file."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    assert isinstance(data, dict), "prompts.yaml must be a mapping"
    return data  # keys like 'initial_response', ...

def run_llm(llm, system: str, user: str) -> str:
    """Run an LLM with system + human prompts."""
    from langchain.schema import SystemMessage, HumanMessage
    msgs = [SystemMessage(content=system), HumanMessage(content=user)]
    out = llm.invoke(msgs)
    return out.content if hasattr(out, "content") else str(out)
