from ecs_framework.primitives import DrawCommand
from ecs_framework.protocols import RenderManagerProtocol


class RenderManager(RenderManagerProtocol):

    def __init__(self):
        self._queue: list[DrawCommand] = []

    def push(self, command: DrawCommand) -> None:
        self._queue.append(command)

    def get(self) -> list[DrawCommand]:
        return sorted(self._queue, key=lambda c: c.layer())

    def clear(self) -> None:
        self._queue.clear()
