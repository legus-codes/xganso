from omniecs.world import World, WorldFactory

from adapters.input.events import MouseButton
from ui.components.behavior import Hovered
from ui.components.intent import PressIntent
from ui.resources.state import PointerState
from ui.systems.intent_system import PressIntentSystem


def create_world(pointer_state: PointerState) -> World:
    world = WorldFactory.create_empty_world()
    world.register_system(PressIntentSystem())
    world.set_resource(pointer_state)
    return world

def test_no_press_intent():
    world = create_world(PointerState())

    world.spawn(Hovered())
    world.execute()

    assert world.query_entities(all_of=(PressIntent,)) == set()

def test_right_button_press_intent():
    world = create_world(PointerState(buttons_pressed=set([MouseButton.right])))

    world.spawn(Hovered())
    world.execute()

    assert world.query_entities(all_of=(PressIntent,)) == set()

def test_hovered_press_intent():
    world = create_world(PointerState(buttons_pressed=set([MouseButton.left])))

    entity_id = world.spawn(Hovered())
    world.execute()

    assert entity_id in world.query_entities(all_of=(PressIntent,))

def test_not_hovered_press_intent():
    world = create_world(PointerState(buttons_pressed=set([MouseButton.left])))

    world.spawn()
    world.execute()

    assert world.query_entities(all_of=(PressIntent,)) == set()
