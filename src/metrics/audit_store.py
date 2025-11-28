# metrics/audit_store.py
import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("data/audit_log.jsonl")
LOG_FILE.parent.mkdir(exist_ok=True)

def save_audit_log(entry: dict):
    entry["saved_at"] = datetime.now().isoformat()
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
