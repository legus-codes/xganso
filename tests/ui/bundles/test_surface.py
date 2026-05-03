from core.primitives import Color
from ui.bundles import SurfaceBundle
from ui.components.style import Background, Frame
from ui.types import FrameDescription, InteractionColors


def test_default_surface():
    surface = SurfaceBundle()
    surface_components = set([type(component) for component in surface.components()])

    expected_components = set()
    assert surface_components == expected_components

    non_existing_components = set([Background, Frame])
    assert non_existing_components.intersection(surface_components) == set()


def test_full_surface():
    surface = SurfaceBundle(InteractionColors(normal=Color(20, 20, 20)), FrameDescription(3, InteractionColors(normal=Color(20, 20, 200))))
    surface_components = set([type(component) for component in surface.components()])

    expected_components = set([Background, Frame])
    assert surface_components == expected_components


def test_frame_zero_width():
    surface = SurfaceBundle(frame=FrameDescription(0, InteractionColors(normal=Color(20, 20, 200))))
    surface_components = set([type(component) for component in surface.components()])

    assert Frame not in surface_components
