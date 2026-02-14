from itertools import chain
from typing import Iterable
from ecs_framework.primitives import ExecutionStage, SystemProtocol
from ecs_framework.systems.cleanup import ClearEventSystem, ClearRenderQueueSystem, ClearTemporaryComponentSystem


class SystemManager:

    def __init__(self):
        self._systems: dict[ExecutionStage, list[SystemProtocol]] = {
            ExecutionStage.frame_start: [],
            ExecutionStage.update: []
        }
   
    @property
    def all_systems(self) -> Iterable[SystemProtocol]:
        return chain(*self._systems.values())

    def add(self, system: SystemProtocol, stage: ExecutionStage) -> None:
        if any(isinstance(s, type(system)) for s in self.all_systems):
            raise ValueError(f'System {type(system).__name__} already registered')
        self._systems[stage].append(system)

    def remove(self, system_type: type[SystemProtocol]) -> None:
        for stage, systems in self._systems.items():
            self._systems[stage] = [system for system in systems if not isinstance(system, system_type)]

    def execute(self, delta_time: float) -> None:
        for system in list(self._systems[ExecutionStage.frame_start]):
            system.execute(delta_time)

        for system in list(self._systems[ExecutionStage.update]):
            system.execute(delta_time)

    def clear(self) -> None:
        for systems in self._systems.values():
            systems.clear()
