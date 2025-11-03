from pathlib import Path
from typing import Any, List, Protocol

import yaml


class RepositoryProtocol(Protocol):

    def load(self) -> List[Any]:
        ...


class YamlRepository(RepositoryProtocol):

    def __init__(self, path: Path, pattern: str='*.yaml'):
        self.path = path
        self.pattern = pattern

    def load(self) -> List[Any]:
        data = []
        for yaml_file in self.path.glob(self.pattern):
            data.append(self._load_file(yaml_file))
        return data

    def _load_file(self, filepath: Path) -> Any:
        with open(filepath) as yaml_file:
            return yaml.safe_load(yaml_file)
