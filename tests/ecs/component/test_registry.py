import pytest

from ecs_architecture.component.registry import ComponentRegistry, GlobalComponentRegistry


@GlobalComponentRegistry.register_component('section.mock_a')
def build_mockA():
    ...

@GlobalComponentRegistry.register_component('section.mock_b')
def build_mockB():
    ...

def test_registry_empty_on_creation():
    registry = ComponentRegistry()
    assert registry.builders == {}

@pytest.mark.parametrize('component', ['section.mock_a', 'section.mock_b'])
def test_load_registered_component(component):
    section, name = component.split('.')
    registry = ComponentRegistry()
    registry.load(component)
    assert section in registry.builders
    assert name in registry.builders[section]

@pytest.mark.parametrize('component', ['section.mock_a', 'section.mock_b'])
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

def test_load_unregistered_section():
    component = 'session.mock_a'
    registry = ComponentRegistry()
    with pytest.raises(ValueError):
        registry.load(component)

def test_get_unregistered_component():
    component = 'mock_c'
    registry = ComponentRegistry()
    builder = registry.get_builder(component)
    assert builder is None

def test_get_unregistered_component():
    component = 'section.mock_c'
    registry = ComponentRegistry()
    builder = registry.get_builder(component)
    assert builder is None

def test_register_duplicate_name():
    with pytest.raises(ValueError):
        @GlobalComponentRegistry.register_component('section.mock_b')
        def build_mockC():
            ...

def test_register_wrong_name():
    with pytest.raises(ValueError):
        @GlobalComponentRegistry.register_component('mock_b')
        def build_mockC():
            ...

def test_get_full_name():
    name = GlobalComponentRegistry.get_full_name('section', 'component')
    assert name == 'section.component'

def test_get_section_component():
    section, component = GlobalComponentRegistry.get_section_component('section.component')
    assert section == 'section'
    assert component == 'component'

def test_get_section_component_wrong_input():
    with pytest.raises(ValueError):
        GlobalComponentRegistry.get_section_component('error')
