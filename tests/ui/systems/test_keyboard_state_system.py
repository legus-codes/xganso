from adapters.input.events import Key, KeyDown, KeyUp, MouseMove, TextInput
from core.primitives import IVec2
from ecs_framework.types import ExecutionStage
from ecs_framework.world import WorldFactory
from ui.resources.state import KeyboardState
from ui.systems.input_system import KeyboardStateSystem


def test_unrelated_event():
    world = WorldFactory.create_world()
    world.register_system(KeyboardStateSystem(), ExecutionStage.update)
    world.set_resource(KeyboardState())

    world.push_event(MouseMove(IVec2(5, 5)))
    world.execute(0)
    
    keyboard_state = world.get_resource(KeyboardState)
    assert keyboard_state.keys_down == set()
    assert keyboard_state.keys_pressed == set()
    assert keyboard_state.keys_released == set()
    assert keyboard_state.text_input == []

def test_key_down_event():
    world = WorldFactory.create_world()
    world.register_system(KeyboardStateSystem(), ExecutionStage.update)
    world.set_resource(KeyboardState())

    world.push_event(KeyDown(Key.DELETE))
    world.execute(0)
    
    keyboard_state = world.get_resource(KeyboardState)
    assert keyboard_state.keys_down == set([Key.DELETE])
    assert keyboard_state.keys_pressed == set([Key.DELETE])
    assert keyboard_state.keys_released == set()
    assert keyboard_state.text_input == []

def test_key_up_event():
    world = WorldFactory.create_world()
    world.register_system(KeyboardStateSystem(), ExecutionStage.update)
    world.set_resource(KeyboardState())

    world.push_event(KeyUp(Key.ENTER))
    world.execute(0)
    
    keyboard_state = world.get_resource(KeyboardState)
    assert keyboard_state.keys_down == set()
    assert keyboard_state.keys_pressed == set()
    assert keyboard_state.keys_released == set([Key.ENTER])
    assert keyboard_state.text_input == []

def test_keyboard_click():
    world = WorldFactory.create_world()
    world.register_system(KeyboardStateSystem(), ExecutionStage.update)
    world.set_resource(KeyboardState())

    world.push_event(KeyDown(Key.DELETE))
    world.execute(0)
    
    keyboard_state = world.get_resource(KeyboardState)
    assert keyboard_state.keys_down == set([Key.DELETE])
    assert keyboard_state.keys_pressed == set([Key.DELETE])
    assert keyboard_state.keys_released == set()
    assert keyboard_state.text_input == []

    world.execute(0)
    
    keyboard_state = world.get_resource(KeyboardState)
    assert keyboard_state.keys_down == set([Key.DELETE])
    assert keyboard_state.keys_pressed == set()
    assert keyboard_state.keys_released == set()
    assert keyboard_state.text_input == []

    world.push_event(KeyUp(Key.DELETE))
    world.execute(0)
    
    keyboard_state = world.get_resource(KeyboardState)
    assert keyboard_state.keys_down == set()
    assert keyboard_state.keys_pressed == set()
    assert keyboard_state.keys_released == set([Key.DELETE])
    assert keyboard_state.text_input == []

def test_text_input_event():
    world = WorldFactory.create_world()
    world.register_system(KeyboardStateSystem(), ExecutionStage.update)
    world.set_resource(KeyboardState())

    world.push_event(TextInput('text'))
    world.execute(0)

    keyboard_state = world.get_resource(KeyboardState)
    assert keyboard_state.keys_down == set()
    assert keyboard_state.keys_pressed == set()
    assert keyboard_state.keys_released == set()
    assert keyboard_state.text_input == ['text']
