import pytest

from ecs_architecture.component.registry import ComponentRegistry, GlobalComponentRegistry


@GlobalComponentRegistry.register_component('section', 'mock_a')
def build_mockA():
    ...

@GlobalComponentRegistry.register_component('section', 'mock_b')
def build_mockB():
    ...


def test_get_section():
    section = GlobalComponentRegistry.get_section('section')
    assert len(section) == 2
    assert 'mock_a' in section
    assert 'mock_b' in section

def test_get_non_existing_section():
    section = GlobalComponentRegistry.get_section('non_existing')
    assert section == {}

def test_registry_empty_on_creation():
    registry = ComponentRegistry()
    assert registry.builders == {}

@pytest.mark.parametrize('component', ['mock_a', 'mock_b'])
def test_load_registered_component(component):
    section = 'section'
    registry = ComponentRegistry()
    registry.load(section, component)
    assert section in registry.builders
    assert component in registry.builders[section]

def test_load_multiple_registered_component():
    section = 'section'
    mock_a = 'mock_a'
    mock_b = 'mock_b'
    registry = ComponentRegistry()
    registry.load(section, mock_a)
    registry.load(section, mock_b)
    assert section in registry.builders
    assert mock_a in registry.builders[section]
    assert mock_b in registry.builders[section]

@pytest.mark.parametrize('component', ['mock_a', 'mock_b'])
def test_get_registered_component(component):
    section = 'section'
    registry = ComponentRegistry()
    registry.load(section, component)
    builder = registry.get_builder(section, component)
    assert builder is not None

def test_load_unregistered_component():
    section = 'section'
    component = 'mock_c'
    registry = ComponentRegistry()
    with pytest.raises(ValueError):
        registry.load(section, component)

def test_load_unregistered_section():
    section = 'session'
    component = 'mock_a'
    registry = ComponentRegistry()
    with pytest.raises(ValueError):
        registry.load(section, component)

def test_get_unregistered_component():
    section = 'section'
    component = 'mock_c'
    registry = ComponentRegistry()
    builder = registry.get_builder(section, component)
    assert builder is None

def test_get_unregistered_section():
    section = 'non_existing'
    component = 'mock_a'
    registry = ComponentRegistry()
    builder = registry.get_builder(section, component)
    assert builder is None

def test_register_duplicate_name():
    with pytest.raises(ValueError):
        @GlobalComponentRegistry.register_component('section', 'mock_b')
        def build_mockC():
            ...
