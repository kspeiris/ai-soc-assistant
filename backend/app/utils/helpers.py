import re
from datetime import datetime, timedelta

def extract_ip(text: str) -> str | None:
    pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def parse_timestamp(ts_str: str) -> datetime:
    # Supports multiple formats
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(ts_str, fmt)
        except ValueError:
            continue
    return datetime.utcnow()

def severity_score(severity: str) -> int:
    return {"low": 1, "medium": 3, "high": 5, "critical": 7}.get(severity, 0)