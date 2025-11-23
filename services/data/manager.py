from pathlib import Path
from typing import Dict, List, Type
from pydantic import ValidationError

from services.core import LoadingError
from services.data.core import DataManagerConfig, DataManagerProtocol
from services.data.models import DataDescription
from utils.file_system import FileSystemProtocol
from utils.reflection import import_class
from utils.loader import LoaderProtocol


class DataManager(DataManagerProtocol):

    def __init__(self, data_model: Type[DataDescription], data_loader: Type[LoaderProtocol], file_provider: Type[FileSystemProtocol], search_path: str | Path):
        self.data: Dict[str, DataDescription] = {}
        self.data_model = data_model
        self.data_loader = data_loader
        self.file_provider = file_provider
        self.search_path = Path(search_path)

    def load(self) -> List[LoadingError]:
        errors = []
        for filepath in self.file_provider.glob(self.search_path, '*.yaml'):
            unit_data = self.data_loader.load_file(filepath)
            try:
                unit = self.data_model(**unit_data)
                if unit.identity.id in self.data:
                    errors.append(LoadingError(filename=str(filepath), message=f'Unit with {unit.identity.id} already registered'))
                    continue
                self.data[unit.identity.id] = unit
            except ValidationError as ve:
                errors.append(LoadingError(filename=str(filepath), message=str(ve)))

        if errors:
            self._clear()
        return errors

    def reload(self) -> List[LoadingError]:
        self._clear()
        return self.load()

    def get(self, identifier: str) -> DataDescription | None:
        return self.data.get(identifier, None)

    def _clear(self) -> None:
        self.data.clear()


class DataManagerFactory:
    
    @staticmethod
    def build(data_manager_config: DataManagerConfig) -> DataManager:
        model_cls = import_class(data_manager_config.data_model)
        loader_cls = import_class(data_manager_config.data_loader)
        file_cls = import_class(data_manager_config.file_provider)
        return DataManager(model_cls, loader_cls, file_cls, data_manager_config.search_path)
