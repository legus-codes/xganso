from ecs_framework.ecs import ComponentProtocol


class Text(ComponentProtocol):
    text: str


class Value(ComponentProtocol):
    value: str
