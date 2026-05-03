from core.primitives import Color, Vec2
from ui.bundles import ActivatableBundle, PointerBundle, RectTransformBundle, SurfaceBundle, TextVisualBundle, ToggleableBundle, WidgetCoreBundle
from ui.components.behavior import Enabled, Hoverable, Toggleable, Toggled, Trigger
from ui.components.content import Text
from ui.components.layout import Parent, RenderLayer, Spacing, TextAlignment, HorizontalAlignment, Transform, VerticalAlignment
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame, TextStyle
from ui.types import FrameDescription, InteractionColors, TextStyleDescription
from ui.widgets import ToggleBundle


def test_default_toggle():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))))
    transform = RectTransformBundle(Vec2(x=50, y=50))
    surface = SurfaceBundle()
    pointer = PointerBundle()
    activatable = ActivatableBundle(None)
    toggleable = ToggleableBundle()

    toggle = ToggleBundle(core, text, transform, surface, pointer, activatable, toggleable)
    toggle_components = set([type(component) for component in toggle.components()])

    expected_components = set([Enabled, Dirty, Text, TextStyle, TextAlignment, Spacing, Transform, RenderLayer, Hoverable, Trigger, Toggleable])
    assert toggle_components == expected_components

    non_existing_components = set([Parent, Background, Frame])
    assert non_existing_components.intersection(toggle_components) == set()


def test_full_toggle():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))), HorizontalAlignment.center, VerticalAlignment.middle, 8, 7)
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    surface = SurfaceBundle(InteractionColors(normal=Color(20, 20, 20)), FrameDescription(3, InteractionColors(normal=Color(20, 20, 200))))
    pointer = PointerBundle()
    activatable = ActivatableBundle(None)
    toggleable = ToggleableBundle(True)

    toggle = ToggleBundle(core, text, transform, surface, pointer, activatable, toggleable)
    toggle_components = set([type(component) for component in toggle.components()])

    expected_components = set([Enabled, Dirty, Text, TextStyle, TextAlignment, Spacing, Transform, RenderLayer, Parent, Background, Frame, Hoverable, Trigger, Toggleable, Toggled])
    assert toggle_components == expected_components
