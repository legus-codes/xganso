from typing import Iterable

from ecs_framework.managers import ComponentManager, EntityManager, EventManager, RenderManager, ResourceManager, SystemManager
from ecs_framework.system import ClearEventSystem, ClearRenderQueueSystem, ClearTemporaryComponentSystem, System
from ecs_framework.types import R, Component, Cs, DrawCommandProtocol, EntityId, Event, ExecutionStage, Resource


class World:

    def __init__(self,
                 entity_manager: EntityManager,
                 component_manager: ComponentManager,
                 system_manager: SystemManager,
                 resource_manager: ResourceManager,
                 event_manager: EventManager,
                 render_manager: RenderManager):
        self._entities = entity_manager
        self._components = component_manager
        self._systems = system_manager
        self._resources = resource_manager
        self._events = event_manager
        self._render = render_manager
        self._running = True

    def spawn(self, *components: Component) -> EntityId:
        entity_id = self._entities.create()
        for component in components:
            self.add_component(entity_id, component)
        return entity_id

    def destroy(self, entity_id: EntityId) -> None:
        self._components.destroy(entity_id)
        self._entities.destroy(entity_id)

    def add_component(self, entity_id: EntityId, component: Component) -> None:
        self._components.add(entity_id, component)

    def remove_component(self, entity_id: EntityId, component_type: type[Component]) -> None:
        self._components.remove(entity_id, component_type)

    def remove_all(self, component_type: type[Component]) -> None:
        self._components.remove_all(component_type)

    def query_entities(self,
                       all_of: tuple[type[Component], ...] = (),
                       any_of: tuple[type[Component], ...] = (),
                       none_of: tuple[type[Component], ...] = ()
     ) -> set[EntityId]:
        return self._components.query_entities(all_of, any_of, none_of)


    def query(self,
              *component_types: *Cs,
              all_of: tuple[type[Component], ...] = (),
              any_of: tuple[type[Component], ...] = (),
              none_of: tuple[type[Component], ...] = ()
     ) -> Iterable[tuple[EntityId, tuple[*Cs]]]:
        yield from self._components.query(*component_types, all_of=all_of, any_of=any_of, none_of=none_of)

    def register_temporary_component(self, component_type: type[Component]) -> None:
        self._components.register_temporary_component(component_type)

    def get_temporary_components(self) -> list[type[Component]]:
        return self._components.get_temporary_components()
    
    def register_system(self, system: System, stage: ExecutionStage) -> None:
        system.register(self)
        self._systems.add(system, stage)

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

    def add_draw_command(self, draw_command: DrawCommandProtocol) -> None:
        self._render.push(draw_command)

    def get_draw_commands(self ) -> list[DrawCommandProtocol]:
        return self._render.get()
    
    def clear_draw_commands(self) -> None:
        self._render.clear()


class WorldFactory:

    @staticmethod
    def create_world() -> World:
        entity_manager = EntityManager()
        component_manager = ComponentManager()
        system_manager = SystemManager()
        resource_manager = ResourceManager()
        event_manager = EventManager()
        render_manager = RenderManager()

        world = World(entity_manager, component_manager, system_manager, resource_manager, event_manager, render_manager)
        world.register_system(ClearRenderQueueSystem(), ExecutionStage.reset)
        world.register_system(ClearEventSystem(), ExecutionStage.cleanup)
        world.register_system(ClearTemporaryComponentSystem(), ExecutionStage.cleanup)
        
        return world
