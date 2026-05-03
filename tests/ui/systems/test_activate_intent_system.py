from adapters.input.events import MouseButton
from omniecs.world import World, WorldFactory
from ui.components.behavior import ActivateIntent, Hovered, Pressed
from ui.resources.state import PointerState
from ui.systems.intent_system import ActivateIntentSystem


def create_world(pointer_state: PointerState) -> World:
    world = WorldFactory.create_empty_world()
    world.register_system(ActivateIntentSystem())
    world.set_resource(pointer_state)
    return world


def test_no_activate_intent():
    world = create_world(PointerState())

    world.spawn(Hovered(), Pressed())
    world.execute()

    assert world.query_entities(all_of=(ActivateIntent,)) == set()

def test_hovered_and_pressed_activate_intent():
    world = create_world(PointerState(buttons_released=set([MouseButton.left])))

    entity_id = world.spawn(Hovered(), Pressed())
    world.execute()

    assert entity_id in world.query_entities(all_of=(ActivateIntent,))

def test_hovered_not_pressed_activated_intent():
    world = create_world(PointerState(buttons_released=set([MouseButton.left])))

    world.spawn(Hovered())
    world.execute()

    assert world.query_entities(all_of=(ActivateIntent,)) == set()

def test_not_hovered_pressed_activated_intent():
    world = create_world(PointerState(buttons_released=set([MouseButton.left])))

    world.spawn(Pressed())
    world.execute()

    assert world.query_entities(all_of=(ActivateIntent,)) == set()
