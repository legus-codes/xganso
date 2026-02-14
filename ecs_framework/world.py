from asyncio import Event
from typing import Iterable, TypeVar, TypeVarTuple

from ecs_framework.managers.component_manager import ComponentManager
from ecs_framework.managers.entity_manager import EntityManager
from ecs_framework.managers.event_manager import EventManager
from ecs_framework.managers.render_manager import RenderManager
from ecs_framework.managers.resource_manager import ResourceManager
from ecs_framework.managers.system_manager import SystemManager
from ecs_framework.primitives import ComponentProtocol, DrawCommand, EntityId, ExecutionStage, Resource, SystemProtocol
from ecs_framework.systems.cleanup import ClearEventSystem, ClearRenderQueueSystem, ClearTemporaryComponentSystem


R = TypeVar("R", bound=Resource)
Cs = TypeVarTuple("Cs")


class World:

    def __init__(self):
        self._entities = EntityManager()
        self._components = ComponentManager()
        self._systems = SystemManager()
        self._add_cleanup_systems()
        self._resources = ResourceManager()
        self._events = EventManager()
        self._render = RenderManager()
        self._running = True

    def reset(self) -> None:
        self._entities.clear()
        self._components.clear()
        self._systems.clear()
        self._add_cleanup_systems()
        self._resources.clear()
        self._events.clear()
        self._render.clear()

    def spawn(self, *components: ComponentProtocol) -> EntityId:
        entity_id = self._entities.create()
        for component in components:
            self.add_component(entity_id, component)
        return entity_id

    def destroy(self, entity_id: EntityId) -> None:
        self._components.destroy(entity_id)
        self._entities.destroy(entity_id)

    def add_component(self, entity_id: EntityId, component: ComponentProtocol) -> None:
        self._components.add(entity_id, component)

    def remove_component(self, entity_id: EntityId, component_type: type[ComponentProtocol]) -> None:
        self._components.remove(entity_id, component_type)

    def remove_all(self, component_type: type[ComponentProtocol]) -> None:
        self._components.remove_all(component_type)

    def query_entities(self,
                       all_of: tuple[type[ComponentProtocol], ...] = (),
                       any_of: tuple[type[ComponentProtocol], ...] = (),
                       none_of: tuple[type[ComponentProtocol], ...] = ()
     ) -> set[EntityId]:
        return self._components.query_entities(all_of, any_of, none_of)


    def query(self,
              *component_types: *Cs,
              all_of: tuple[type[ComponentProtocol], ...] = (),
              any_of: tuple[type[ComponentProtocol], ...] = (),
              none_of: tuple[type[ComponentProtocol], ...] = ()
     ) -> Iterable[tuple[EntityId, tuple[*Cs]]]:
        yield from self._components.query(*component_types, all_of=all_of, any_of=any_of, none_of=none_of)

    def register_temporary_component(self, component_type: type[ComponentProtocol]) -> None:
        self._components.register_temporary_component(component_type)

    def get_temporary_components(self) -> list[type[ComponentProtocol]]:
        return self._components.get_temporary_components()
    
    def add_system(self, system: SystemProtocol, stage: ExecutionStage) -> None:
        self._systems.add(system, stage)

    def _add_cleanup_systems(self) -> None:
        self.add_system(ClearEventSystem(self), ExecutionStage.frame_start)
        self.add_system(ClearRenderQueueSystem(self), ExecutionStage.frame_start)
        self.add_system(ClearTemporaryComponentSystem(self), ExecutionStage.frame_start)

    def execute(self, delta_time: float) -> None:
        self._systems.execute(delta_time)

    def set_resource(self, resource: Resource) -> None:
        self._resources.set(resource)

    def get_resource(self, resource: type[R]) -> R:
        return self._resources.get(resource)

    def push_event(self, event: Event) -> None:
        self._events.push(event)

    def get_events(self) -> list[Event]:
        return self._events.get()
    
    def clear_events(self) -> None:
        self._events.clear()

    def add_draw_command(self, draw_command: DrawCommand) -> None:
        self._render.push(draw_command)

    def get_draw_commands(self ) -> list[DrawCommand]:
        return self._render.get()
    
    def clear_draw_commands(self) -> None:
        self._render.clear()
