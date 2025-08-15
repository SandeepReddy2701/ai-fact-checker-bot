import gradio as gr
from ..fact_checker import FactChecker

fc = FactChecker()

def check(claim: str):
    res = fc.run(claim)
    lines = [
        "### Preliminary", res.preliminary, 
        "\n### Assumptions"
    ] + [f"- {a}" for a in res.assumptions]
    lines += ["\n### Checks"]
    for c in res.checks:
        cites = "\n".join([f"- {e['title']} ({e['url']})" for e in c.evidence])
        lines += [f"**{c.assumption}**\nVerdict: {c.verdict}\n{c.rationale}\n{cites}"]
    lines += ["\n### Final Synthesis", res.synthesis, f"**Verdict:** {res.final_verdict} | **Confidence:** {res.confidence}"]
    return "\n\n".join(lines)

demo = gr.Interface(fn=check, inputs=gr.Textbox(lines=2, label="Claim"), outputs="markdown", title="AI Fact-Checker Bot")
if __name__ == "__main__":
    demo.launch()
