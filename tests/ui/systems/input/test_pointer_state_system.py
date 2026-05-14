from omniecs.world import World, WorldFactory

from adapters.input.events import Key, KeyDown, MouseButton, MouseButtonDown, MouseButtonUp, MouseMove
from core.primitives import IVec2
from ui.resources.state import PointerState
from ui.systems.input_system import PointerStateSystem


def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(PointerStateSystem())
    world.set_resource(PointerState())
    return world

def test_unrelated_event():
    world = create_world()

    world.push_event(KeyDown(Key.DELETE))
    world.execute()
    
    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(0, 0)
    assert pointer_state.buttons_down == set()
    assert pointer_state.buttons_pressed == set()
    assert pointer_state.buttons_released == set()

def test_mouse_move_event():
    world = create_world()

    world.push_event(MouseMove(IVec2(5, 5)))
    world.execute()
    
    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(5, 5)
    assert pointer_state.buttons_down == set()
    assert pointer_state.buttons_pressed == set()
    assert pointer_state.buttons_released == set()

def test_mouse_button_down_event():
    world = create_world()

    world.push_event(MouseButtonDown(IVec2(2, 7), MouseButton.left))
    world.execute()
    
    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(2, 7)
    assert pointer_state.buttons_down == set([MouseButton.left])
    assert pointer_state.buttons_pressed == set([MouseButton.left])
    assert pointer_state.buttons_released == set()

def test_mouse_button_up_event():
    world = create_world()

    world.push_event(MouseButtonUp(IVec2(7, 2), MouseButton.right))
    world.execute()
    
    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(7, 2)
    assert pointer_state.buttons_down == set()
    assert pointer_state.buttons_pressed == set()
    assert pointer_state.buttons_released == set([MouseButton.right])

def test_mouse_click():
    world = create_world()

    world.push_event(MouseButtonDown(IVec2(2, 7), MouseButton.left))
    world.execute()
    
    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(2, 7)
    assert pointer_state.buttons_down == set([MouseButton.left])
    assert pointer_state.buttons_pressed == set([MouseButton.left])
    assert pointer_state.buttons_released == set()

    world.execute()

    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(2, 7)
    assert pointer_state.buttons_down == set([MouseButton.left])
    assert pointer_state.buttons_pressed == set()
    assert pointer_state.buttons_released == set()

    world.push_event(MouseButtonUp(IVec2(7, 2), MouseButton.left))
    world.execute()
    
    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(7, 2)
    assert pointer_state.buttons_down == set()
    assert pointer_state.buttons_pressed == set()
    assert pointer_state.buttons_released == set([MouseButton.left])
