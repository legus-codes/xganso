from ui.components.behavior import Enabled, Hoverable, Pressable, Trigger
from ui.components.content import Text
from ui.components.layout import Parent, RenderLayer, TextAlignment, TextAlignmentEnum, Transform
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame, TextStyle
from ui.primitives import Color, FrameDescription, InteractionColors, TextStyleDescription, Vec2
from ui.widgets import ButtonBundle, InteractableBundle, RectTransformBundle, SurfaceBundle, TextVisualBundle, WidgetCoreBundle


def test_default_button():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))))
    transform = RectTransformBundle(Vec2(x=50, y=50))
    decoration = SurfaceBundle()
    interactable = InteractableBundle(None)

    button = ButtonBundle(core, text, transform, decoration, interactable)
    button_components = list(button.components())

    expected_components = [Enabled, Dirty, Text, TextStyle, TextAlignment, Transform, RenderLayer, Hoverable, Pressable, Trigger]
    assert len(button_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in button_components)

    non_existing_components = [Parent, Background, Frame]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in button_components)


def test_full_button():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))), TextAlignmentEnum.center)
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    decoration = SurfaceBundle(InteractionColors(normal=Color(20, 20, 20)), FrameDescription(3, InteractionColors(normal=Color(20, 20, 200))))
    interactable = InteractableBundle(None)

    button = ButtonBundle(core, text, transform, decoration, interactable)
    button_components = list(button.components())

    expected_components = [Enabled, Dirty, Text, TextStyle, TextAlignment, Transform, RenderLayer, Parent, Background, Frame, Hoverable, Pressable, Trigger]
    assert len(button_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in button_components)
