from ui.bundles import WidgetCoreBundle
from ui.components.behavior import Enabled
from ui.components.rendering import Dirty


def test_default_widget_core():
    core = WidgetCoreBundle()
    core_components = list(core.components())

    expected_components = [Enabled, Dirty]
    assert len(core_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in core_components)


def test_disabled_widget_core():
    core = WidgetCoreBundle(False)
    core_components = list(core.components())

    expected_components = [Dirty]
    assert len(core_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in core_components)

    non_existing_components = [Enabled]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in core_components)


def test_multiple_instances():
    core = WidgetCoreBundle()
    components1 = list(core.components())
    components2 = list(core.components())

    for index, component in enumerate(components1):
        assert id(component) != id(components2[index])
