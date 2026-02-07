from ui.bundles import ActivatableBundle
from ui.components.behavior import Trigger


def test_default_pointer():
    activatable = ActivatableBundle(None)
    activatable_components = list(activatable.components())

    expected_components = [Trigger]
    assert len(activatable_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in activatable_components)
