import re
from typing import Any, Dict, List

DANGEROUS_SQL_PATTERN = re.compile(r"(;|--|\b(drop|select|insert|update|delete|alter|create)\b)", re.IGNORECASE)

def sanitize_filters(params: Dict[str, Any], strict_sql: bool = False) -> Dict[str, Any]:
    sanitized = {}

    for key, value in params.items():
        if value is None:
            continue

        def is_safe(val: str) -> bool:
            return not DANGEROUS_SQL_PATTERN.search(val)

        if isinstance(value, list):
            cleaned = []
            for item in value:
                if isinstance(item, str):
                    item = item.strip()
                    if item and (not strict_sql or is_safe(item)):
                        cleaned.append(item)
                elif isinstance(item, (int, float, bool)):
                    cleaned.append(item)
            if cleaned:
                sanitized[key] = cleaned
        elif isinstance(value, str):
            value = value.strip()
            if value and (not strict_sql or is_safe(value)):
                sanitized[key] = value
        elif isinstance(value, (int, float, bool)):
            sanitized[key] = value

    return sanitized
