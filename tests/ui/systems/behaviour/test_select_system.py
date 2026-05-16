from omniecs.world import World, WorldFactory

from core.primitives import Color
from ui.components.behavior import Selectable, Selected, SelectionGroup
from ui.components.command import SetTextColorCommand
from ui.components.intent import PressIntent
from ui.events.events import DeselectGroupEvent
from ui.systems.behaviour_system import SelectSystem


def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(SelectSystem())
    return world

def test_no_press_intention():
    world = create_world()

    entity_id = world.spawn(Selectable())
    world.execute()

    assert world.query_entities(none_of=(Selected,)) == set([entity_id])

def test_no_selectable():
    world = create_world()

    entity_id = world.spawn(PressIntent())
    world.execute()

    assert world.query_entities(none_of=(Selected,)) == set([entity_id])

def test_selected_on_spawn():
    world = create_world()

    entity_id = world.spawn(Selectable(enter=[SetTextColorCommand(Color(0, 0, 0))]), Selected())
    world.execute()

    assert world.query_entities(all_of=(Selected, SetTextColorCommand)) == set([entity_id])
    assert len(world.get_events()) == 0

def test_add_selected():
    world = create_world()

    entity_id = world.spawn(Selectable(), PressIntent())
    world.execute()

    assert world.query_entities(all_of=(Selected,)) == set([entity_id])
    assert len(world.get_events()) == 0

def test_add_selected_with_command():
    world = create_world()

    entity_id = world.spawn(Selectable(enter=[SetTextColorCommand(Color(0, 0, 0))]), PressIntent())
    world.execute()

    assert world.query_entities(all_of=(Selected, SetTextColorCommand)) == set([entity_id])
    assert len(world.get_events()) == 0

def test_add_selected_in_group():
    world = WorldFactory.create_empty_world()
    world.register_system(SelectSystem())

    entity_id = world.spawn(Selectable(), SelectionGroup(group='group'), PressIntent())
    world.execute()

    assert world.query_entities(all_of=(Selected,)) == set([entity_id])
    assert len(world.get_events()) == 1
    event = world.get_events()[0]
    assert isinstance(event, DeselectGroupEvent)
    assert event.group == 'group'
    assert event.selected == entity_id
