from ui.bundles import ToggleableBundle
from ui.components.behavior import Toggleable, Toggled


def test_default_toggleable():
    toggleable = ToggleableBundle()
    toggleable_components = set([type(component) for component in toggleable.components()])

    expected_components = set([Toggleable])
    assert toggleable_components == expected_components

    non_existing_components = set([Toggled])
    assert non_existing_components.intersection(toggleable_components) == set()


def test_active_toggleable():
    toggleable = ToggleableBundle(True)
    toggleable_components = set([type(component) for component in toggleable.components()])

    expected_components = set([Toggleable, Toggled])
    assert toggleable_components == expected_components
