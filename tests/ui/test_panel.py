from ui.components.behavior import Enabled
from ui.components.layout import Layout, Parent, RenderLayer, Transform
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame
from ui.primitives import Color, FrameDescription, HorizontalLayoutDescription, InteractionColors, Vec2
from ui.widgets import PanelBundle, PanelLayoutBundle, RectTransformBundle, SurfaceBundle, WidgetCoreBundle


def test_default_panel():
    core = WidgetCoreBundle()
    transform = RectTransformBundle(Vec2(x=50, y=50))
    layout = PanelLayoutBundle()
    decoration = SurfaceBundle()

    panel = PanelBundle(core, transform, layout, decoration)
    panel_components = list(panel.components())

    expected_components = [Enabled, Dirty, Transform, RenderLayer]
    assert len(panel_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in panel_components)

    non_existing_components = [Parent, Background, Frame, Layout]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in panel_components)


def test_full_panel():
    core = WidgetCoreBundle()
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    layout = PanelLayoutBundle(HorizontalLayoutDescription(10))
    decoration = SurfaceBundle(InteractionColors(normal=Color(20, 20, 20)), FrameDescription(3, InteractionColors(normal=Color(20, 20, 200))))

    panel = PanelBundle(core, transform, layout, decoration)
    panel_components = list(panel.components())

    expected_components = [Enabled, Dirty, Transform, RenderLayer, Parent, Layout, Background, Frame]
    assert len(panel_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in panel_components)
