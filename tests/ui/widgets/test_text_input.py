from core.primitives import Color, Vec2
from ui.bundles import InputBundle, PointerBundle, RectTransformBundle, SurfaceBundle, TextVisualBundle, WidgetCoreBundle
from ui.components.behavior import Enabled, Focusable, Hoverable, InputFilter, Pressable
from ui.components.content import InputValue, Text
from ui.components.layout import Parent, RenderLayer, Spacing, TextAlignment, HorizontalAlignment, Transform, VerticalAlignment
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame, TextStyle
from ui.types import FrameDescription, InteractionColors, TextStyleDescription
from ui.widgets import TextInputBundle


def test_default_text_input():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))))
    transform = RectTransformBundle(Vec2(x=50, y=50))
    surface = SurfaceBundle()
    pointer = PointerBundle()
    inputable = InputBundle('value', {'a'})
    
    text_input = TextInputBundle(core, text, transform, surface, pointer, inputable)
    text_input_components = list(text_input.components())

    expected_components = [Enabled, Dirty, Text, TextStyle, TextAlignment, Spacing, Transform, RenderLayer, Hoverable, Pressable, Focusable, InputValue, InputFilter]
    assert len(text_input_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in text_input_components)

    non_existing_components = [Parent, Background, Frame]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in text_input_components)


def test_full_toggle():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))), HorizontalAlignment.center, VerticalAlignment.middle, 6, 8)
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    surface = SurfaceBundle(InteractionColors(normal=Color(20, 20, 20)), FrameDescription(3, InteractionColors(normal=Color(20, 20, 200))))
    pointer = PointerBundle()
    inputable = InputBundle('value', {'a'})

    text_input = TextInputBundle(core, text, transform, surface, pointer, inputable)
    text_input_components = list(text_input.components())

    expected_components = [Enabled, Dirty, Text, TextStyle, TextAlignment, Spacing, Transform, RenderLayer, Parent, Background, Frame, Hoverable, Pressable, Focusable, InputValue, InputFilter]
    assert len(text_input_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in text_input_components)
