import pytest

from ui.components.layout import GridLayout, HorizontalLayout, Layout, VerticalLayout
from ui.types import GridLayoutDescription, HorizontalLayoutDescription, LayoutDescription, VerticalLayoutDescription
from ui.widgets import PanelLayoutBundle


def test_default_panel_layout():
    layout = PanelLayoutBundle()
    layout_components = list(layout.components())

    expected_components = []
    assert len(layout_components) == len(expected_components)

    non_existing_components = [Layout, HorizontalLayout, VerticalLayout, GridLayout]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in layout_components)

@pytest.mark.parametrize("layout_description", [HorizontalLayoutDescription(10), VerticalLayoutDescription(10), GridLayoutDescription(2, 2, 10, 10)])
def test_panel_layout_variants(layout_description: LayoutDescription):
    layout = PanelLayoutBundle(layout_description)
    layout_components = list(layout.components())

    if isinstance(layout_description, HorizontalLayoutDescription):
        expected_component = HorizontalLayout
        non_existing_components = [VerticalLayout, GridLayout]
    elif isinstance(layout_description, VerticalLayoutDescription):
        expected_component = VerticalLayout
        non_existing_components = [HorizontalLayout, GridLayout]
    else:
        expected_component = GridLayout
        non_existing_components = [HorizontalLayout, VerticalLayout]

    assert any(isinstance(obj, expected_component) for obj in layout_components)
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in layout_components)
