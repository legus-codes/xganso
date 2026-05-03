from ui.bundles import PressableBundle
from ui.components.behavior import Pressable


def test_default_pressable():
    pressable = PressableBundle()
    pressable_components = set([type(component) for component in pressable.components()])

    expected_components = set([Pressable])
    assert pressable_components == expected_components
