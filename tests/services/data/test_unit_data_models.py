import pytest
from pydantic import ValidationError

from services.data.data_models import UnitDataDescription


@pytest.fixture
def unit_data() -> dict:
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


def test_correct_unit(unit_data: dict):
    UnitDataDescription(**unit_data)

def test_correct_unit_without_passive(unit_data: dict):
    unit_data.pop('passive')
    UnitDataDescription(**unit_data)

@pytest.mark.parametrize('field', ['id', 'name', 'unit_class', 'sprites', 'stats'])
def test_incorrect_unit_without_fields(unit_data: dict, field: str):
    unit_data.pop(field)
    with pytest.raises(ValidationError):
        UnitDataDescription(**unit_data)

@pytest.mark.parametrize('field', ['character', 'board'])
def test_incorrect_unit_without_sprites_fields(unit_data: dict, field: str):
    unit_data['sprites'].pop(field)
    with pytest.raises(ValidationError):
        UnitDataDescription(**unit_data)

@pytest.mark.parametrize('field', ['hp', 'attack', 'defense', 'speed', 'attack_range', 'movement_range'])
def test_incorrect_unit_without_stats_fields(unit_data: dict, field: str):
    unit_data['stats'].pop(field)
    with pytest.raises(ValidationError):
        UnitDataDescription(**unit_data)

@pytest.mark.parametrize('field', ['base', 'growth', 'regen'])
def test_incorrect_unit_without_hp_fields(unit_data: dict, field: str):
    unit_data['stats']['hp'].pop(field)
    with pytest.raises(ValidationError):
        UnitDataDescription(**unit_data)

@pytest.mark.parametrize('field', ['base', 'growth'])
def test_incorrect_unit_without_attack_fields(unit_data: dict, field: str):
    unit_data['stats']['attack'].pop(field)
    with pytest.raises(ValidationError):
        UnitDataDescription(**unit_data)

@pytest.mark.parametrize('field', ['base', 'growth'])
def test_incorrect_unit_without_defense_fields(unit_data: dict, field: str):
    unit_data['stats']['defense'].pop(field)
    with pytest.raises(ValidationError):
        UnitDataDescription(**unit_data)

@pytest.mark.parametrize('field', ['base', 'growth'])
def test_incorrect_unit_without_speed_fields(unit_data: dict, field: str):
    unit_data['stats']['speed'].pop(field)
    with pytest.raises(ValidationError):
        UnitDataDescription(**unit_data)

@pytest.mark.parametrize('field', ['base'])
def test_incorrect_unit_without_attack_range_fields(unit_data: dict, field: str):
    unit_data['stats']['attack_range'].pop(field)
    with pytest.raises(ValidationError):
        UnitDataDescription(**unit_data)

@pytest.mark.parametrize('field', ['base'])
def test_incorrect_unit_without_movement_range_fields(unit_data: dict, field: str):
    unit_data['stats']['movement_range'].pop(field)
    with pytest.raises(ValidationError):
        UnitDataDescription(**unit_data)
