import streamlit as st
from fact_checker import FactChecker

st.set_page_config(page_title="AI Fact-Checker", page_icon="✅", layout="wide")
st.title("AI Fact-Checker Bot")

if "fc" not in st.session_state:
    st.session_state.fc = FactChecker()

claim = st.text_input("Enter a claim to fact-check:", "The capital of France is Paris.")
if st.button("Check"):
    with st.spinner("Fact-checking..."):
        res = st.session_state.fc.run(claim)
    st.subheader("Preliminary")
    st.write(res.preliminary)
    st.subheader("Assumptions")
    for a in res.assumptions:
        st.markdown(f"- {a}")
    st.subheader("Checks")
    for c in res.checks:
        with st.expander(c.assumption):
            st.write(f"**Verdict:** {c.verdict}")
            st.write(c.rationale)
            for e in c.evidence:
                st.write(f"- [{e['title']}]({e['url']})")
    st.subheader("Final Synthesis")
    st.write(res.synthesis)
    st.success(f"Verdict: {res.final_verdict} | Confidence: {res.confidence}")
