# Agentic AI for Public Transit Reliability and Equity

**AI agents sense, organize and explain; fixed, published rules score; people decide.**

A prototype decision-support system for bus disruptions near Newark Penn Station. Live transit, census and weather data
and computer-vision rider counts feed a deterministic scoring engine (confidence, impact R/V/A/P, significance and a
priority-adjusted option ranking). People make every decision: a first reviewer, an independent second reviewer for
high-impact actions, operations staff and a policy owner. Ethics-training (Section C) and conflict-of-interest
(Section D) gates protect each review. Language-model text never enters a score, a routing decision or an approval.

> **Prototype only.** Not connected to live operations: approved actions are recorded, not dispatched. The transit
> network is synthetic (fictional routes drawn over a real Newark basemap).

## What's in this repository

| Path | What it is |
|---|---|
| `notebooks/Transit_Agentic_AI_Submission_v5_with_evaluation.ipynb` | The full notebook (Colab): every section, the scenario gallery, the evaluation (V1–V11) and the Gradio dashboard. **Source of truth.** |
| `streamlit_app.py` | Streamlit version of the dashboard, for Streamlit Community Cloud. |
| `transit_ai/engine.py` | The notebook's engine code as a Python module (generated; do not edit by hand). |
| `tools/build_engine.py` | Regenerates `transit_ai/engine.py` from the notebook. |
| `requirements.txt` | Packages for the Streamlit app. `requirements-notebook.txt` adds what the notebook needs locally. |
| `.streamlit/secrets.toml.example` | Template for API keys. |

## Run the notebook (Google Colab)

1. Open the notebook in Colab (`File → Upload notebook`, or `File → Open notebook → GitHub` once this repo is pushed).
2. Optional: add keys in the **🔑 Secrets** panel (see the table below) and turn on notebook access for each.
3. `Runtime → Restart session and run all`.

## Run the Streamlit app locally

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # optional: add keys
streamlit run streamlit_app.py
```

The first load takes about 30 seconds: the app runs the notebook's setup once (live connectors, computer vision,
the 15-case scenario gallery and the evaluation).

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repository (public, or private with Streamlit access granted).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **Create app** → **Deploy a public app from GitHub**.
3. Repository: your repo · Branch: `main` · Main file path: `streamlit_app.py`.
4. **Advanced settings** → Python version **3.12**. Paste any keys from `.streamlit/secrets.toml.example` into
   **Secrets** (TOML format). All keys are optional.
5. **Deploy**.

## API keys (all optional)

| Key | Used for | Without it |
|---|---|---|
| `OPENAI_API_KEY` | Default LLM provider (narratives, notes) | OpenRouter / Hugging Face, then template text |
| `OPENROUTER_API_KEY` | LLM fallback 1 | skipped |
| `HF_API_KEY` (or `HF_TOKEN`) | LLM fallback 2 | skipped |
| `NJ_TRANSIT_USERNAME`, `NJ_TRANSIT_PASSWORD` | NJ Transit GTFS-realtime | documented sample data |
| `CENSUS_API_KEY` | US Census ACS | works without, at lower rate limits |
| `NWS_CONTACT_EMAIL` | Identifies the project to the National Weather Service | generic user agent |

Keys are read from Colab Secrets, Streamlit secrets or environment variables, and are never printed or saved.

## Notes on the hosted app

- **One shared demo state.** Everyone who opens the app sees the same cases and decisions (as with the notebook's
  dashboard). Use **Reset demo** in the sidebar to start over.
- **Lighter models.** The app leaves out PyTorch and Transformers to fit Streamlit Community Cloud's memory, so computer
  vision uses the OpenCV HOG fallback detector (expect V6 counting checks to fail) and the FLAN-T5 small language model
  in Section A is skipped. The notebook in Colab uses both.
- Outputs (CSV, JSON, map) can be downloaded from the **Audit & export** tab.

## Changing the code

Edit the notebook, then regenerate the module the app imports:

```bash
python tools/build_engine.py
```

## Data sources and credits

NJ Transit GTFS-realtime · US Census Bureau ACS 5-year · National Weather Service API · sample imagery downloaded at run
time: `bus.jpg` (Ultralytics assets, AGPL-3.0) and `vtest.avi` (OpenCV samples). Only anonymized counts are kept.
