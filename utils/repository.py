from pathlib import Path
from typing import Any, Dict, Protocol

import yaml


class RepositoryProtocol(Protocol):

    def load_file(self, filepath: Path) -> Any:
        ...

    def load_all(self, path: Path) -> Dict[str, Any]:
        ...


class YamlRepository(RepositoryProtocol):

    def __init__(self, pattern: str='*.yaml'):
        self.pattern = pattern

    def load_file(self, filepath: Path) -> Any:
        with open(filepath) as yaml_file:
            return yaml.safe_load(yaml_file)

    def load_all(self, path: Path) -> Dict[str, Any]:
        data = {}
        for yaml_file in path.glob(self.pattern):
            data[yaml_file.name] = self.load_file(yaml_file)
        return data
