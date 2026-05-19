from omniecs.world import World, WorldFactory

from adapters.render.commands import DrawRectangle
from core.primitives import Color, ColorStack, Vec2
from ui.bundles import PanelLayoutBundle, RectTransformBundle, SurfaceBundle, WidgetCoreBundle
from ui.components.behavior import Enabled
from ui.components.layout import RenderLayer, WorldTransform
from ui.components.rendering import Dirty
from ui.components.style import Background
from ui.systems.layout_system import WorldTransformationSystem
from ui.systems.renderer_system import BackgroundRendererSystem
from ui.widgets import PanelBundle


background = Background(colors=ColorStack(Color(200, 0, 0)))
transform = WorldTransform(Vec2(100, 100), Vec2(50, 50))
render_layer = RenderLayer(3)
enabled = Enabled()
dirty = Dirty()

def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(BackgroundRendererSystem())
    return world


def test_render_background():
    world = create_world()
    world.spawn(background, transform, render_layer, enabled, dirty)

    world.execute()
    assert world.query_entities(all_of=(Dirty,)) == set()

    draw_commands = world.get_draw_commands()
    assert len(draw_commands) == 1
    
    draw_command = draw_commands[0]
    assert isinstance(draw_command, DrawRectangle)
    assert draw_command.global_layer == 3
    assert draw_command.local_layer == 0
    assert draw_command.position == Vec2(100, 100)
    assert draw_command.size == Vec2(50, 50)
    assert draw_command.color == Color(200, 0, 0)


def test_render_panel_bundle():
    core = WidgetCoreBundle()
    transform = RectTransformBundle(Vec2(x=50, y=50))
    layout = PanelLayoutBundle()
    surface = SurfaceBundle(Color(0, 200, 0))

    panel = PanelBundle(core, transform, layout, surface)

    world = WorldFactory.create_world()
    world.spawn(*panel.components())
    world.register_system(WorldTransformationSystem())
    world.register_system(BackgroundRendererSystem())

    world.execute()
    assert world.query_entities(all_of=(Dirty,)) == set()

    draw_commands = world.get_draw_commands()
    assert len(draw_commands) == 1
    
    draw_command = draw_commands[0]
    assert isinstance(draw_command, DrawRectangle)
    assert draw_command.global_layer == 0
    assert draw_command.local_layer == 0
    assert draw_command.position == Vec2(0, 0)
    assert draw_command.size == Vec2(50, 50)
    assert draw_command.color == Color(0, 200, 0)


def test_render_background_no_background():
    world = create_world()
    world.spawn(transform, render_layer, enabled, dirty)

    world.execute()

    assert world.get_draw_commands() == []

def test_render_background_no_transform():
    world = create_world()
    world.spawn(background, render_layer, enabled, dirty)

    world.execute()

    assert world.get_draw_commands() == []

def test_render_background_no_render_layer():
    world = create_world()
    world.spawn(background, transform, enabled, dirty)

    world.execute()

    assert world.get_draw_commands() == []

def test_render_background_no_enabled():
    world = create_world()
    world.spawn(background, transform, render_layer, dirty)

    world.execute()

    assert world.get_draw_commands() == []

def test_render_background_no_dirty():
    world = create_world()
    world.spawn(background, transform, render_layer, enabled)

    world.execute()

    assert world.get_draw_commands() == []
 