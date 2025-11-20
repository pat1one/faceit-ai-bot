import json
import logging
import os
import threading
from typing import Any, Dict

from ..config.settings import settings

logger = logging.getLogger(__name__)

_lock = threading.Lock()

AI_SAMPLES_DIR = getattr(settings, "AI_SAMPLES_DIR", "data")
AI_SAMPLES_FILENAME = "ai_samples.jsonl"


def append_sample(record: Dict[str, Any]) -> None:
    """Append a single AI training sample to a local JSONL file.

    Each line is a standalone JSON object with at least keys:
    - task: str
    - language: str
    - input: dict
    - output: any (string or structured JSON)
    """
    try:
        os.makedirs(AI_SAMPLES_DIR, exist_ok=True)
        path = os.path.join(AI_SAMPLES_DIR, AI_SAMPLES_FILENAME)
        line = json.dumps(record, ensure_ascii=False, default=str)

        with _lock:
            with open(path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
    except Exception:
        # Never break main flow because of logging issues
        logger.exception("Failed to append AI sample to JSONL store")
