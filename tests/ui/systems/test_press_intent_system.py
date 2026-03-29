from adapters.input.events import MouseButton
from omniecs.world import WorldFactory
from ui.components.behavior import Hovered, PressIntent
from ui.resources.state import PointerState
from ui.systems.intent_system import PressIntentSystem


def test_no_press_intent():
    world = WorldFactory.create_empty_world()
    world.register_system(PressIntentSystem())
    world.set_resource(PointerState())

    world.spawn(Hovered())
    world.execute()

    assert world.query_entities(all_of=(PressIntent,)) == set()

def test_hovered_press_intent():
    world = WorldFactory.create_empty_world()
    world.register_system(PressIntentSystem())
    world.set_resource(PointerState(buttons_pressed=set([MouseButton.left])))

    entity_id = world.spawn(Hovered())
    world.execute()

    assert entity_id in world.query_entities(all_of=(PressIntent,))

def test_not_hovered_press_intent():
    world = WorldFactory.create_empty_world()
    world.register_system(PressIntentSystem())
    world.set_resource(PointerState(buttons_pressed=set([MouseButton.left])))

    world.spawn()
    world.execute()

    assert world.query_entities(all_of=(PressIntent,)) == set()
