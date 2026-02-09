import pytest
from dataclasses import dataclass

from ecs_framework.primitives import SystemProtocol
from ecs_framework.managers.system_manager import SystemManager


@dataclass
class SystemA(SystemProtocol): 
    executed: bool = False

    def execute(self, delta_time):
        self.executed = True

@dataclass
class SystemB(SystemProtocol):
    executed: bool = False

    def execute(self, delta_time):
        self.executed = True

@dataclass
class SystemC(SystemProtocol):
    executed: bool = False

    def execute(self, delta_time):
        self.executed = True


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

def test_execute_systems():
    system_manager = SystemManager()
    system_manager.add(SystemA())
    system_manager.add(SystemB())
    system_manager.add(SystemC())
    system_manager.execute(0)
    for system in system_manager._systems:
        assert system.executed

def test_remove_system():
    system_manager = SystemManager()
    system_manager.add(SystemA())
    system_manager.add(SystemB())
    system_manager.add(SystemC())
    system_manager.remove(SystemB)
    assert len(system_manager._systems) == 2

def test_clear_systems():
    system_manager = SystemManager()
    system_manager.add(SystemA())
    system_manager.add(SystemB())
    system_manager.add(SystemC())
    system_manager.clear()
    assert len(system_manager._systems) == 0
