from core.primitives import Vec2
from ui.bundles import RectTransformBundle
from ui.components.layout import Parent, RenderLayer, Transform


def test_default_transform():
    transform = RectTransformBundle(Vec2(x=50, y=50))
    transform_components = set([type(component) for component in transform.components()])

    expected_components = set([Transform, RenderLayer])
    assert transform_components == expected_components

    non_existing_components = set([Parent])
    assert non_existing_components.intersection(transform_components) == set()


def test_full_transform():
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    transform_components = set([type(component) for component in transform.components()])

    expected_components = set([Transform, RenderLayer, Parent])
    assert transform_components == expected_components


def test_parent_entity_zero():
    transform = RectTransformBundle(Vec2(x=50, y=50), parent=0)
    transform_components = set([type(component) for component in transform.components()])

    assert Parent in transform_components
