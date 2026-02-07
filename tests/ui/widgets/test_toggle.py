from core.primitives import Color, Vec2
from ui.bundles import ActivatableBundle, PointerBundle, RectTransformBundle, SurfaceBundle, TextVisualBundle, ToggleableBundle, WidgetCoreBundle
from ui.components.behavior import Enabled, Hoverable, Pressable, Toggleable, Toggled, Trigger
from ui.components.content import Text
from ui.components.layout import Parent, RenderLayer, TextAlignment, TextAlignmentEnum, Transform
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
    toggle_components = list(toggle.components())

    expected_components = [Enabled, Dirty, Text, TextStyle, TextAlignment, Transform, RenderLayer, Hoverable, Pressable, Trigger, Toggleable]
    assert len(toggle_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in toggle_components)

    non_existing_components = [Parent, Background, Frame]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in toggle_components)


def test_full_toggle():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))), TextAlignmentEnum.center)
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    surface = SurfaceBundle(InteractionColors(normal=Color(20, 20, 20)), FrameDescription(3, InteractionColors(normal=Color(20, 20, 200))))
    pointer = PointerBundle()
    activatable = ActivatableBundle(None)
    toggleable = ToggleableBundle(True)

    toggle = ToggleBundle(core, text, transform, surface, pointer, activatable, toggleable)
    toggle_components = list(toggle.components())

    expected_components = [Enabled, Dirty, Text, TextStyle, TextAlignment, Transform, RenderLayer, Parent, Background, Frame, Hoverable, Pressable, Trigger, Toggleable, Toggled]
    assert len(toggle_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in toggle_components)
