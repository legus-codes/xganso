import pytest

from ui.components.behavior import Enabled
from ui.components.layout import GridLayout, HorizontalLayout, Layout, Parent, RenderLayer, Transform, VerticalLayout
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame
from ui.primitives import Color, FrameDescription, GridLayoutDescription, HorizontalLayoutDescription, InteractionColors, Vec2, VerticalLayoutDescription
from ui.widgets import PanelBundle


def test_default_panel():
    panel = PanelBundle(Vec2(x=50, y=50))
    panel_components = list(panel.components())

    expected_components = [Transform, RenderLayer, Enabled, Dirty]
    assert len(panel_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in panel_components)

    non_existing_components = [Parent, Background, Frame, Layout]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in panel_components)


def test_full_panel():
    size = Vec2(x=50, y=50)
    position = Vec2(x=50, y=50)
    parent = 1
    layer = 1
    background_colors = InteractionColors(normal=Color(20, 20, 20))
    frame = FrameDescription(3, InteractionColors(normal=Color(20, 20, 200)))
    layout = HorizontalLayoutDescription(10)
    panel = PanelBundle(size, position, parent, layer, background_colors, frame, layout)
    panel_components = list(panel.components())

    expected_components = [Transform, RenderLayer, Enabled, Dirty, Parent, Background, Frame, Layout]
    assert len(panel_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in panel_components)


def test_parent_entity_zero():
    panel = PanelBundle(Vec2(x=50, y=50), parent=0)
    panel_components = panel.components()

    assert any(isinstance(obj, Parent) for obj in panel_components)


def test_frame_zero_width():
    panel = PanelBundle(Vec2(x=50, y=50), frame=FrameDescription(0, InteractionColors(normal=Color(20, 20, 200))))
    panel_components = panel.components()

    assert not any(isinstance(obj, Frame) for obj in panel_components)


@pytest.mark.parametrize("layout", [HorizontalLayoutDescription(10), VerticalLayoutDescription(10), GridLayoutDescription(2, 2, 10, 10)])
def test_layout_variants(layout: Layout):
    panel = PanelBundle(Vec2(x=50, y=50), layout=layout)
    panel_components = panel.components()

    if isinstance(layout, HorizontalLayoutDescription):
        expected_component = HorizontalLayout
        non_existing_components = [VerticalLayout, GridLayout]
    elif isinstance(layout, VerticalLayoutDescription):
        expected_component = VerticalLayout
        non_existing_components = [HorizontalLayout, GridLayout]
    elif isinstance(layout, GridLayoutDescription):
        expected_component = GridLayout
        non_existing_components = [HorizontalLayout, VerticalLayout]

    assert any(isinstance(obj, expected_component) for obj in panel_components)
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in panel_components)


def test_multiple_instances():
    panel = PanelBundle(Vec2(x=50, y=50))
    components1 = list(panel.components())
    components2 = list(panel.components())

    for index, component in enumerate(components1):
        assert id(component) != id(components2[index])
