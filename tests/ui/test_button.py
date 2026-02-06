from ui.components.behavior import Action, Enabled, Hoverable, Pressable
from ui.components.content import Text
from ui.components.layout import Parent, RenderLayer, TextAlignment, TextAlignmentEnum, Transform
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame, TextStyle
from ui.primitives import Color, FrameDescription, InteractionColors, TextStyleDescription, Vec2
from ui.widgets import ButtonBundle


def test_default_text():
    text = ButtonBundle('text', lambda: ..., TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))), Vec2(x=50, y=50))
    text_components = list(text.components())

    expected_components = [Action, Text, TextStyle, TextAlignment, Transform, RenderLayer, Enabled, Hoverable, Pressable, Dirty]
    assert len(text_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in text_components)

    non_existing_components = [Parent, Background, Frame]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in text_components)


def test_full_panel():
    text = 'text'
    callback = lambda: ...
    text_style = TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20)))
    size = Vec2(x=50, y=50)
    position = Vec2(x=50, y=50)
    parent = 1
    layer = 1
    background_colors = InteractionColors(normal=Color(20, 20, 20))
    frame = FrameDescription(3, InteractionColors(normal=Color(20, 20, 200)))
    text_alignment = TextAlignmentEnum.center
    panel = ButtonBundle(text, callback, text_style, size, position, parent, layer, background_colors, frame, text_alignment)
    panel_components = list(panel.components())

    expected_components = [Action, Text, TextStyle, TextAlignment, Transform, RenderLayer, Enabled, Hoverable, Pressable, Dirty, Parent, Background, Frame]
    assert len(panel_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in panel_components)
