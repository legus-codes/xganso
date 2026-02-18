from dataclasses import dataclass
from ecs_framework.system import ClearEventSystem, ClearRenderQueueSystem, ClearTemporaryComponentSystem
from ecs_framework.types import Component, DrawCommandProtocol, Event
from ecs_framework.world import WorldFactory


class MockEvent(Event): ...
class MockTemporaryComponent(Component): ...

@dataclass
class MockDrawCommand(DrawCommandProtocol): 
    layer: int


def test_clear_event_system():
    world = WorldFactory.create_world()
    assert any(isinstance(system, ClearEventSystem) for system in world._systems.all_systems)

    world.push_event(MockEvent())
    assert len(world.get_events()) == 1

    world.execute(0)
    assert len(world.get_events()) == 0


def test_clear_render_queue_system():
    world = WorldFactory.create_world()
    assert any(isinstance(system, ClearRenderQueueSystem) for system in world._systems.all_systems)

    world.add_draw_command(MockDrawCommand(3))
    assert len(world.get_draw_commands()) == 1

    world.execute(0)
    assert len(world.get_draw_commands()) == 0


def test_clear_temporary_component_system():
    world = WorldFactory.create_world()
    assert any(isinstance(system, ClearTemporaryComponentSystem) for system in world._systems.all_systems)

    world.spawn(MockTemporaryComponent())
    world.spawn(MockTemporaryComponent())
    world.spawn(MockTemporaryComponent())
    world.register_temporary_component(MockTemporaryComponent)
    assert len(list(world.query_entities(all_of=(MockTemporaryComponent,)))) == 3

    world.execute(0)
    assert len(list(world.query_entities(all_of=(MockTemporaryComponent,)))) == 0
