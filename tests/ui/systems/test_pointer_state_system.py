from adapters.input.events import Key, KeyDown, MouseButton, MouseButtonDown, MouseButtonUp, MouseMove
from core.primitives import IVec2
from ecs_framework.types import ExecutionStage
from ecs_framework.world import WorldFactory
from ui.resources.state import PointerState
from ui.systems.state import PointerStateSystem


def test_unrelated_event():
    world = WorldFactory.create_world()
    world.register_system(PointerStateSystem(), ExecutionStage.update)
    world.set_resource(PointerState())

    world.push_event(KeyDown(Key.DELETE))
    world.execute(0)
    
    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(0, 0)
    assert pointer_state.buttons_down == set()
    assert pointer_state.buttons_pressed == set()
    assert pointer_state.buttons_released == set()

def test_mouse_move_event():
    world = WorldFactory.create_world()
    world.register_system(PointerStateSystem(), ExecutionStage.update)
    world.set_resource(PointerState())

    world.push_event(MouseMove(IVec2(5, 5)))
    world.execute(0)
    
    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(5, 5)
    assert pointer_state.buttons_down == set()
    assert pointer_state.buttons_pressed == set()
    assert pointer_state.buttons_released == set()

def test_mouse_button_down_event():
    world = WorldFactory.create_world()
    world.register_system(PointerStateSystem(), ExecutionStage.update)
    world.set_resource(PointerState())

    world.push_event(MouseButtonDown(IVec2(2, 7), MouseButton.left))
    world.execute(0)
    
    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(2, 7)
    assert pointer_state.buttons_down == set([MouseButton.left])
    assert pointer_state.buttons_pressed == set([MouseButton.left])
    assert pointer_state.buttons_released == set()

def test_mouse_button_up_event():
    world = WorldFactory.create_world()
    world.register_system(PointerStateSystem(), ExecutionStage.update)
    world.set_resource(PointerState())

    world.push_event(MouseButtonUp(IVec2(7, 2), MouseButton.right))
    world.execute(0)
    
    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(7, 2)
    assert pointer_state.buttons_down == set()
    assert pointer_state.buttons_pressed == set()
    assert pointer_state.buttons_released == set([MouseButton.right])

def test_mouse_click():
    world = WorldFactory.create_world()
    world.register_system(PointerStateSystem(), ExecutionStage.update)
    world.set_resource(PointerState())

    world.push_event(MouseButtonDown(IVec2(2, 7), MouseButton.left))
    world.execute(0)
    
    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(2, 7)
    assert pointer_state.buttons_down == set([MouseButton.left])
    assert pointer_state.buttons_pressed == set([MouseButton.left])
    assert pointer_state.buttons_released == set()

    world.execute(0)

    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(2, 7)
    assert pointer_state.buttons_down == set([MouseButton.left])
    assert pointer_state.buttons_pressed == set()
    assert pointer_state.buttons_released == set()

    world.push_event(MouseButtonUp(IVec2(7, 2), MouseButton.left))
    world.execute(0)
    
    pointer_state = world.get_resource(PointerState)
    assert pointer_state.position == IVec2(7, 2)
    assert pointer_state.buttons_down == set()
    assert pointer_state.buttons_pressed == set()
    assert pointer_state.buttons_released == set([MouseButton.left])
