from ecs_framework.primitives import SystemProtocol


class SystemManager:

    def __init__(self):
        self._systems: list[SystemProtocol] = []
   
    def add(self, system: SystemProtocol) -> None:
        if any(isinstance(s, type(system)) for s in self._systems):
            raise ValueError(f'System {type(system).__name__} already registered')
        self._systems.append(system)

    def remove(self, system_type: type[SystemProtocol]) -> None:
        self._systems = [system for system in self._systems if not isinstance(system, system_type)]

    def execute(self, delta_time: float) -> None:
        # Systems execute in insertion order (no priority yet)
        for system in list(self._systems):
            system.execute(delta_time)

    def clear(self) -> None:
        self._systems.clear()
