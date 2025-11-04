from typing import Dict


from services.data.core import DataManagerProtocol, DataType
from services.data.data_models import DataDescription


class DataService:

    def __init__(self):
        self.data_managers: Dict[DataType, DataManagerProtocol] = {}
    
    def register(self, data_type: DataType, data_manager: DataManagerProtocol):
        self.data_managers[data_type] = data_manager

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
