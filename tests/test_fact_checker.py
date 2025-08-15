from src.fact_checker import FactChecker

def test_smoke_run(monkeypatch):
    # Monkeypatch the model to avoid real API calls during tests
    class DummyLLM:
        def invoke(self, msgs):
            # return minimal content depending on the last user message
            text = msgs[-1].content.lower()
            if "preliminary" in msgs[0].content.lower():
                return type("Obj", (), {"content": "Preliminary answer (tentative)."})
            if "extract" in msgs[0].content.lower():
                return type("Obj", (), {"content": "- Assumption A\n- Assumption B"})
            if "verification" in msgs[0].content.lower():
                return type("Obj", (), {"content": "- query A\n- query B"})
            if "evidence" in msgs[0].content.lower():
                return type("Obj", (), {"content": "supported. https://example.com"})
            if "final" in msgs[0].content.lower():
                return type("Obj", (), {"content": "Verdict: True\nConfidence: 80"})
            return type("Obj", (), {"content": "ok"})
    from src import prompt_chains
    prompt_chains.load_chat_model = lambda *a, **k: DummyLLM()

    fc = FactChecker()
    res = fc.run("The capital of France is Paris")
    assert res.final_verdict in {"True", "False", "Mixed", "Uncertain"}
