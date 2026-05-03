from omniecs.world import World, WorldFactory
from ui.components.behavior import Hovered, PressIntent, Pressable, Pressed
from ui.components.rendering import Dirty
from ui.resources.state import WidgetState
from ui.systems.behaviour_system import PressSystem

def create_world() -> World:
    world = WorldFactory.create_empty_world()
    world.register_system(PressSystem())
    world.set_resource(WidgetState())
    return world

def test_with_press_intent():
    world = create_world()

    entity_id1 = world.spawn(PressIntent(), Pressable(), Hovered())
    entity_id2 = world.spawn(PressIntent(), Pressable(), Hovered())
    world.execute()

    widgets = world.get_resource(WidgetState)
    assert world.query_entities(all_of=(Pressed, Dirty)) == set([entity_id1, entity_id2])
    assert widgets.active_entities == set([entity_id1, entity_id2])

def test_no_press_intention():
    world = create_world()

    world.spawn(Pressable(), Hovered())
    world.execute()

    widgets = world.get_resource(WidgetState)
    assert world.query_entities(all_of=(Pressed, Dirty)) == set()
    assert widgets.active_entities == set()

def test_no_presssable():
    world = create_world()

    world.spawn(PressIntent(), Hovered())
    world.execute()

    widgets = world.get_resource(WidgetState)
    assert world.query_entities(all_of=(Pressed, Dirty)) == set()
    assert widgets.active_entities == set()

def test_pressed_is_removed_if_not_hovered():
    world = create_world()

    entity_id1 = world.spawn(Pressed())
    entity_id2 = world.spawn(Pressed(), Hovered())
    world.execute()

    assert world.query_entities(all_of=(Pressed,)) == set([entity_id2])
    assert world.query_entities(all_of=(Dirty,), none_of=(Pressed,)) == set([entity_id1])

def test_pressed_is_added_if_active_entity():
    world = create_world()

    entity_id1 = world.spawn(Hovered(), Pressable())
    entity_id2 = world.spawn(Hovered(), Pressable(), Pressed())
    entity_id3 = world.spawn(Hovered(), Pressed())
    entity_id4 = world.spawn(Pressable(), Pressed())
    widgets = world.get_resource(WidgetState)
    widgets.active_entities.add(entity_id1)
    widgets.active_entities.add(entity_id2)
    widgets.active_entities.add(entity_id3)
    widgets.active_entities.add(entity_id4)
    world.execute()

    assert world.query_entities(all_of=(Pressed, Dirty)) == set([entity_id1])
    