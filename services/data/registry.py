from typing import Dict, Type

from services.data.core import DataManagerProtocol, DataType


_registry: Dict[DataType, Type[DataManagerProtocol]] = {}


def register_data_manager(data_type: DataType) -> None:
    def decorator(cls):
        if data_type in _registry:
            raise ValueError(f'DataType {data_type} already has a registered data manager')
        _registry[data_type] = cls
        return cls
    return decorator


def clear_registry() -> None:
    _registry.clear()


def get_registered_data_managers() -> Dict[DataType, Type[DataManagerProtocol]]:
    return _registry