from ui.components.content import Text
from ui.components.layout import TextAlignment, TextAlignmentEnum
from ui.components.style import TextStyle
from ui.primitives import Color, InteractionColors, TextStyleDescription
from ui.widgets import TextVisualBundle


def test_default_text_visual():
    text_visual = TextVisualBundle('text', TextStyleDescription('couriernew', 16, None))
    text_visual_components = list(text_visual.components())

    expected_components = [Text, TextStyle, TextAlignment]
    assert len(text_visual_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in text_visual_components)


def test_full_text_visual():
    text_visual = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))), TextAlignmentEnum.center)
    text_visual_components = list(text_visual.components())

    expected_components = [Text, TextStyle, TextAlignment]
    assert len(text_visual_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in text_visual_components)
