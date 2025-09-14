from dataclasses import dataclass

from ecs_framework.ecs import ComponentProtocol


@dataclass
class ForceRedraw(ComponentProtocol):
    pass


@dataclass
class NeedRedraw(ComponentProtocol):
    pass


@dataclass
class Renderable(ComponentProtocol):
    pass


@dataclass
class Highlightable(ComponentProtocol):
    pass


@dataclass
class Labelable(ComponentProtocol):
    pass


@dataclass
class Frameable(ComponentProtocol):
    pass
