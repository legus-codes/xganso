from omniecs.world import WorldFactory
from ui.components.behavior import ActivateIntent, Trigger, Triggered
from ui.systems.behaviour_system import ActivateSystem


def test_press_intent():
    world = WorldFactory.create_empty_world()
    world.register_system(ActivateSystem())    

    entity_id1 = world.spawn(ActivateIntent(), Trigger(None))
    entity_id2 = world.spawn(ActivateIntent(), Trigger(None))
    world.execute()

    assert world.query_entities(all_of=(Triggered,)) == set([entity_id1, entity_id2])

def test_no_press_intention():
    world = WorldFactory.create_world()
    world.register_system(ActivateSystem())

    world.spawn(Trigger(None))
    world.execute()

    assert world.query_entities(all_of=(Triggered,)) == set()

def test_no_trigger():
    world = WorldFactory.create_world()
    world.register_system(ActivateSystem())

    world.spawn(ActivateIntent())
    world.execute()

    assert world.query_entities(all_of=(Triggered,)) == set()

def test_Triggered_is_cleared_after_execute():
    world = WorldFactory.create_world()
    world.register_system(ActivateSystem())    

    world.spawn(Triggered())
    world.spawn(Triggered())
    world.execute()

    assert world.query_entities(all_of=(Triggered,)) == set()
