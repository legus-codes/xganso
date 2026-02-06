from ui.components.style import Background, Frame
from ui.primitives import Color, FrameDescription, InteractionColors
from ui.widgets import SurfaceBundle


def test_default_surface():
    decoration = SurfaceBundle()
    decoration_components = list(decoration.components())

    expected_components = []
    assert len(decoration_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in decoration_components)

    non_existing_components = [Background, Frame]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in decoration_components)


def test_full_surface():
    decoration = SurfaceBundle(InteractionColors(normal=Color(20, 20, 20)), FrameDescription(3, InteractionColors(normal=Color(20, 20, 200))))
    decoration_components = list(decoration.components())

    expected_components = [Background, Frame]
    assert len(decoration_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in decoration_components)


def test_frame_zero_width():
    decoration = SurfaceBundle(frame=FrameDescription(0, InteractionColors(normal=Color(20, 20, 200))))
    decoration_components = decoration.components()

    assert not any(isinstance(obj, Frame) for obj in decoration_components)
