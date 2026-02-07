from core.primitives import Color
from ui.bundles import SurfaceBundle
from ui.components.style import Background, Frame
from ui.types import FrameDescription, InteractionColors


def test_default_surface():
    surface = SurfaceBundle()
    surface_components = list(surface.components())

    expected_components = []
    assert len(surface_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in surface_components)

    non_existing_components = [Background, Frame]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in surface_components)


def test_full_surface():
    surface = SurfaceBundle(InteractionColors(normal=Color(20, 20, 20)), FrameDescription(3, InteractionColors(normal=Color(20, 20, 200))))
    surface_components = list(surface.components())

    expected_components = [Background, Frame]
    assert len(surface_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in surface_components)


def test_frame_zero_width():
    surface = SurfaceBundle(frame=FrameDescription(0, InteractionColors(normal=Color(20, 20, 200))))
    surface_components = surface.components()

    assert not any(isinstance(obj, Frame) for obj in surface_components)
