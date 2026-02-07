from core.primitives import Color, Vec2
from ui.bundles import PointerBundle, RectTransformBundle, SelectableBundle, SurfaceBundle, TextVisualBundle, WidgetCoreBundle
from ui.components.behavior import Enabled, Hoverable, Pressable, Selectable, Selected, SelectionGroup
from ui.components.content import Text
from ui.components.layout import Parent, RenderLayer, TextAlignment, TextAlignmentEnum, Transform
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame, TextStyle
from ui.types import FrameDescription, InteractionColors, TextStyleDescription
from ui.widgets import RadioButtonBundle


def test_default_radio_item():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))))
    transform = RectTransformBundle(Vec2(x=50, y=50))
    surface = SurfaceBundle()
    pointer = PointerBundle()
    selectable = SelectableBundle('group')

    radio_button = RadioButtonBundle(core, text, transform, surface, pointer, selectable)
    radio_button_components = list(radio_button.components())

    expected_components = [Enabled, Dirty, Text, TextStyle, TextAlignment, Transform, RenderLayer, Hoverable, Pressable, SelectionGroup, Selectable]
    assert len(radio_button_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in radio_button_components)

    non_existing_components = [Parent, Background, Frame, Selected]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in radio_button_components)


def test_full_toggle():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))), TextAlignmentEnum.center)
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    surface = SurfaceBundle(InteractionColors(normal=Color(20, 20, 20)), FrameDescription(3, InteractionColors(normal=Color(20, 20, 200))))
    pointer = PointerBundle()
    selectable = SelectableBundle('group', True)

    radio_button = RadioButtonBundle(core, text, transform, surface, pointer, selectable)
    radio_button_components = list(radio_button.components())

    expected_components = [Enabled, Dirty, Text, TextStyle, TextAlignment, Transform, RenderLayer, Parent, Background, Frame, Hoverable, Pressable, SelectionGroup, Selectable, Selected]
    assert len(radio_button_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in radio_button_components)
