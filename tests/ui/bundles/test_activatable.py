from ui.bundles import ActivatableBundle
from ui.components.behavior import Trigger


def test_default_activatable():
    activatable = ActivatableBundle(None)
    activatable_components = set([type(component) for component in activatable.components()])

    expected_components = set([Trigger])
    assert activatable_components == expected_components
