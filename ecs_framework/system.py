from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ecs_framework.world import World


class System:

    def __init__(self):
        self.world: World | None = None

    def register(self, world: World) -> None:
        self.world = world

    def execute(self, delta_time: float) -> None: ...
        

class ClearEventSystem(System):

    def execute(self, _: float) -> None:
        self.world.clear_events()

        
class ClearRenderQueueSystem(System):

    def execute(self, _: float) -> None:
        self.world.clear_draw_commands()


class ClearTemporaryComponentSystem(System):

    def execute(self, _: float) -> None:
        for component_type in self.world.get_temporary_components():
            self.world.remove_all(component_type)
