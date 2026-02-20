from adapters.input.events import MouseButton
from core.primitives import IVec2
from ui.resources.state import PointerState


def test_default_pointer_state():
    pointer = PointerState()
    assert pointer.position == IVec2(0, 0)
    assert pointer.buttons_down == set()
    assert pointer.buttons_pressed == set()
    assert pointer.buttons_released == set()

def test_pointer_state_is_down():
    pointer = PointerState(buttons_down=set([MouseButton.left]))
    assert pointer.is_down(MouseButton.left)

def test_pointer_state_was_pressed():
    pointer = PointerState(buttons_pressed=set([MouseButton.right]))
    assert pointer.was_pressed(MouseButton.right)

def test_pointer_state_was_released():
    pointer = PointerState(buttons_released=set([MouseButton.left]))
    assert pointer.was_released(MouseButton.left)

def test_pointer_state_reset():
    pointer = PointerState(buttons_down=set([MouseButton.left]), buttons_pressed=set([MouseButton.right]), buttons_released=set([MouseButton.left]))
    pointer.reset()
    assert pointer.is_down(MouseButton.left)
    assert not pointer.was_pressed(MouseButton.right)
    assert not pointer.was_released(MouseButton.left)
