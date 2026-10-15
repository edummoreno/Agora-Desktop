"""Optional messages attached to successful submissions."""

import json
import os

MAX_CONFIG_BYTES: int = 1024 * 1024

def message_for(package_name: str) -> dict[str, str] | None:
    path = os.environ.get("AGORA_SUBMISSION_MESSAGES")
    if not path or not isinstance(package_name, str) or not package_name:
        return None
    
    try:
        with open(path, "rb") as stream:
            raw: bytes = stream.read(MAX_CONFIG_BYTES + 1)

        if len(raw) > MAX_CONFIG_BYTES:
            return None
        
        config: dict = json.loads(raw)

        message = config.get(package_name) if isinstance(config, dict) else None
        if not isinstance(message, dict):
            return None
        
        result: dict[str, str] = {}

        for key, limit in (("id", 128), ("title", 200), ("body", 8000)):
            value = message.get(key)
            if not isinstance(value, str):
                return None

            stripped_val = value.strip()
            if not stripped_val or len(stripped_val) > limit:
                return None
            
            result[key] = stripped_val

        button = message.get("buttonText")
        if isinstance(button, str):

            stripped_btn = button.strip()
            if 0 < len(stripped_btn) <= 80:
                result["buttonText"] = stripped_btn

        return result
    
    except (OSError, ValueError, UnicodeError):
        return None
    