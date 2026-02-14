from ecs_framework.primitives import Resource
from ecs_framework.protocols import R, ResourceManagerProtocol


class ResourceManager(ResourceManagerProtocol):

    def __init__(self):
        self._resources: dict[type[Resource], Resource] = {}
   
    def set(self, resource: Resource) -> None:
        self._resources[type(resource)] = resource

    def get(self, resource_type: type[R]) -> R | None:
        return self._resources.get(resource_type, None)

    def remove(self, resource_type: type[Resource]) -> None:
        self._resources.pop(resource_type, None)

    def clear(self) -> None:
        self._resources.clear()
