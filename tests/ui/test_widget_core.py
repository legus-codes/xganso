from ui.components.behavior import Enabled
from ui.components.rendering import Dirty
from ui.widgets import WidgetCoreBundle


def test_default_widget_core():
    widget_core = WidgetCoreBundle()
    widget_core_components = list(widget_core.components())

    expected_components = [Enabled, Dirty]
    assert len(widget_core_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in widget_core_components)


def test_disabled_widget_core():
    widget_core = WidgetCoreBundle(False)
    widget_core_components = list(widget_core.components())

    expected_components = [Dirty]
    assert len(widget_core_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in widget_core_components)

    non_existing_components = [Enabled]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in widget_core_components)


def test_multiple_instances():
    widget_core = WidgetCoreBundle()
    components1 = list(widget_core.components())
    components2 = list(widget_core.components())

    for index, component in enumerate(components1):
        assert id(component) != id(components2[index])
