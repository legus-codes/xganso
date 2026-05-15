from omniecs.world import World, WorldFactory

from core.primitives import Color
from ui.components.behavior import Enabled, Pressable, Pressed, Trigger, Triggered
from ui.components.command import SetBackgroundColorCommand, SetFrameColorCommand
from ui.components.intent import ActivateIntent
from ui.components.rendering import Dirty
from ui.systems.behaviour_system import ActivateSystem


def create_world() -> World:
    world = WorldFactory.create_empty_world()
    world.register_system(ActivateSystem())
    return world


def test_no_activate_intention():
    world = create_world()

    entity_id = world.spawn(Pressable(), Trigger())
    world.execute()

    assert world.query_entities(none_of=(Triggered,)) == set([entity_id])

def test_no_trigger():
    world = create_world()

    entity_id = world.spawn(Pressable(), ActivateIntent())
    world.execute()

    assert world.query_entities(none_of=(Triggered,)) == set([entity_id])

def test_no_pressable():
    world = create_world()

    entity_id = world.spawn(Trigger(), ActivateIntent())
    world.execute()

    assert world.query_entities(none_of=(Triggered,)) == set([entity_id])

def test_add_triggered():
    world = create_world() 

    entity_id1 = world.spawn(Pressable(), Trigger(), ActivateIntent(), Pressed())
    entity_id2 = world.spawn(Pressable(), Trigger(), ActivateIntent())
    world.execute()

    assert world.query_entities(all_of=(Triggered,), none_of=(Pressed,)) == set([entity_id1, entity_id2])

def test_add_triggered_with_command():
    world = create_world() 

    entity_id = world.spawn(Pressable(exit=[SetFrameColorCommand(Color(0, 0, 0))]),
                            Trigger(commands=[SetBackgroundColorCommand(Color(0, 0, 0))]),
                            ActivateIntent(),
                            Pressed())
    world.execute()

    assert world.query_entities(all_of=(Triggered, SetFrameColorCommand, SetBackgroundColorCommand)) == set([entity_id])


def test_triggered_is_cleared_after_execute():
    world = WorldFactory.create_world()
    world.register_system(ActivateSystem())    

    entity_id = world.spawn(Enabled(), Triggered())
    world.execute()

    assert world.query_entities(none_of=(Triggered,)) == set([entity_id])
