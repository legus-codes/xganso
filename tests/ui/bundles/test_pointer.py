from ui.bundles import PressableBundle
from ui.components.behavior import Pressable


def test_default_pointer():
    pointer = PressableBundle()
    pointer_components = set([type(component) for component in pointer.components()])

    expected_components = set([Pressable])
    assert pointer_components == expected_components
