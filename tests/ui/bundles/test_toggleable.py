from ui.bundles import ToggleableBundle
from ui.components.behavior import Toggleable, Toggled


def test_default_toggleable():
    toggleable = ToggleableBundle()
    toggleable_components = list(toggleable.components())

    expected_components = [Toggleable]
    assert len(toggleable_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in toggleable_components)

    non_existing_components = [Toggled]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in toggleable_components)


def test_active_toggleable():
    toggleable = ToggleableBundle(True)
    toggleable_components = list(toggleable.components())

    expected_components = [Toggleable, Toggled]
    assert len(toggleable_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in toggleable_components)
