from core.primitives import Color
from ui.bundles import TextVisualBundle
from ui.components.content import Text
from ui.components.layout import Spacing, TextAlignment, HorizontalAlignment, VerticalAlignment
from ui.components.style import TextStyle
from ui.types import InteractionColors, TextStyleDescription


def test_default_text_visual():
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, None))
    text_components = list(text.components())

    expected_components = [Text, TextStyle, TextAlignment, Spacing]
    assert len(text_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in text_components)


def test_full_text_visual():
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))), HorizontalAlignment.center, VerticalAlignment.middle, 5, 7)
    text_components = list(text.components())

    expected_components = [Text, TextStyle, TextAlignment, Spacing]
    assert len(text_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in text_components)
