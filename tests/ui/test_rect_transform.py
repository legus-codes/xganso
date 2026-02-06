from ui.components.layout import Parent, RenderLayer, Transform
from ui.primitives import Vec2
from ui.widgets import RectTransformBundle


def test_default_transform():
    transform = RectTransformBundle(Vec2(x=50, y=50))
    transform_components = list(transform.components())

    expected_components = [Transform, RenderLayer]
    assert len(transform_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in transform_components)

    non_existing_components = [Parent]
    for component in non_existing_components:
        assert not any(isinstance(obj, component) for obj in transform_components)


def test_full_transform():
    transform = RectTransformBundle(Vec2(x=50, y=50), Vec2(x=50, y=50), 1, 1)
    transform_components = list(transform.components())

    expected_components = [Transform, RenderLayer, Parent]
    assert len(transform_components) == len(expected_components)
    for component in expected_components:
        assert any(isinstance(obj, component) for obj in transform_components)


def test_parent_entity_zero():
    transform = RectTransformBundle(Vec2(x=50, y=50), parent=0)
    transform_components = list(transform.components())

    assert any(isinstance(obj, Parent) for obj in transform_components)
