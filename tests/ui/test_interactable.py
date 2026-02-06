from ui.components.behavior import Hoverable, Pressable, Trigger
from ui.widgets import InteractableBundle


def test_default_interactable():
    interactable = InteractableBundle(None)
    interactable_components = list(interactable.components())

    expected_components = [Hoverable, Pressable, Trigger]
    assert len(interactable_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in interactable_components)
