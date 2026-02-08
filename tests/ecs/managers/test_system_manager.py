import pytest
from ecs_framework.ecs import SystemProtocol
from ecs_framework.managers.system_manager import SystemManager


class SystemA(SystemProtocol): ...

class SystemB(SystemProtocol): ...

class SystemC(SystemProtocol): ...


def test_add_system():
    system_manager = SystemManager()
    system_manager.add(SystemA())
    assert len(system_manager._systems) == 1

def test_add_multiple_systems():
    system_manager = SystemManager()
    system_manager.add(SystemA())
    system_manager.add(SystemB())
    system_manager.add(SystemC())
    assert len(system_manager._systems) == 3

def test_add_system_of_same_type():
    system_manager = SystemManager()
    system_manager.add(SystemA())
    with pytest.raises(ValueError) as exception:
        system_manager.add(SystemA())

def test_remove_system():
    system_manager = SystemManager()
    system_manager.add(SystemA())
    system_manager.add(SystemB())
    system_manager.add(SystemC())
    system_manager.remove(SystemB)
    assert len(system_manager._systems) == 2
