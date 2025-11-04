import pytest
from services.data.core import DataType
from utils.registry import clear_registry, get_registered_data_managers, register_data_manager


@pytest.fixture(autouse=True)
def clean_data_manager_registry():
    clear_registry()


def test_register_data_manager():
    @register_data_manager(DataType.UNIT)
    class DataManagerA: pass
    assert len(get_registered_data_managers()) == 1
    
def test_register_duplicate_data_manager():
    @register_data_manager(DataType.UNIT)
    class DataManagerA: pass
    with pytest.raises(ValueError):
        @register_data_manager(DataType.UNIT)
        class DataManagerB: pass
    