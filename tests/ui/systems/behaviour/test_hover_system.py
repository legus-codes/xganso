from omniecs.world import World, WorldFactory

from core.primitives import Color
from ui.components.behavior import Enabled, Hoverable, Hovered
from ui.components.command import SetFrameColorCommand
from ui.components.intent import HoverIntent
from ui.systems.behaviour_system import HoverSystem


def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(HoverSystem())
    return world

def test_no_hover_intention():
    world = create_world()

    entity_id = world.spawn(Enabled(), Hoverable())
    world.execute()

    assert world.query_entities(none_of=(Hovered,)) == set([entity_id])

def test_adding_hover_intentions():
    world = create_world()

    entity_id1 = world.spawn(Hoverable(), HoverIntent())
    entity_id2 = world.spawn(Hoverable(), HoverIntent())
    world.execute()

    assert world.query_entities(all_of=(Hovered,)) == set([entity_id1, entity_id2])

def test_adding_hover_intentions_with_command():
    world = create_world()

    entity_id1 = world.spawn(Hoverable(enter=[SetFrameColorCommand(Color(0, 0, 0))]), HoverIntent())
    entity_id2 = world.spawn(Hoverable(enter=[SetFrameColorCommand(Color(0, 0, 0))]), HoverIntent())
    world.execute()

    assert world.query_entities(all_of=(Hovered, SetFrameColorCommand)) == set([entity_id1, entity_id2])

def test_removing_hovered():
    world = create_world()

    entity_id1 = world.spawn(Enabled(), Hoverable(), Hovered())
    entity_id2 = world.spawn(Enabled(), Hoverable(), Hovered())
    world.execute()

    assert world.query_entities(none_of=(Hovered,)) == set([entity_id1, entity_id2])

def test_removing_hovered_with_command():
    world = create_world()

    entity_id1 = world.spawn(Enabled(), Hoverable(exit=[SetFrameColorCommand(Color(0, 0, 0))]), Hovered())
    entity_id2 = world.spawn(Enabled(), Hoverable(exit=[SetFrameColorCommand(Color(0, 0, 0))]), Hovered())
    world.execute()

    assert world.query_entities(all_of=(SetFrameColorCommand,), none_of=(Hovered,)) == set([entity_id1, entity_id2])
