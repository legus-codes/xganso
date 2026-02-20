from adapters.input.events import Key
from ui.resources.state import KeyboardState


def test_default_keyboard_state():
    keyboard = KeyboardState()
    assert keyboard.keys_down == set()
    assert keyboard.keys_pressed == set()
    assert keyboard.keys_released == set()
    assert keyboard.text_input == []

def test_keyboard_state_is_down():
    keyboard = KeyboardState(keys_down=set([Key.DELETE]))
    assert keyboard.is_down(Key.DELETE)

def test_keyboard_state_was_pressed():
    keyboard = KeyboardState(keys_pressed=set([Key.ENTER]))
    assert keyboard.was_pressed(Key.ENTER)

def test_keyboard_state_was_released():
    keyboard = KeyboardState(keys_released=set([Key.DELETE]))
    assert keyboard.was_released(Key.DELETE)

def test_keyboard_state_reset():
    keyboard = KeyboardState(keys_down=set([Key.DELETE]), keys_pressed=set([Key.ENTER]), keys_released=set([Key.DELETE]), text_input=['abc'])
    keyboard.reset()
    
    assert keyboard.is_down(Key.DELETE)
    assert not keyboard.was_pressed(Key.ENTER)
    assert not keyboard.was_released(Key.DELETE)
    assert keyboard.text_input == []
