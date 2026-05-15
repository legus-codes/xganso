from omniecs.world import World, WorldFactory

from adapters.input.events import MouseButton
from ui.components.behavior import Hovered, Pressed
from ui.components.intent import ActivateIntent
from ui.resources.state import PointerState
from ui.systems.intent_system import ActivateIntentSystem


def create_world(pointer_state: PointerState) -> World:
    world = WorldFactory.create_empty_world()
    world.register_system(ActivateIntentSystem())
    world.set_resource(pointer_state)
    return world


def test_no_activate_intent():
    world = create_world(PointerState())

    entity_id = world.spawn(Hovered(), Pressed())
    world.execute()

    assert world.query_entities(none_of=(ActivateIntent,)) == set([entity_id])

def test_right_button_activate_intent():
    world = create_world(PointerState(buttons_released=set([MouseButton.right])))

    entity_id = world.spawn(Hovered(), Pressed())
    world.execute()

    assert world.query_entities(none_of=(ActivateIntent,)) == set([entity_id])

def test_hovered_and_pressed_activate_intent():
    world = create_world(PointerState(buttons_released=set([MouseButton.left])))

    entity_id = world.spawn(Hovered(), Pressed())
    world.execute()

    assert world.query_entities(all_of=(ActivateIntent,)) == set([entity_id])

def test_hovered_not_pressed_activated_intent():
    world = create_world(PointerState(buttons_released=set([MouseButton.left])))

    entity_id = world.spawn(Hovered())
    world.execute()

    assert world.query_entities(none_of=(ActivateIntent,)) == set([entity_id])

def test_pressed_not_hovered_activated_intent():
    world = create_world(PointerState(buttons_released=set([MouseButton.left])))

    entity_id = world.spawn(Pressed())
    world.execute()

    assert world.query_entities(none_of=(ActivateIntent,)) == set([entity_id])
