from typing import Dict

from services.data.core import DataManagerProtocol, DataType
from services.data.data_models import DataDescription
from services.data.registry import get_registered_data_managers
from utils.repository import RepositoryProtocol


class DataService:

    def __init__(self, repositories: Dict[DataType, RepositoryProtocol]):
        self.data_managers: Dict[DataType, DataManagerProtocol] = {}
        for data_type, type_class in get_registered_data_managers().items():
            repository = repositories.get(data_type, None)
            if repository is None:
                raise ValueError(f'Repository for data type {data_type} not found')
            self.data_managers[data_type] = type_class(repository)

    def load_all(self) -> None:
        for data_manager in self.data_managers.values():
            data_manager.load()
    
    def reload_all(self) -> None:
        for data_manager in self.data_managers.values():
            data_manager.reload()

    def get(self, data_type: DataType, identifier: str) -> DataDescription:
        if data_type in self.data_managers:
            return self.data_managers[data_type].get(identifier)
        return None
