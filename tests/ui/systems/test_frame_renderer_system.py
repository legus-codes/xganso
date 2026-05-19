from omniecs.world import World, WorldFactory

from adapters.render.commands import DrawFrame
from core.primitives import Color, ColorStack, Vec2
from ui.bundles import PanelLayoutBundle, RectTransformBundle, SurfaceBundle, WidgetCoreBundle
from ui.components.behavior import Enabled
from ui.components.layout import RenderLayer, WorldTransform
from ui.components.rendering import Dirty
from ui.components.style import Frame
from ui.systems.layout_system import WorldTransformationSystem
from ui.systems.renderer_system import FrameRendererSystem
from ui.widgets import PanelBundle


frame = Frame(colors=ColorStack(Color(200, 0, 0)), width=2)
transform = WorldTransform(Vec2(100, 100), Vec2(50, 50))
render_layer = RenderLayer(3)
enabled = Enabled()
dirty = Dirty()

def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(FrameRendererSystem())
    return world


def test_render_frame():
    world = create_world()
    world.spawn(frame, transform, render_layer, enabled, dirty)

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


def test_render_panel_bundle():
    core = WidgetCoreBundle()
    transform = RectTransformBundle(Vec2(x=50, y=50))
    layout = PanelLayoutBundle()
    surface = SurfaceBundle(Color(0, 0, 200), Color(200, 0, 0), 2)

    panel = PanelBundle(core, transform, layout, surface)

    world = WorldFactory.create_world()
    world.spawn(*panel.components())
    world.register_system(WorldTransformationSystem())
    world.register_system(FrameRendererSystem())

    world.execute()
    assert world.query_entities(all_of=(Dirty,)) == set()

    draw_commands = world.get_draw_commands()
    assert len(draw_commands) == 1
    
    draw_command = draw_commands[0]
    assert isinstance(draw_command, DrawFrame)
    assert draw_command.global_layer == 0
    assert draw_command.local_layer == 1
    assert draw_command.position == Vec2(0, 0)
    assert draw_command.size == Vec2(50, 50)
    assert draw_command.color == Color(0, 0, 200)
    assert draw_command.width == 2


def test_render_frame_no_frame():
    world = create_world()
    world.spawn(transform, render_layer, enabled, dirty)

    world.execute()

    assert world.get_draw_commands() == []

def test_render_frame_no_transform():
    world = create_world()
    world.spawn(frame, render_layer, enabled, dirty)

    world.execute()

    assert world.get_draw_commands() == []

def test_render_frame_no_render_layer():
    world = create_world()
    world.spawn(frame, transform, enabled, dirty)

    world.execute()

    assert world.get_draw_commands() == []

def test_render_frame_no_enabled():
    world = create_world()
    world.spawn(frame, transform, render_layer, dirty)

    world.execute()

    assert world.get_draw_commands() == []

def test_render_frame_no_dirty():
    world = create_world()
    world.spawn(frame, transform, render_layer, enabled)

    world.execute()

    assert world.get_draw_commands() == []
 