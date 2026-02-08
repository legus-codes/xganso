from typing import List, Protocol


class DrawCommand(Protocol):

    @property
    def layer(self) -> int: ...


class RenderManager:

    def __init__(self):
        self._queue: List[DrawCommand] = []

    def push(self, command: DrawCommand) -> None:
        self._queue.append(command)

    def drain(self) -> List[DrawCommand]:
        commands = self._queue
        self._queue = []
        commands.sort(key=lambda c: c.layer)
        return commands

    def clear(self) -> None:
        self._queue.clear()
