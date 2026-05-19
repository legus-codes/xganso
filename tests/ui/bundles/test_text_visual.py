from core.primitives import Color
from ui.bundles import TextVisualBundle
from ui.components.content import Text
from ui.components.layout import Spacing, TextAlignment, HorizontalAlignment, VerticalAlignment
from ui.components.style import TextStyle
from ui.types import TextStyleDescription


def test_default_text_visual():
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, None))
    text_components = set([type(component) for component in text.components()])

    expected_components = set([Text, TextStyle, TextAlignment, Spacing])
    assert text_components == expected_components


def test_full_text_visual():
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, Color(20, 20, 20)), HorizontalAlignment.center, VerticalAlignment.middle, 5, 7)
    text_components = set([type(component) for component in text.components()])

    expected_components = set([Text, TextStyle, TextAlignment, Spacing])
    assert text_components == expected_components
