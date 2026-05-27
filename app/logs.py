import json
import secrets
from pathlib import Path
from datetime import datetime


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def log_interaction(question, answer, model_name="mistral:latest", source="streamlit"):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": "docs_agent_ollama",
        "model": model_name,
        "source": source,
        "question": question,
        "answer": answer,
        "tool_used": "search"
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    rand_hex = secrets.token_hex(3)

    filename = f"docs_agent_ollama_{ts}_{rand_hex}.json"
    filepath = LOG_DIR / filename

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

    return filepath
