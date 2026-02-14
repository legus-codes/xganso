from ecs_framework.managers.component_manager import ComponentManager
from ecs_framework.managers.entity_manager import EntityManager
from ecs_framework.managers.event_manager import EventManager
from ecs_framework.managers.render_manager import RenderManager
from ecs_framework.managers.resource_manager import ResourceManager
from ecs_framework.managers.system_manager import SystemManager
from ecs_framework.primitives import ExecutionStage
from ecs_framework.protocols import WorldProtocol
from ecs_framework.systems.cleanup import ClearEventSystem, ClearRenderQueueSystem, ClearTemporaryComponentSystem
from ecs_framework.world import World


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
        WorldFactory._register_cleanup_systems(world)
        
        return world
        
    @staticmethod
    def _register_cleanup_systems(world: WorldProtocol) -> None:
        world.add_system(ClearEventSystem(world), ExecutionStage.frame_start)
        world.add_system(ClearRenderQueueSystem(world), ExecutionStage.frame_start)
        world.add_system(ClearTemporaryComponentSystem(world), ExecutionStage.frame_start)
