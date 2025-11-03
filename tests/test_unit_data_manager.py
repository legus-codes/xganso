from typing import Any, Dict

from services.data.data_models import UnitDataDescription
from services.data.managers.unit_data_manager import UnitDataManager
from utils.repository import RepositoryProtocol


def scout_unit_data():
    return {
        'id': 'Scout',
        'name': 'Scout Goose',
        'unit_class': 'Recon',
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
        'passive': 'evasion_instinct'
    }

def bard_unit_data():
    return {
        'id': 'Bard',
        'name': 'Bard Goose',
        'unit_class': 'Support',
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
        'passive': 'happy_melody'
    }

class MockRepository(RepositoryProtocol):

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def load(self) -> Dict[str, Any]:
        return self.data


def test_load_unit_data_correct():
    repository = MockRepository({'scout.yaml': scout_unit_data(), 'bard.yaml': bard_unit_data()})
    unit_data_manager = UnitDataManager(repository)
    errors = unit_data_manager.load()
    assert errors == {}
    assert len(unit_data_manager.data) == 2
    assert 'Scout' in unit_data_manager.data
    assert 'Bard' in unit_data_manager.data

def test_load_unit_data_incorrect():
    scout_data = scout_unit_data()
    scout_data.pop('sprites')
    repository = MockRepository({'scout.yaml': scout_data, 'bard.yaml': bard_unit_data()})
    unit_data_manager = UnitDataManager(repository)
    errors = unit_data_manager.load()
    assert len(errors) == 1
    assert 'scout.yaml' in errors
    assert 'sprites' in errors['scout.yaml']
    assert unit_data_manager.data == {}

def test_load_unit_data_duplicate():
    repository = MockRepository({'scout.yaml': scout_unit_data(), 'bard.yaml': scout_unit_data()})
    unit_data_manager = UnitDataManager(repository)
    errors = unit_data_manager.load()
    assert len(errors) == 1
    assert 'bard.yaml' in errors
    assert 'registered' in errors['bard.yaml']
    assert unit_data_manager.data == {}

def test_reload_unit_data_correct():
    repository_scout = MockRepository({'scout.yaml': scout_unit_data()})
    unit_data_manager = UnitDataManager(repository_scout)
    unit_data_manager.load()
    assert len(unit_data_manager.data) == 1
    assert 'Scout' in unit_data_manager.data

    repository_bard = MockRepository({'bard.yaml': bard_unit_data()})
    unit_data_manager.repository = repository_bard
    unit_data_manager.reload()
    assert len(unit_data_manager.data) == 1
    assert 'Bard' in unit_data_manager.data

def test_get_existing_unit():
    repository = MockRepository({'scout.yaml': scout_unit_data(), 'bard.yaml': bard_unit_data()})
    unit_data_manager = UnitDataManager(repository)
    unit_data_manager.load()
    unit = unit_data_manager.get('Scout')
    assert isinstance(unit, UnitDataDescription)

def test_get_non_existing_unit():
    repository = MockRepository({'scout.yaml': scout_unit_data(), 'bard.yaml': bard_unit_data()})
    unit_data_manager = UnitDataManager(repository)
    unit_data_manager.load()
    unit = unit_data_manager.get('Warrior')
    assert unit is None
