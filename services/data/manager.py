from pathlib import Path
from typing import Dict, List, Type
from pydantic import ValidationError

from services.data.core import DataManagerConfig, DataManagerError, DataManagerProtocol
from services.data.models import DataDescription
from utils.reflection import import_class
from utils.repository import RepositoryProtocol


class DataManager(DataManagerProtocol):

    def __init__(self, data_model: Type[DataDescription], repository: RepositoryProtocol, path = str | Path):
        self.data: Dict[str, DataDescription] = {}
        self.data_model = data_model
        self.repository = repository
        self.path = Path(path)

    def load(self) -> List[DataManagerError]:
        errors = []
        for filename, unit_data in self.repository.load_all(self.path).items():
            try:
                unit = self.data_model(**unit_data)
                if unit.id in self.data:
                    errors.append(DataManagerError(filename, f'Unit with {unit.id} already registered'))
                    continue
                self.data[unit.id] = unit
            except ValidationError as ve:
                errors.append(DataManagerError(filename, str(ve)))

        if errors:
            self._clear()
        return errors

    def reload(self) -> List[DataManagerError]:
        self._clear()
        return self.load()

    def get(self, identifier: str) -> DataDescription | None:
        return self.data.get(identifier, None)

    def _clear(self) -> None:
        self.data.clear()


class DataManagerFactory:
    
    @staticmethod
    def build(data_manager_config: DataManagerConfig) -> DataManager:
        model_cls = import_class(data_manager_config.model)
        repo_cls = import_class(data_manager_config.repository)
        return DataManager(model_cls, repo_cls(), data_manager_config.data_path)
