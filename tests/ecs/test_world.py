from asyncio import Event
from ecs_framework.managers.component_manager import ComponentManager
from ecs_framework.managers.entity_manager import EntityManager
from ecs_framework.managers.event_manager import EventManager
from ecs_framework.managers.render_manager import RenderManager
from ecs_framework.managers.resource_manager import ResourceManager
from ecs_framework.managers.system_manager import SystemManager
from ecs_framework.primitives import ComponentProtocol, DrawCommand, ExecutionStage, Resource, SystemProtocol
from ecs_framework.world import World


class MockComponentA(ComponentProtocol): ...
class MockComponentB(ComponentProtocol): ...
class MockComponentC(ComponentProtocol): ...

class MockSystem(SystemProtocol):
    executed: bool = False
    def execute(self, delta_time: float) -> None:
        self.executed = True

class MockResource(Resource): ...

class MockEvent(Event): ...

class MockDrawCommand(DrawCommand):
    def layer(self) -> int:
        return 0

def test_world_has_all_managers():
    world = World()
    assert isinstance(world._entities, EntityManager)
    assert isinstance(world._components, ComponentManager)
    assert isinstance(world._systems, SystemManager)
    assert len(list(world._systems.all_systems)) == 3
    assert isinstance(world._resources, ResourceManager)
    assert isinstance(world._events, EventManager)
    assert isinstance(world._render, RenderManager)

def test_reset_world():
    world = World()
    world.spawn(MockComponentA(), MockComponentB())
    world.register_temporary_component(MockComponentA)
    world.add_system(MockSystem(), ExecutionStage.update)
    world.set_resource(MockResource())
    world.push_event(MockEvent())
    world.add_draw_command(MockDrawCommand())

    world.reset()
    assert world._entities._entities == set()
    assert len(world._components._component_storage) == 0
    assert len(world._components._temporary_components) == 0
    assert len(list(world._systems.all_systems)) == 3
    assert len(world._resources._resources) == 0
    assert world._events._events == []
    assert world._render._queue == []

def test_spawn_entity():
    world = World()
    componentA = MockComponentA()
    componentB = MockComponentB()
    entity_id = world.spawn(componentA, componentB)

    entities = list(world.query(MockComponentA, MockComponentB))
    assert len(entities) == 1
    entity, (compA, compB) = entities[0]
    assert entity == entity_id
    assert compA == componentA
    assert compB == componentB

def test_destroy_entity():
    world = World()
    componentA = MockComponentA()
    componentB = MockComponentB()
    entity_id = world.spawn(componentA, componentB)
    world.destroy(entity_id)

    assert world.query_entities(any_of=(MockComponentA, MockComponentB)) == set()

def test_add_component():
    world = World()
    componentC = MockComponentC()
    entity_id = world.spawn(MockComponentA(), MockComponentB())
    world.add_component(entity_id, componentC)

    entities = list(world.query(MockComponentC))
    assert len(entities) == 1
    entity, (compC,) = entities[0]
    assert entity == entity_id
    assert compC == componentC

def test_remove_component():
    world = World()
    entity_id = world.spawn(MockComponentA(), MockComponentB())
    world.remove_component(entity_id, MockComponentA)

    assert world.query_entities(all_of=(MockComponentA,)) == set()

def test_register_temporary_component():
    world = World()
    world.register_temporary_component(MockComponentA)
    world.spawn(MockComponentA())
    world.spawn(MockComponentA())
    world.spawn(MockComponentA())
    world.execute(0)

    assert world.query_entities(all_of=(MockComponentA,)) == set()

def test_execute_system():
    world = World()
    system = MockSystem()
    world.add_system(system, ExecutionStage.update)
    assert not system.executed

    world.execute(0)
    assert system.executed

def test_set_resource():
    world = World()
    resource = MockResource()
    world.set_resource(resource)

    assert world.get_resource(MockResource) == resource

def test_overwrite_resource():
    world = World()
    resource = MockResource()
    world.set_resource(MockResource())
    world.set_resource(resource)

    assert world.get_resource(MockResource) == resource

def test_push_events():
    world = World()
    event = MockEvent()
    world.push_event(event)
    world.push_event(event)
    world.push_event(event)

    assert world.get_events() == [event, event, event]
    assert world.get_events() == [event, event, event]

def test_add_draw_commands():
    world = World()
    draw_command = MockDrawCommand()
    world.add_draw_command(draw_command)
    world.add_draw_command(draw_command)
    world.add_draw_command(draw_command)

    assert world.get_draw_commands() == [draw_command, draw_command, draw_command]
    assert world.get_draw_commands() == [draw_command, draw_command, draw_command]

