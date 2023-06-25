import json
from pathlib import Path


def get_resource(current_path: Path, file_name: str) -> dict:
    with open(current_path / 'resources' / file_name) as file:
        return json.load(file)


def get_resource_absolute_path(current_path: Path, file_name: str) -> str:
    return f'{current_path}/resources/{file_name}'
