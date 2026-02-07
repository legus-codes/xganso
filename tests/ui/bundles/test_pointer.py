from ui.bundles import PointerBundle
from ui.components.behavior import Hoverable, Pressable


def test_default_pointer():
    pointer = PointerBundle()
    pointer_components = list(pointer.components())

    expected_components = [Hoverable, Pressable]
    assert len(pointer_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in pointer_components)
