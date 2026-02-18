from ecs_framework.factory import WorldFactory
from ecs_framework.primitives import ComponentProtocol, DrawCommand, Event
from ecs_framework.systems.cleanup import ClearEventSystem, ClearRenderQueueSystem, ClearTemporaryComponentSystem


class MockEvent(Event): ...
class MockDrawCommand(DrawCommand): ...
class MockTemporaryComponent(ComponentProtocol): ...


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

    world.add_draw_command(MockDrawCommand())
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
