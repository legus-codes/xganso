from omniecs.world import World, WorldFactory
from ui.components.behavior import Enabled, HoverIntent, Hovered
from ui.resources.state import WidgetState
from ui.systems.behaviour_system import HoverSystem

def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(HoverSystem())
    world.set_resource(WidgetState())
    return world

def test_no_hover_intention_or_hovered():
    world = create_world()

    world.spawn(Enabled())
    world.execute()

    widgets = world.get_resource(WidgetState)
    assert widgets.hovered_entities == set()
    assert world.query_entities(all_of=(Hovered,)) == set()

def test_adding_hover_intentions():
    world = create_world()

    entity_id1 = world.spawn(HoverIntent())
    entity_id2 = world.spawn(HoverIntent())
    world.execute()

    widgets = world.get_resource(WidgetState)
    assert widgets.hovered_entities == set([entity_id1, entity_id2])
    assert world.query_entities(all_of=(Hovered,)) == set([entity_id1, entity_id2])

def test_removing_hovered():
    world = create_world()

    entity_id1 = world.spawn(Enabled())
    entity_id2 = world.spawn(Enabled())
    world.set_resource(WidgetState(hovered_entities=set([entity_id1, entity_id2])))
    world.execute()

    widgets = world.get_resource(WidgetState)
    assert widgets.hovered_entities == set([])
    assert world.query_entities(all_of=(Hovered,)) == set([])

def test_changing_hovered():
    world = create_world()

    entity_id1 = world.spawn(Enabled())
    world.spawn(Enabled())
    entity_id3 = world.spawn(HoverIntent())
    world.set_resource(WidgetState(hovered_entities=set([entity_id1])))
    world.execute()

    widgets = world.get_resource(WidgetState)
    assert widgets.hovered_entities == set([entity_id3])
    assert world.query_entities(all_of=(Hovered,)) == set([entity_id3])
