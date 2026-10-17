# Multi-Agent AI Research Assistant

An offline, evidence-grounded research assistant prototype built with **Python** and **Streamlit**. It coordinates four simple, transparent agents to search user-provided notes, summarize matching passages, check whether supporting passages were found, and produce a Markdown report.

> **Important:** This is an extractive, keyword-based prototype. It is **not** powered by a large language model (LLM), does not browse the internet, and cannot independently verify scientific claims.

## Features

- Upload multiple UTF-8 `.txt` research notes.
- Optionally include bundled demo notes.
- **Search Agent:** ranks relevant sentences using token overlap.
- **Summary Agent:** assembles a short source-attributed extractive summary.
- **Verification Agent:** reports whether matching passages were found (not independent fact-checking).
- **Report Agent:** creates a structured, downloadable Markdown research report.

## Project structure

```text
.
├── app.py
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── agents/
│   ├── __init__.py
│   └── core.py
├── data/
│   ├── agent_notes.txt
│   └── rag_notes.txt
└── tests/
    └── test_core.py
```

## Installation

Requires Python 3.10 or later.

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

In the app, leave **Include demo research notes** enabled or upload your own UTF-8 `.txt` documents, enter a research question, and click **Run research agents**.

## Run tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

## Limitations

This application retrieves text from local files using lexical similarity. It does not generate new explanations with an LLM, access academic databases, assess the truth of scientific statements, or guarantee complete retrieval. Review the original publications before citing any claims.

## License

See the `LICENSE` file in this repository.
