from enum import Enum
from typing import List

import pytest
from services.data.core import DataManagerError, DataManagerProtocol
from services.data.models import DataDescription
from services.data.service import DataService


class TestDataType(Enum):
    UNIT = 0
    ITEM = 1


class MockDataManager(DataManagerProtocol):

    def __init__(self):
        self.loaded = False
        self.reloaded = False
        self.called = False
    
    def load(self) -> List[DataManagerError]:
        self.loaded = True
        return []

    def reload(self) -> List[DataManagerError]:
        self.reloaded = True
        return []

    def get(self, identifier: str) -> DataDescription | None:
        self.called = True
        return DataDescription(id='id')


@pytest.fixture
def data_service() -> DataService:
    data_service = DataService()
    data_service.register(TestDataType.UNIT, MockDataManager())
    data_service.register(TestDataType.ITEM, MockDataManager())
    return data_service


def assert_data_manager(data_manger: MockDataManager, is_loaded: bool, is_reloaded: bool, is_called: bool) -> None:
    assert data_manger.loaded == is_loaded
    assert data_manger.reloaded == is_reloaded
    assert data_manger.called == is_called
    

def test_initialize_data_service():
    data_service = DataService()
    assert data_service.data_managers == {}

def test_register_data_managers(data_service: DataService):
    assert TestDataType.UNIT in data_service.data_managers
    assert TestDataType.ITEM in data_service.data_managers
    unit_data_manager = data_service.data_managers[TestDataType.UNIT]
    assert isinstance(unit_data_manager, MockDataManager)
    assert_data_manager(unit_data_manager, False, False, False)
    item_data_manager = data_service.data_managers[TestDataType.ITEM]
    assert isinstance(item_data_manager, MockDataManager)
    assert_data_manager(item_data_manager, False, False, False)

def test_load_data_managers(data_service: DataService):
    data_service.load_all()
    unit_data_manager = data_service.data_managers[TestDataType.UNIT]
    assert_data_manager(unit_data_manager, True, False, False)
    item_data_manager = data_service.data_managers[TestDataType.ITEM]
    assert_data_manager(item_data_manager, True, False, False)

def test_reload_data_managers(data_service: DataService):
    data_service.reload_all()
    unit_data_manager = data_service.data_managers[TestDataType.UNIT]
    assert_data_manager(unit_data_manager, False, True, False)
    item_data_manager = data_service.data_managers[TestDataType.ITEM]
    assert_data_manager(item_data_manager, False, True, False)

def test_get_from_data_managers(data_service: DataService):
    data_service.get(TestDataType.UNIT, 'id')
    unit_data_manager = data_service.data_managers[TestDataType.UNIT]
    assert_data_manager(unit_data_manager, False, False, True)
    item_data_manager = data_service.data_managers[TestDataType.ITEM]
    assert_data_manager(item_data_manager, False, False, False)
