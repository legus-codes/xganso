import pytest

from core.primitives import IVec2
from ui.components.layout import GridLayout, HorizontalLayout, Layout, VerticalLayout
from ui.types import GridLayoutDescription, HorizontalLayoutDescription, LayoutDescription, VerticalLayoutDescription
from ui.widgets import PanelLayoutBundle


def test_default_panel_layout():
    layout = PanelLayoutBundle()
    layout_components = set([type(component) for component in layout.components()])

    expected_components = set()
    assert layout_components == expected_components

    non_existing_components = set([Layout, HorizontalLayout, VerticalLayout, GridLayout])
    assert non_existing_components.intersection(layout_components) == set()


@pytest.mark.parametrize("layout_description", [HorizontalLayoutDescription(10, IVec2()), VerticalLayoutDescription(10, IVec2()), GridLayoutDescription(2, 2, IVec2(), IVec2())])
def test_panel_layout_variants(layout_description: LayoutDescription):
    layout = PanelLayoutBundle(layout_description)
    layout_components = set([type(component) for component in layout.components()])

    if isinstance(layout_description, HorizontalLayoutDescription):
        expected_components = set([HorizontalLayout])
        non_existing_components = set([VerticalLayout, GridLayout])
    elif isinstance(layout_description, VerticalLayoutDescription):
        expected_components = set([VerticalLayout])
        non_existing_components = set([HorizontalLayout, GridLayout])
    else:
        expected_components = set([GridLayout])
        non_existing_components = set([HorizontalLayout, VerticalLayout])

    assert layout_components == expected_components
    assert non_existing_components.intersection(layout_components) == set()
