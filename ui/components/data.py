from dataclasses import dataclass

from ecs_framework.ecs import ComponentProtocol


@dataclass
class Label(ComponentProtocol):
    label: str


@dataclass
class RadioItem(ComponentProtocol):
    radio_group: str


@dataclass
class Trigger(ComponentProtocol):
    name: ComponentProtocol


@dataclass
class Variable(ComponentProtocol):
    value: str
    variable_type: type


@dataclass
class RenderLayer(ComponentProtocol):
    layer: int
