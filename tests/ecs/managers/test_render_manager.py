from dataclasses import dataclass

from ecs_framework.primitives import DrawCommand
from ecs_framework.managers.render_manager import RenderManager


@dataclass
class MockDrawCommand(DrawCommand):
    layer: int
    text: str


def test_create_command():
    render_manager = RenderManager()
    render_manager.push(MockDrawCommand(1, ''))
    assert len(render_manager._queue) == 1

    
def test_drain_events():
    render_manager = RenderManager()
    render_manager.push(MockDrawCommand(3, 'third'))
    render_manager.push(MockDrawCommand(1, 'first'))
    render_manager.push(MockDrawCommand(2, 'second'))
    commands = render_manager.drain()
    assert len(commands) == 3
    assert commands[0].text == 'first'
    assert commands[1].text == 'second'
    assert commands[2].text == 'third'
    assert len(render_manager._queue) == 0

    
def test_clear_events():
    render_manager = RenderManager()
    render_manager.push(MockDrawCommand(3, 'third'))
    render_manager.push(MockDrawCommand(1, 'first'))
    render_manager.push(MockDrawCommand(2, 'second'))
    render_manager.clear()
    assert len(render_manager._queue) == 0
