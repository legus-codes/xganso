from pathlib import Path
from typing import Generic, Type, TypeVar
from utils.loader import LoaderProtocol


T = TypeVar("T")


class ConfigLoader(Generic[T]):

    def __init__(self, loader: Type[LoaderProtocol]):
        self.loader = loader

    def load_config(self, config_path: str | Path, config_model: Type[T]) -> T:
        data = self.loader.load_file(Path(config_path))
        return config_model(**data)
