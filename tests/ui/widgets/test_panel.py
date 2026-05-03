from core.primitives import Color, Vec2
from ui.bundles import PanelLayoutBundle, RectTransformBundle, SurfaceBundle, WidgetCoreBundle
from ui.components.behavior import Enabled
from ui.components.layout import GridLayout, HorizontalLayout, Layout, Parent, RenderLayer, Transform, VerticalLayout
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame
from ui.types import FrameDescription, HorizontalLayoutDescription, InteractionColors
from ui.widgets import PanelBundle


def test_default_panel():
    core = WidgetCoreBundle()
    transform = RectTransformBundle(Vec2(x=50, y=50))
    layout = PanelLayoutBundle()
    surface = SurfaceBundle()

    panel = PanelBundle(core, transform, layout, surface)
    panel_components = set([type(component) for component in panel.components()])

    expected_components = set([Enabled, Dirty, Transform, RenderLayer])
    assert panel_components == expected_components

    non_existing_components = set([Parent, Background, Frame, HorizontalLayout, VerticalLayout, GridLayout, Layout])
    assert non_existing_components.intersection(panel_components) == set()


def test_full_panel():
    core = WidgetCoreBundle()
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    layout = PanelLayoutBundle(HorizontalLayoutDescription(10))
    surface = SurfaceBundle(InteractionColors(normal=Color(20, 20, 20)), FrameDescription(3, InteractionColors(normal=Color(20, 20, 200))))

    panel = PanelBundle(core, transform, layout, surface)
    panel_components = set([type(component) for component in panel.components()])

    expected_components = set([Enabled, Dirty, Transform, RenderLayer, Parent, HorizontalLayout, Background, Frame])
    assert panel_components == expected_components

    non_existing_components = set([VerticalLayout, GridLayout])
    assert non_existing_components.intersection(panel_components) == set()
