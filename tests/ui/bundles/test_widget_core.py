from ui.bundles import WidgetCoreBundle
from ui.components.behavior import Enabled
from ui.components.rendering import Dirty


def test_default_widget_core():
    core = WidgetCoreBundle()
    core_components = set([type(component) for component in core.components()])

    expected_components = set([Enabled, Dirty])
    assert core_components == expected_components


def test_disabled_widget_core():
    core = WidgetCoreBundle(False)
    core_components = set([type(component) for component in core.components()])

    expected_components = set([Dirty])
    assert core_components == expected_components

    non_existing_components = set([Enabled])
    assert non_existing_components.intersection(core_components) == set()


def test_multiple_instances():
    core = WidgetCoreBundle()
    components1 = list(core.components())
    components2 = list(core.components())

    for index, component in enumerate(components1):
        assert id(component) != id(components2[index])
