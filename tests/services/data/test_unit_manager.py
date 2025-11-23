from pathlib import Path
from typing import Any, Dict, List

from services.data.core import DataManagerConfig, DataType
from services.data.manager import DataManager, DataManagerFactory
from services.data.models import UnitDataDescription
from utils.file_system import FileSystemProtocol, LocalFileSystem
from utils.loader import LoaderProtocol, YamlLoader


def scout_unit_data():
    return {
        'identity': {
            'id': 'Scout',
            'name': 'Scout Goose',
            'unit_class': 'Recon'
        },
        'sprites': {
            'character': 'units/scout_goose_char.png',
            'board': 'units/scout_goose_board.png'
        },
        'stats': {
            'hp': {'base': 80, 'growth': 5, 'regen': 2},
            'attack': {'base': 15, 'growth': 2},
            'defense': {'base': 10, 'growth': 1},
            'speed': {'base': 5, 'growth': 0.2},
            'attack_range': {'base': 4},
            'movement_range': {'base': 6}
        },
        'skills': {
            'passive': 'evasion_instinct'
        }
    }

def bard_unit_data():
    return {
        'identity': {
            'id': 'Bard',
            'name': 'Bard Goose',
            'unit_class': 'Support'
        },
        'sprites': {
            'character': 'units/bard_goose_char.png',
            'board': 'units/bard_goose_board.png'
        },
        'stats': {
            'hp': {'base': 90, 'growth': 6, 'regen': 3},
            'attack': {'base': 10, 'growth': 1},
            'defense': {'base': 12, 'growth': 3},
            'speed': {'base': 8, 'growth': 0.5},
            'attack_range': {'base': 5},
            'movement_range': {'base': 3}
        },
        'skills': {
            'passive': 'happy_melody'
        }
    }

class MockLoader(LoaderProtocol):

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def load_file(self, filepath: str) -> Any:
        return self.data.get(filepath, {})


class MockFileSystem(FileSystemProtocol):
    
    def __init__(self, data: List[str]):
        self.data = data
    
    def glob(self, base_path: Path, pattern: str) -> List[Path]:
        return self.data
        

def create_unit_data_manager(loader: LoaderProtocol = None, file_provider: FileSystemProtocol = None) -> DataManager:
    if loader is None:
        loader = MockLoader({'scout': scout_unit_data(), 'bard': bard_unit_data()})
    if file_provider is None:
        file_provider = MockFileSystem(['scout', 'bard'])
    return DataManager(UnitDataDescription, loader, file_provider, 'search_path')


def test_build_unit_data_manager():
    data = {
        'type': DataType.UNIT,
        'data_model': 'services.data.models.UnitDataDescription',
        'data_loader': 'utils.loader.YamlLoader',
        'file_provider': 'utils.file_system.LocalFileSystem',
        'search_path': 'data/units'
    }
    data_manager_config = DataManagerConfig(**data)
    data_manager = DataManagerFactory.build(data_manager_config)
    assert isinstance(data_manager, DataManager)
    assert data_manager.data_model == UnitDataDescription
    assert data_manager.data_loader == YamlLoader
    assert data_manager.file_provider == LocalFileSystem
    assert data_manager.search_path == Path('data/units')
 
def test_load_unit_data_correct():
    unit_data_manager = create_unit_data_manager()
    errors = unit_data_manager.load()
    assert errors == []
    assert len(unit_data_manager.data) == 2
    assert 'Scout' in unit_data_manager.data
    assert 'Bard' in unit_data_manager.data

def test_load_unit_data_incorrect():
    scout_data = scout_unit_data()
    scout_data.pop('sprites')
    loader = MockLoader({'scout': scout_data, 'bard': bard_unit_data()})
    unit_data_manager = create_unit_data_manager(loader=loader)
    errors = unit_data_manager.load()
    assert len(errors) == 1
    error = errors[0]
    assert error.filename == 'scout'
    assert 'sprites' in error.message
    assert unit_data_manager.data == {}

def test_load_unit_data_duplicate():
    loader = MockLoader({'scout': scout_unit_data(), 'bard': scout_unit_data()})
    unit_data_manager = create_unit_data_manager(loader=loader)
    errors = unit_data_manager.load()
    assert len(errors) == 1
    error = errors[0]
    assert error.filename == 'bard'
    assert 'registered' in error.message
    assert unit_data_manager.data == {}

def test_reload_unit_data_correct():
    loader_scout = MockLoader({'scout': scout_unit_data()})
    scout_file_provider = MockFileSystem(['scout'])
    unit_data_manager = create_unit_data_manager(loader=loader_scout, file_provider=scout_file_provider)
    unit_data_manager.load()
    assert len(unit_data_manager.data) == 1
    assert 'Scout' in unit_data_manager.data

    loader_bard = MockLoader({'bard': bard_unit_data()})
    bard_file_provider = MockFileSystem(['bard'])
    unit_data_manager.data_loader = loader_bard
    unit_data_manager.file_provider = bard_file_provider
    unit_data_manager.reload()
    assert len(unit_data_manager.data) == 1
    assert 'Bard' in unit_data_manager.data

def test_get_existing_unit():
    unit_data_manager = create_unit_data_manager()
    unit_data_manager.load()
    unit = unit_data_manager.get('Scout')
    assert isinstance(unit, UnitDataDescription)

def test_get_non_existing_unit():
    unit_data_manager = create_unit_data_manager()
    unit_data_manager.load()
    unit = unit_data_manager.get('Warrior')
    assert unit is None
