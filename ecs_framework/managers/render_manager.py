from ecs_framework.primitives import DrawCommand


class RenderManager:

    def __init__(self):
        self._queue: list[DrawCommand] = []

    def push(self, command: DrawCommand) -> None:
        self._queue.append(command)

    def drain(self) -> list[DrawCommand]:
        commands = self._queue
        self._queue = []
        commands.sort(key=lambda c: c.layer)
        return commands

    def clear(self) -> None:
        self._queue.clear()
