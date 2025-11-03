from typing import Dict
from pydantic import ValidationError

from services.data.core import DataManagerProtocol, DataType
from services.data.data_models import UnitDataDescription
from services.data.registry import register_data_manager
from utils.repository import RepositoryProtocol


@register_data_manager(DataType.UNIT)
class UnitDataManager(DataManagerProtocol):

    def __init__(self, 
                 repository: RepositoryProtocol):
        self.data: Dict[str, UnitDataDescription] = {}
        self.repository = repository

    def load(self) -> Dict[str, str]:
        errors = {}
        for filename, unit_data in self.repository.load().items():
            try:
                unit = UnitDataDescription(**unit_data)
                if unit.id in self.data:
                    errors[filename] = f'Unit with {unit.id} already registered'
                    continue
                self.data[unit.id] = unit
            except ValidationError as ve:
                errors[filename] = str(ve)

        if errors:
            self._clear()
        return errors

    def reload(self) -> Dict[str, str]:
        self._clear()
        return self.load()

    def get(self, identifier: str) -> UnitDataDescription | None:
        return self.data.get(identifier, None)

    def _clear(self) -> None:
        self.data.clear()
