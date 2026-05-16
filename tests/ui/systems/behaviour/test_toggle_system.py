from omniecs.world import World, WorldFactory

from core.primitives import Color
from ui.components.behavior import SelectionGroup, Toggleable, Toggled
from ui.components.command import SetTextColorCommand
from ui.components.intent import PressIntent
from ui.systems.behaviour_system import ToggleSystem


def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(ToggleSystem())
    return world

def test_no_press_intention():
    world = create_world()

    entity_id = world.spawn(Toggleable())
    world.execute()

    assert world.query_entities(none_of=(Toggled,)) == set([entity_id])

def test_no_toggleable():
    world = create_world()

    entity_id = world.spawn(PressIntent())
    world.execute()

    assert world.query_entities(none_of=(Toggled,)) == set([entity_id])

def test_toggled_on_spawn():
    world = create_world()

    entity_id = world.spawn(Toggleable(enter=[SetTextColorCommand(Color(0, 0, 0))]), Toggled())
    world.execute()

    assert world.query_entities(all_of=(Toggled, SetTextColorCommand)) == set([entity_id])

def test_add_toggle():
    world = create_world()

    entity_id = world.spawn(Toggleable(), PressIntent())
    world.execute()

    assert world.query_entities(all_of=(Toggled,)) == set([entity_id])
    assert len(world.get_events()) == 0

def test_add_selected_with_command():
    world = create_world()

    entity_id = world.spawn(Toggleable(enter=[SetTextColorCommand(Color(0, 0, 0))]), PressIntent())
    world.execute()

    assert world.query_entities(all_of=(Toggled, SetTextColorCommand)) == set([entity_id])
    assert len(world.get_events()) == 0

def test_remove_toggle():
    world = create_world()

    entity_id = world.spawn(Toggleable(), Toggled(), PressIntent())
    world.execute()

    assert world.query_entities(none_of=(Toggled,)) == set([entity_id])

def test_remove_selected_with_command():
    world = create_world()

    entity_id = world.spawn(Toggleable(exit=[SetTextColorCommand(Color(0, 0, 0))]), Toggled(), PressIntent())
    world.execute()

    assert world.query_entities(all_of=(SetTextColorCommand,), none_of=(Toggled,)) == set([entity_id])
