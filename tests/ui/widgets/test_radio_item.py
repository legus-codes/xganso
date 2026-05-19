from core.primitives import Color, Vec2
from ui.bundles import HoverableBundle, RectTransformBundle, SelectableBundle, SurfaceBundle, TextVisualBundle, WidgetCoreBundle
from ui.components.behavior import Enabled, Hoverable, Selectable, Selected, SelectionGroup
from ui.components.content import Text
from ui.components.layout import Parent, RenderLayer, Spacing, TextAlignment, HorizontalAlignment, Transform, VerticalAlignment
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame, TextStyle
from ui.types import TextStyleDescription
from ui.widgets import RadioButtonBundle


def test_default_radio_item():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, Color(20, 20, 20)))
    transform = RectTransformBundle(Vec2(x=50, y=50))
    surface = SurfaceBundle()
    pointer = HoverableBundle()
    selectable = SelectableBundle('group')

    radio_button = RadioButtonBundle(core, text, transform, surface, pointer, selectable)
    radio_button_components = set([type(component) for component in radio_button.components()])

    expected_components = set([Enabled, Dirty, Text, TextStyle, TextAlignment, Spacing, Transform, RenderLayer, Hoverable, SelectionGroup, Selectable])
    assert radio_button_components == expected_components

    non_existing_components = set([Parent, Background, Frame, Selected])
    assert non_existing_components.intersection(radio_button_components) == set()


def test_full_toggle():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, Color(20, 20, 20)), HorizontalAlignment.center, VerticalAlignment.middle, 5, 7)
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    surface = SurfaceBundle(Color(20, 20, 20), Color(20, 20, 200), 3)
    pointer = HoverableBundle()
    selectable = SelectableBundle('group', True)

    radio_button = RadioButtonBundle(core, text, transform, surface, pointer, selectable)
    radio_button_components = set([type(component) for component in radio_button.components()])

    expected_components = set([Enabled, Dirty, Text, TextStyle, TextAlignment, Spacing, Transform, RenderLayer, Parent, Background, Frame, Hoverable, SelectionGroup, Selectable, Selected])
    assert radio_button_components == expected_components
