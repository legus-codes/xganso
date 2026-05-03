from core.primitives import Color, Vec2
from ui.bundles import ActivatableBundle, PressableBundle, PressableBundle, RectTransformBundle, SurfaceBundle, TextVisualBundle, WidgetCoreBundle
from ui.components.behavior import Enabled, Pressable, Pressable, Trigger
from ui.components.content import Text
from ui.components.layout import Parent, RenderLayer, Spacing, TextAlignment, HorizontalAlignment, Transform, VerticalAlignment
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame, TextStyle
from ui.types import FrameDescription, InteractionColors, TextStyleDescription
from ui.widgets import ButtonBundle


def test_default_button():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))))
    transform = RectTransformBundle(Vec2(x=50, y=50))
    surface = SurfaceBundle()
    pointer = PressableBundle()
    pressable = PressableBundle()
    activatable = ActivatableBundle(None)

    button = ButtonBundle(core, text, transform, surface, pointer, pressable, activatable)
    button_components = set([type(component) for component in button.components()])

    expected_components = set([Enabled, Dirty, Text, TextStyle, TextAlignment, Spacing, Transform, RenderLayer, Pressable, Pressable, Trigger])
    assert button_components == expected_components

    non_existing_components = set([Parent, Background, Frame])
    assert non_existing_components.intersection(button_components) == set()


def test_full_button():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))), HorizontalAlignment.center, VerticalAlignment.middle, 3, 5)
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    surface = SurfaceBundle(InteractionColors(normal=Color(20, 20, 20)), FrameDescription(3, InteractionColors(normal=Color(20, 20, 200))))
    pointer = PressableBundle()
    pressable = PressableBundle()
    activatable = ActivatableBundle(None)

    button = ButtonBundle(core, text, transform, surface, pointer, pressable, activatable)
    button_components = set([type(component) for component in button.components()])

    expected_components = set([Enabled, Dirty, Text, TextStyle, TextAlignment, Spacing, Transform, RenderLayer, Parent, Background, Frame, Pressable, Pressable, Trigger])
    assert button_components == expected_components
