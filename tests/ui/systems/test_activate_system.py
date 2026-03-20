from omniecs.world import WorldFactory
from ui.components.behavior import Enabled, ActivateIntent, Triggered
from ui.systems.behaviour_system import ActivateSystem


def test_no_press_intention():
    world = WorldFactory.create_world()
    world.register_system(ActivateSystem())

    world.spawn(Enabled())
    world.execute(0)

    assert world.query_entities(all_of=(Triggered,)) == set()

def test_with_press_intent():
    world = WorldFactory.create_empty_world()
    world.register_system(ActivateSystem())    

    entity_id1 = world.spawn(ActivateIntent())
    entity_id2 = world.spawn(ActivateIntent())
    world.execute(0)

    assert world.query_entities(all_of=(Triggered,)) == set([entity_id1, entity_id2])

def test_Triggered_is_cleared_after_execute():
    world = WorldFactory.create_world()
    world.register_system(ActivateSystem())    

    world.spawn(Triggered())
    world.spawn(Triggered())
    world.execute(0)

    assert world.query_entities(all_of=(Triggered,)) == set()
