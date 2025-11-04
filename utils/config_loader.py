from pathlib import Path
from typing import Generic, Type, TypeVar
from utils.repository import RepositoryProtocol


T = TypeVar("T")


class ConfigLoader(Generic[T]):

    def __init__(self, repository: RepositoryProtocol):
        self.repository = repository

    def load_config(self, config_path: str | Path, config_model: Type[T]) -> T:
        data = self.repository.load_file(Path(config_path))
        return config_model(**data)
