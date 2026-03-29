from omniecs.world import WorldFactory
from ui.components.behavior import Enabled, PressIntent, Pressed
from ui.systems.behaviour_system import PressSystem


def test_no_press_intention():
    world = WorldFactory.create_world()
    world.register_system(PressSystem())

    world.spawn(Enabled())
    world.execute()

    assert world.query_entities(all_of=(Pressed,)) == set()

def test_with_press_intent():
    world = WorldFactory.create_empty_world()
    world.register_system(PressSystem())    

    entity_id1 = world.spawn(PressIntent())
    entity_id2 = world.spawn(PressIntent())
    world.execute()

    assert world.query_entities(all_of=(Pressed,)) == set([entity_id1, entity_id2])

def test_pressed_is_cleared_after_execute():
    world = WorldFactory.create_world()
    world.register_system(PressSystem())    

    world.spawn(Pressed())
    world.spawn(Pressed())
    world.execute()

    assert world.query_entities(all_of=(Pressed,)) == set()
