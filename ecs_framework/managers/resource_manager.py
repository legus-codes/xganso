from typing import Dict, Type, TypeVar


class Resource: ...


R = TypeVar("R", bound=Resource)


class ResourceManager:

    def __init__(self):
        self._resources: Dict[Type[Resource], Resource] = {}
   
    def set(self, resource: Resource) -> None:
        self._resources[type(resource)] = resource

    def get(self, resource_type: Type[R]) -> R | None:
        return self._resources.get(resource_type, None)

    def remove(self, resource_type: Type[Resource]) -> None:
        self._resources.pop(resource_type, None)

    def clear(self) -> None:
        self._resources.clear()
