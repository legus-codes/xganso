from core.primitives import Color, Vec2
from ui.bundles import RectTransformBundle, SurfaceBundle, TextVisualBundle, WidgetCoreBundle
from ui.components.behavior import Enabled
from ui.components.content import Text
from ui.components.layout import Parent, RenderLayer, Spacing, TextAlignment, HorizontalAlignment, Transform, VerticalAlignment
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame, TextStyle
from ui.types import FrameDescription, InteractionColors, TextStyleDescription
from ui.widgets import TextBundle


def test_default_text():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))))
    transform = RectTransformBundle(Vec2(x=50, y=50))
    surface = SurfaceBundle()

    text = TextBundle(core, text, transform, surface)
    text_components = list(text.components())

    expected_components = [Enabled, Dirty, Text, TextStyle, TextAlignment, Spacing, Transform, RenderLayer]
    assert len(text_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in text_components)

    non_existing_components = [Parent, Background, Frame]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in text_components)


def test_full_text():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))), HorizontalAlignment.center, VerticalAlignment.bottom, 5, 10)
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    surface = SurfaceBundle(InteractionColors(normal=Color(20, 20, 20)), FrameDescription(3, InteractionColors(normal=Color(20, 20, 200))))

    text = TextBundle(core, text, transform, surface)
    text_components = list(text.components())

    expected_components = [Enabled, Dirty, Text, TextStyle, TextAlignment, Spacing, Transform, RenderLayer, Parent, Background, Frame]
    assert len(text_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in text_components)
