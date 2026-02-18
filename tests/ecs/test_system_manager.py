import pytest
from dataclasses import dataclass

from ecs_framework.managers import SystemManager
from ecs_framework.system import System
from ecs_framework.types import ExecutionStage



@dataclass
class SystemA(System): 
    executed: bool = False

    def execute(self, delta_time):
        self.executed = True

@dataclass
class SystemB(System):
    executed: bool = False

    def execute(self, delta_time):
        self.executed = True

@dataclass
class SystemC(System):
    executed: bool = False

    def execute(self, delta_time):
        self.executed = True


@pytest.mark.parametrize('stage', [ExecutionStage.reset, ExecutionStage.update, ExecutionStage.cleanup])
def test_add_system_frame_start(stage: ExecutionStage):
    system_manager = SystemManager()
    system_manager.add(SystemA(), stage)
    system_manager.add(SystemB(), stage)
    system_manager.add(SystemC(), stage)
    assert len(system_manager._systems[stage]) == 3

def test_add_system_of_same_type():
    system_manager = SystemManager()
    system_manager.add(SystemA(), ExecutionStage.update)
    with pytest.raises(ValueError) as exception:
        system_manager.add(SystemA(), ExecutionStage.update)

def test_execute_systems():
    system_manager = SystemManager()
    system_manager.add(SystemA(), ExecutionStage.reset)
    system_manager.add(SystemB(), ExecutionStage.update)
    system_manager.add(SystemC(), ExecutionStage.cleanup)
    system_manager.execute(0)
    for system in system_manager.all_systems:
        assert system.executed

def test_remove_system():
    system_manager = SystemManager()
    system_manager.add(SystemA(), ExecutionStage.reset)
    system_manager.add(SystemB(), ExecutionStage.update)
    system_manager.add(SystemC(), ExecutionStage.cleanup)
    system_manager.remove(SystemA)
    system_manager.remove(SystemB)
    assert len(list(system_manager.all_systems)) == 1
