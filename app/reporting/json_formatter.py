import json

def format_pretty_json(data: dict) -> str:
    return json.dumps(data, indent=4, sort_keys=True)