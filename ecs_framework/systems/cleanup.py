from ecs_framework.primitives import SystemProtocol
from ecs_framework.protocols import WorldProtocol


class ClearEventSystem(SystemProtocol):

    def __init__(self, world: WorldProtocol):
        self.world = world

    def execute(self, _: float) -> None:
        self.world.clear_events()

        
class ClearRenderQueueSystem(SystemProtocol):

    def __init__(self, world: WorldProtocol):
        self.world = world

    def execute(self, _: float) -> None:
        self.world.clear_draw_commands()


class ClearTemporaryComponentSystem(SystemProtocol):

    def __init__(self, world: WorldProtocol):
        self.world = world

    def execute(self, _: float) -> None:
        for component_type in self.world.get_temporary_components():
            self.world.remove_all(component_type)
