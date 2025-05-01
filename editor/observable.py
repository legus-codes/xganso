from typing import Callable, Generic, List, TypeVar

T = TypeVar('T')

class Observable(Generic[T]):

    def __init__(self, value: T):
        self.value = value
        self.listeners: List[Callable[[T], None]] = []

    def set(self, value: T) -> None:
        if value != self.value:
            self.value = value
            for callback in self.listeners:
                callback(value)

    def get(self) -> T:
        return self.value
    
    def bind(self, callback: Callable) -> None:
        self.listeners.append(callback)
        
    def unbind(self, callback: Callable) -> None:
        if callback in self.listeners:
            self.listeners.remove(callback)
        