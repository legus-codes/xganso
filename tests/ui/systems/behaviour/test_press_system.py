from omniecs.world import World, WorldFactory

from core.primitives import Color
from ui.components.behavior import Hovered, Pressable, Pressed
from ui.components.command import SetBackgroundColorCommand
from ui.components.intent import PressIntent
from ui.systems.behaviour_system import PressSystem


def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(PressSystem())
    return world

def test_no_press_intention():
    world = create_world()

    entity_id = world.spawn(Pressable(), Hovered())
    world.execute()

    assert world.query_entities(none_of=(Pressed,)) == set([entity_id])

def test_no_presssable():
    world = create_world()

    entity_id = world.spawn(PressIntent(), Hovered())
    world.execute()

    assert world.query_entities(none_of=(Pressed,)) == set([entity_id])

def test_no_hovered():
    world = create_world()

    entity_id = world.spawn(Pressable(), PressIntent())
    world.execute()

    assert world.query_entities(none_of=(Pressed,)) == set([entity_id])

def test_add_pressed():
    world = create_world()

    entity_id = world.spawn(Pressable(), Hovered(), PressIntent())
    world.execute()

    assert world.query_entities(all_of=(Pressed,)) == set([entity_id])

def test_add_pressed_with_command():
    world = create_world()

    entity_id = world.spawn(Pressable(enter=[SetBackgroundColorCommand(Color(0, 0, 0))]), Hovered(), PressIntent())
    world.execute()

    assert world.query_entities(all_of=(Pressed, SetBackgroundColorCommand)) == set([entity_id])

def test_keep_pressed_if_hovered():
    world = create_world()

    entity_id = world.spawn(Pressable(), Hovered(), Pressed())
    world.execute()

    assert world.query_entities(all_of=(Pressed,)) == set([entity_id])

def test_remove_pressed_if_not_hovered():
    world = create_world()

    entity_id = world.spawn(Pressable(), Pressed())
    world.execute()

    assert world.query_entities(none_of=(Pressed,)) == set([entity_id])

def test_remove_pressed_if_not_hovered_with_command():
    world = create_world()

    entity_id = world.spawn(Pressable(exit=[SetBackgroundColorCommand(Color(0, 0, 0))]), Pressed())
    world.execute()

    assert world.query_entities(all_of=(SetBackgroundColorCommand,), none_of=(Pressed,)) == set([entity_id])
    