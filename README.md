# AI Fact-Checker Bot

<img width="1117" height="512" alt="Ai fact check bot png1" src="https://github.com/user-attachments/assets/f602d256-c51a-4ca5-93a8-ad3498979de6" />


<img width="1077" height="636" alt="Ai fact check bot" src="https://github.com/user-attachments/assets/efbf16d1-26da-4548-9f83-a83f3408a210" />

<img width="1065" height="481" alt="Ai fact check bot png2" src="https://github.com/user-attachments/assets/de895a2f-3bf8-4ff4-b520-e26cb3c74a3f" />


<img width="1043" height="220" alt="Ai fact check bot png2 png3" src="https://github.com/user-attachments/assets/27dac0c5-ebea-481f-b36b-248f24883743" />



A reference implementation that follows the project brief. It uses LangChain for prompt chaining, DuckDuckGo for search, and provides Streamlit, Gradio, and CLI interfaces.

## Features
- Prompt chain: preliminary → assumptions → verification (search) → evidence synthesis → final answer
- Web search via `duckduckgo-search`
- Source credibility heuristic (domain + recency)
- Claim classification & confidence folded into final synthesis
- Streamlit, Gradio, and CLI UIs
- Tests and modular structure

## Setup
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
cp .env.example .env  # add your keys
```

## Run (CLI)
```bash
python main.py "The capital of France is Paris."
```

## Run (Streamlit)
```bash
streamlit run src/ui/streamlit_app.py
```

## Run (Gradio)
```bash
python src/ui/gradio_app.py
```

## Project Structure
See folders in `fact_checker_bot/` (src, config, tests, examples).

## Notes
- Uses `langchain-openai` when available; falls back to older import path.
- Search results are heuristically ranked before being passed to the model.
- Tests include a dummy model to avoid API calls.

