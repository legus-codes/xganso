from omniecs.world import WorldFactory

from adapters.render.commands import DrawFrame
from core.primitives import Color, Vec2
from ui.components.behavior import Enabled
from ui.components.layout import RenderLayer, Transform
from ui.components.rendering import Dirty
from ui.components.style import Frame
from ui.systems.renderer_system import FrameRendererSystem
from ui.types import InteractionColors


frame = Frame(color=InteractionColors(normal=Color(200, 0, 0)), width=2)
transform = Transform(Vec2(100, 100), Vec2(50, 50))
render_layer = RenderLayer(3)
enabled = Enabled()
dirty = Dirty()


def test_render_frame():
    world = WorldFactory.create_world()
    world.spawn(frame, transform, render_layer, enabled, dirty)
    world.register_system(FrameRendererSystem())

    world.execute()
    assert world.query_entities(all_of=(Dirty,)) == set()

    draw_commands = world.get_draw_commands()
    assert len(draw_commands) == 1
    
    draw_command = draw_commands[0]
    assert isinstance(draw_command, DrawFrame)
    assert draw_command.global_layer == 3
    assert draw_command.local_layer == 1
    assert draw_command.position == Vec2(100, 100)
    assert draw_command.size == Vec2(50, 50)
    assert draw_command.color == Color(200, 0, 0)
    assert draw_command.width == 2

def test_render_frame_no_frame():
    world = WorldFactory.create_world()
    world.spawn(transform, render_layer, enabled, dirty)
    world.register_system(FrameRendererSystem())

    world.execute()

    assert world.get_draw_commands() == []

def test_render_frame_no_transform():
    world = WorldFactory.create_world()
    world.spawn(frame, render_layer, enabled, dirty)
    world.register_system(FrameRendererSystem())

    world.execute()

    assert world.get_draw_commands() == []

def test_render_frame_no_render_layer():
    world = WorldFactory.create_world()
    world.spawn(frame, transform, enabled, dirty)
    world.register_system(FrameRendererSystem())

    world.execute()

    assert world.get_draw_commands() == []

def test_render_frame_no_enabled():
    world = WorldFactory.create_world()
    world.spawn(frame, transform, render_layer, dirty)
    world.register_system(FrameRendererSystem())

    world.execute()

    assert world.get_draw_commands() == []

def test_render_frame_no_dirty():
    world = WorldFactory.create_world()
    world.spawn(frame, transform, render_layer, enabled)
    world.register_system(FrameRendererSystem())

    world.execute()

    assert world.get_draw_commands() == []
 