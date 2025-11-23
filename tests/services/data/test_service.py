from enum import Enum
from typing import List

import pytest
from services.core import LoadingError
from services.data.core import DataManagerProtocol
from services.data.models import DataDescription
from services.data.service import DataService


class DataTypeTest(Enum):
    UNIT = 0
    ITEM = 1
    NONE = 2


class MockDataManager(DataManagerProtocol):

    def __init__(self):
        self.loaded = False
        self.reloaded = False
        self.called = False
    
    def load(self) -> List[LoadingError]:
        self.loaded = True
        return []

    def reload(self) -> List[LoadingError]:
        self.reloaded = True
        return []

    def get(self, identifier: str) -> DataDescription | None:
        self.called = True
        return DataDescription(id='id')


@pytest.fixture
def data_service() -> DataService:
    data_service = DataService()
    data_service.register(DataTypeTest.UNIT, MockDataManager())
    data_service.register(DataTypeTest.ITEM, MockDataManager())
    return data_service


def assert_data_manager(data_manger: MockDataManager, is_loaded: bool, is_reloaded: bool, is_called: bool) -> None:
    assert data_manger.loaded == is_loaded
    assert data_manger.reloaded == is_reloaded
    assert data_manger.called == is_called
    

def test_initialize_data_service():
    data_service = DataService()
    assert data_service.data_managers == {}

def test_register_data_managers(data_service: DataService):
    assert DataTypeTest.UNIT in data_service.data_managers
    assert DataTypeTest.ITEM in data_service.data_managers
    unit_data_manager = data_service.data_managers[DataTypeTest.UNIT]
    assert isinstance(unit_data_manager, MockDataManager)
    assert_data_manager(unit_data_manager, False, False, False)
    item_data_manager = data_service.data_managers[DataTypeTest.ITEM]
    assert isinstance(item_data_manager, MockDataManager)
    assert_data_manager(item_data_manager, False, False, False)

def test_load_data_managers(data_service: DataService):
    data_service.load_all()
    unit_data_manager = data_service.data_managers[DataTypeTest.UNIT]
    assert_data_manager(unit_data_manager, True, False, False)
    item_data_manager = data_service.data_managers[DataTypeTest.ITEM]
    assert_data_manager(item_data_manager, True, False, False)

def test_reload_data_managers(data_service: DataService):
    data_service.reload_all()
    unit_data_manager = data_service.data_managers[DataTypeTest.UNIT]
    assert_data_manager(unit_data_manager, False, True, False)
    item_data_manager = data_service.data_managers[DataTypeTest.ITEM]
    assert_data_manager(item_data_manager, False, True, False)

def test_get_from_data_managers(data_service: DataService):
    data = data_service.get(DataTypeTest.UNIT, 'id')
    assert isinstance(data, DataDescription)
    unit_data_manager = data_service.data_managers[DataTypeTest.UNIT]
    assert_data_manager(unit_data_manager, False, False, True)
    item_data_manager = data_service.data_managers[DataTypeTest.ITEM]
    assert_data_manager(item_data_manager, False, False, False)

def test_get_from_non_existing_data_manager(data_service: DataService):
    data = data_service.get(DataTypeTest.NONE, 'id')
    assert data is None
    unit_data_manager = data_service.data_managers[DataTypeTest.UNIT]
    assert_data_manager(unit_data_manager, False, False, False)
    item_data_manager = data_service.data_managers[DataTypeTest.ITEM]
    assert_data_manager(item_data_manager, False, False, False)
