from core.primitives import Color, Vec2
from ui.bundles import RectTransformBundle, SurfaceBundle, TextVisualBundle, WidgetCoreBundle
from ui.components.behavior import Enabled
from ui.components.content import Text
from ui.components.layout import Parent, RenderLayer, Spacing, TextAlignment, HorizontalAlignment, Transform, VerticalAlignment
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame, TextStyle
from ui.types import TextStyleDescription
from ui.widgets import TextBundle


def test_default_text():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, Color(20, 20, 20)))
    transform = RectTransformBundle(Vec2(x=50, y=50))
    surface = SurfaceBundle()

    text = TextBundle(core, text, transform, surface)
    text_components = set([type(component) for component in text.components()])

    expected_components = set([Enabled, Dirty, Text, TextStyle, TextAlignment, Spacing, Transform, RenderLayer])
    assert text_components == expected_components

    non_existing_components = set([Parent, Background, Frame])
    assert non_existing_components.intersection(text_components) == set()


def test_full_text():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, Color(20, 20, 20)), HorizontalAlignment.center, VerticalAlignment.bottom, 5, 10)
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    surface = SurfaceBundle(Color(20, 20, 20), Color(20, 20, 200), 3)

    text = TextBundle(core, text, transform, surface)
    text_components = set([type(component) for component in text.components()])

    expected_components = set([Enabled, Dirty, Text, TextStyle, TextAlignment, Spacing, Transform, RenderLayer, Parent, Background, Frame])
    assert text_components == expected_components
