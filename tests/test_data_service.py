from enum import Enum
from typing import Dict, List

import pytest
from services.data.core import DataManagerError
from services.data.data_models import DataDescription
from services.data.registry import clear_registry, register_data_manager
from services.data.service import DataService
from utils.repository import RepositoryProtocol


class TestDataType(Enum):
    UNIT = 0
    ITEM = 1


class MockDataManager:

    def __init__(self, repository: RepositoryProtocol):
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


class MockRepository(RepositoryProtocol): pass

@pytest.fixture
def mock_repository() -> Dict[TestDataType, RepositoryProtocol]:
    return { TestDataType.UNIT: MockRepository(), TestDataType.ITEM: MockRepository() }


def assert_data_manager(data_manger: MockDataManager, is_loaded: bool, is_reloaded: bool, is_called: bool) -> None:
    assert data_manger.loaded == is_loaded
    assert data_manger.reloaded == is_reloaded
    assert data_manger.called == is_called
    

@pytest.fixture(autouse=True)
def clean_data_manager_registry():
    clear_registry()
    register_data_manager(TestDataType.UNIT)(MockDataManager)
    register_data_manager(TestDataType.ITEM)(MockDataManager)


def test_initialize_data_service(mock_repository):
    data_service = DataService(mock_repository)
    assert TestDataType.UNIT in data_service.data_managers
    assert TestDataType.ITEM in data_service.data_managers
    unit_data_manager = data_service.data_managers[TestDataType.UNIT]
    assert isinstance(unit_data_manager, MockDataManager)
    assert_data_manager(unit_data_manager, False, False, False)
    item_data_manager = data_service.data_managers[TestDataType.ITEM]
    assert isinstance(item_data_manager, MockDataManager)
    assert_data_manager(item_data_manager, False, False, False)

def test_load_data_managers(mock_repository):
    data_service = DataService(mock_repository)
    data_service.load_all()
    unit_data_manager = data_service.data_managers[TestDataType.UNIT]
    assert_data_manager(unit_data_manager, True, False, False)
    item_data_manager = data_service.data_managers[TestDataType.ITEM]
    assert_data_manager(item_data_manager, True, False, False)

def test_reload_data_managers(mock_repository):
    data_service = DataService(mock_repository)
    data_service.reload_all()
    unit_data_manager = data_service.data_managers[TestDataType.UNIT]
    assert_data_manager(unit_data_manager, False, True, False)
    item_data_manager = data_service.data_managers[TestDataType.ITEM]
    assert_data_manager(item_data_manager, False, True, False)

def test_get_from_data_managers(mock_repository):
    data_service = DataService(mock_repository)
    data_service.get(TestDataType.UNIT, 'id')
    unit_data_manager = data_service.data_managers[TestDataType.UNIT]
    assert_data_manager(unit_data_manager, False, False, True)
    item_data_manager = data_service.data_managers[TestDataType.ITEM]
    assert_data_manager(item_data_manager, False, False, False)
