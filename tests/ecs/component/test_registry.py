import pytest

from ecs_architecture.component.registry import ComponentRegistry, register_component


@register_component('mock_a')
def build_mockA():
    ...

@register_component('mock_b')
def build_mockB():
    ...

def test_registry_empty_on_creation():
    registry = ComponentRegistry()
    assert registry.builders == {}

@pytest.mark.parametrize('component', ['mock_a', 'mock_b'])
def test_load_registered_component(component):
    registry = ComponentRegistry()
    registry.load(component)

@pytest.mark.parametrize('component', ['mock_a', 'mock_b'])
def test_get_registered_component(component):
    registry = ComponentRegistry()
    registry.load(component)
    builder = registry.get_builder(component)
    assert builder is not None

def test_load_unregistered_component():
    component = 'mock_c'
    registry = ComponentRegistry()
    with pytest.raises(ValueError):
        registry.load(component)

def test_get_unregistered_component():
    component = 'mock_c'
    registry = ComponentRegistry()
    builder = registry.get_builder(component)
    assert builder is None

def test_register_duplicate_name():
    with pytest.raises(ValueError):
        @register_component("mock_b")
        def build_mockC():
            ...
