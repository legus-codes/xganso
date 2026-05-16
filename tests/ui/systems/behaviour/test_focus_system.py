from omniecs.world import World, WorldFactory

from core.primitives import Color
from ui.components.behavior import Focusable, Focused
from ui.components.command import SetTextColorCommand
from ui.components.intent import PressIntent
from ui.systems.behaviour_system import FocusSystem


def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(FocusSystem())
    return world

def test_no_press_intention():
    world = create_world()

    entity_id = world.spawn(Focusable())
    world.execute()

    assert world.query_entities(none_of=(Focused,)) == set([entity_id])

def test_no_focusable():
    world = create_world()

    entity_id = world.spawn(PressIntent())
    world.execute()

    assert world.query_entities(none_of=(Focused,)) == set([entity_id])

def test_focused_on_spawn():
    world = create_world()

    entity_id = world.spawn(Focusable(enter=[SetTextColorCommand(Color(0, 0, 0))]), Focused())
    world.execute()

    assert world.query_entities(all_of=(Focused, SetTextColorCommand)) == set([entity_id])

def test_add_focus():
    world = create_world()

    entity_id = world.spawn(Focusable(), PressIntent())
    world.execute()

    assert world.query_entities(all_of=(Focused,)) == set([entity_id])
    assert len(world.get_events()) == 0

def test_add_focused_with_command():
    world = create_world()

    entity_id = world.spawn(Focusable(enter=[SetTextColorCommand(Color(0, 0, 0))]), PressIntent())
    world.execute()

    assert world.query_entities(all_of=(Focused, SetTextColorCommand)) == set([entity_id])
    assert len(world.get_events()) == 0

def test_remove_focus():
    world = create_world()

    entity_id = world.spawn(Focusable(), Focused())
    world.execute()

    assert world.query_entities(none_of=(Focused,)) == set([entity_id])

def test_remove_focus_with_command():
    world = create_world()

    entity_id = world.spawn(Focusable(exit=[SetTextColorCommand(Color(0, 0, 0))]), Focused(), PressIntent())
    world.execute()

    assert world.query_entities(all_of=(SetTextColorCommand,), none_of=(Focused,)) == set([entity_id])
