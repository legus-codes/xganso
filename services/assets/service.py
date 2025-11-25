from pathlib import Path
from typing import Dict, List, Type

from pygame import Surface

from services.assets.core import AssetServiceConfig
from services.core import LoadingError
from utils.file_system import FileSystemProtocol, LocalFileSystem
from utils.loader import LoaderProtocol
from utils.reflection import import_class


class AssetService:
    
    def __init__(self, loader: Type[LoaderProtocol], file_provider: Type[FileSystemProtocol], search_path = str | Path):
        self.assets: Dict[str, Surface] = {}
        self.asset_paths: Dict[str, Path] = {}
        self.loader = loader
        self.file_provider = file_provider
        self.search_path = Path(search_path)

    def scan(self) -> List[LoadingError]:
        errors = []
        for filepath in self.file_provider.glob(self.search_path, '*.png'):
            try:
                identifier = self._get_identifier(filepath)
                self.asset_paths[identifier] = filepath
            except ValueError as ve:
                errors.append(LoadingError(filename=filepath.as_posix(), message=str(ve)))

        if errors:
            self._clear()
        return errors

    def load_all(self) -> None:
        for identifier, filepath in self.asset_paths.items():
            self.assets[identifier] = self.loader.load_file(filepath)

    def reload_all(self) -> List[LoadingError]:
        self._clear()
        errors = self.scan()
        self.load_all()
        return errors

    def get(self, identifier: str) -> Surface | None:
        return self.assets.get(identifier, None)

    def get_keys(self) -> List[str]:
        return list(self.assets.keys())

    def _get_identifier(self, path: Path) -> str:
        return path.relative_to(self.search_path).with_suffix('').as_posix()

    def _clear(self) -> None:
        self.asset_paths.clear()
        self.assets.clear()



class AssetServiceFactory:
    
    @staticmethod
    def build(asset_service_config: AssetServiceConfig) -> AssetService:
        loader_cls = import_class(asset_service_config.data_loader)
        return AssetService(loader_cls, LocalFileSystem, asset_service_config.search_path)
