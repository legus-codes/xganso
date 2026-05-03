from omniecs.world import World, WorldFactory
from ui.components.behavior import ActivateIntent, Pressed, Trigger, Triggered
from ui.components.rendering import Dirty
from ui.resources.state import WidgetState
from ui.systems.behaviour_system import ActivateSystem


def create_world() -> World:
    world = WorldFactory.create_empty_world()
    world.set_resource(WidgetState())
    world.register_system(ActivateSystem())
    return world


def test_activate_intent():
    world = create_world() 

    entity_id1 = world.spawn(ActivateIntent(), Trigger(None), Pressed())
    entity_id2 = world.spawn(ActivateIntent(), Trigger(None))
    world.execute()

    assert world.query_entities(all_of=(Triggered, Dirty), none_of=(Pressed,)) == set([entity_id1, entity_id2])

def test_no_activate_intention():
    world = create_world()

    world.spawn(Trigger(None))
    world.execute()

    assert world.query_entities(all_of=(Triggered,)) == set()

def test_no_trigger():
    world = create_world()

    world.spawn(ActivateIntent())
    world.execute()

    assert world.query_entities(all_of=(Triggered,)) == set()

def test_active_entities_clear():
    world = create_world()

    entity_id = world.spawn(ActivateIntent(), Trigger(None), Pressed())
    widgets = world.get_resource(WidgetState)
    widgets.active_entities.add(entity_id)
    world.set_resource(widgets)
    assert widgets.active_entities == set([entity_id])

    world.execute()

    widgets = world.get_resource(WidgetState)
    assert widgets.active_entities == set()


def test_triggered_is_cleared_after_execute():
    world = WorldFactory.create_world()
    world.set_resource(WidgetState())
    world.register_system(ActivateSystem())    

    world.spawn(Triggered())
    world.spawn(Triggered())
    world.execute()

    assert world.query_entities(all_of=(Triggered,)) == set()
