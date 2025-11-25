from typing import Dict
import pytest
from ecs_architecture.component.builder import ComponentBuilder
from ecs_architecture.component.registry import ComponentRegistryProtocol, GlobalComponentRegistry
from ecs_framework.ecs import ComponentProtocol


class MockComponentAttack(ComponentProtocol):
    attack: float
    
@GlobalComponentRegistry.register_component('stats', 'mock_attack')
def build_mock_attack(attack: float) -> MockComponentAttack:
    return MockComponentAttack(attack=attack)

class MockComponentHp(ComponentProtocol):
    hp: float
    
@GlobalComponentRegistry.register_component('stats', 'mock_hp')
def build_mock_hp(hp: float) -> MockComponentHp:
    return MockComponentHp(hp=hp)

class MockComponentRegistry(ComponentRegistryProtocol):
    
    def __init__(self, data: Dict[str, Dict[str, callable]]):
        self.data = data

    def get_builder(self, section: str, component: str) -> callable:
        section_builders = self.data.get(section, {})
        return section_builders.get(component, None)

@pytest.fixture
def registry() -> MockComponentRegistry:
    data = {
        'stats': {
            'mock_attack': build_mock_attack,
            'mock_hp': build_mock_hp
        }
    }
    return MockComponentRegistry(data)


def test_build_empty():
    builder = ComponentBuilder(MockComponentRegistry({}))
    components = builder.build({})
    assert components == []

def test_build_mock_attack(registry: MockComponentRegistry):
    builder = ComponentBuilder(registry)
    components = builder.build({'stats': {'mock_attack': {'attack': 5.5}}})
    assert len(components) == 1
    assert isinstance(components[0], MockComponentAttack)
    assert components[0].attack == 5.5

def test_build_mock_attack_wrong_parameter(registry: MockComponentRegistry):
    builder = ComponentBuilder(registry)
    with pytest.raises(TypeError):
        builder.build({'stats': {'mock_attack': {'hp': 5.5}}})

def test_build_mock_hp(registry: MockComponentRegistry):
    builder = ComponentBuilder(registry)
    components = builder.build({'stats': {'mock_hp': {'hp': 53.52}}})
    assert len(components) == 1
    assert isinstance(components[0], MockComponentHp)
    assert components[0].hp == 53.52

def test_build_mock_hp_wrong_parameter(registry: MockComponentRegistry):
    builder = ComponentBuilder(registry)
    with pytest.raises(TypeError):
        builder.build({'stats': {'mock_hp': {'attack': 5.5}}})

def test_build_mock_attack_hp(registry: MockComponentRegistry):
    builder = ComponentBuilder(registry)
    components = builder.build({'stats': {'mock_attack': {'attack': 5.5}, 'mock_hp': {'hp': 53.52}}})
    assert len(components) == 2
    assert isinstance(components[0], MockComponentAttack)
    assert components[0].attack == 5.5
    assert isinstance(components[1], MockComponentHp)
    assert components[1].hp == 53.52

def test_build_mock_hp_attack(registry: MockComponentRegistry):
    builder = ComponentBuilder(registry)
    components = builder.build({'stats': {'mock_hp': {'hp': 53.52}, 'mock_attack': {'attack': 5.5}}})
    assert len(components) == 2
    assert isinstance(components[0], MockComponentHp)
    assert components[0].hp == 53.52
    assert isinstance(components[1], MockComponentAttack)
    assert components[1].attack == 5.5

def test_build_non_existing_component():
    builder = ComponentBuilder(MockComponentRegistry({}))
    with pytest.raises(KeyError):
        builder.build({'stats': {'mock_defense': {'defense': 4.5}}})    

def test_build_mock_attack_hp_defense(registry: MockComponentRegistry):
    builder = ComponentBuilder(registry)
    with pytest.raises(KeyError):
        builder.build({'stats': {'mock_attack': {'attack': 5.5}, 'mock_hp': {'hp': 53.52}, 'mock_defense': {'defense': 4.5}}})

def test_build_component_mock_attack(registry: MockComponentRegistry):
    builder = ComponentBuilder(registry)
    component = builder._build_component('stats', 'mock_attack', {'attack': 5.5})
    assert isinstance(component, MockComponentAttack)
    assert component.attack == 5.5

def test_build_component_mock_hp(registry: MockComponentRegistry):
    builder = ComponentBuilder(registry)
    component = builder._build_component('stats', 'mock_hp', {'hp': 53.52})
    assert isinstance(component, MockComponentHp)
    assert component.hp == 53.52

def test_build_component_mock_defense(registry: MockComponentRegistry):
    builder = ComponentBuilder(registry)
    with pytest.raises(KeyError):
        builder._build_component('stats', 'mock_defense', {'defense': 4.7})
    