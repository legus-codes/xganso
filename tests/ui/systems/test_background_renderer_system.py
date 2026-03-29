from omniecs.world import WorldFactory

from adapters.render.commands import DrawRectangle
from core.primitives import Color, Vec2
from ui.components.behavior import Enabled
from ui.components.layout import RenderLayer, Transform
from ui.components.rendering import Dirty
from ui.components.style import Background
from ui.systems.renderer_system import BackgroundRendererSystem
from ui.types import InteractionColors


background = Background(color=InteractionColors(normal=Color(200, 0, 0)))
transform = Transform(Vec2(100, 100), Vec2(50, 50))
render_layer = RenderLayer(3)
enabled = Enabled()
dirty = Dirty()


def test_render_background():
    world = WorldFactory.create_empty_world()
    world.spawn(background, transform, render_layer, enabled, dirty)
    world.register_system(BackgroundRendererSystem())

    world.execute()
    assert world.query_entities(all_of=(Dirty,)) == set()

    draw_commands = world.get_draw_commands()
    assert len(draw_commands) == 1
    
    draw_command = draw_commands[0]
    assert isinstance(draw_command, DrawRectangle)
    assert draw_command.layer == 3
    assert draw_command.position == Vec2(100, 100)
    assert draw_command.size == Vec2(50, 50)
    assert draw_command.color == Color(200, 0, 0)

def test_render_background_no_background():
    world = WorldFactory.create_empty_world()
    entity_id = world.spawn(transform, render_layer, enabled, dirty)
    world.register_system(BackgroundRendererSystem())

    world.execute()
    assert world.query_entities(all_of=(Dirty,)) == set([entity_id])

    assert world.get_draw_commands() == []

def test_render_background_no_transform():
    world = WorldFactory.create_empty_world()
    entity_id = world.spawn(background, render_layer, enabled, dirty)
    world.register_system(BackgroundRendererSystem())

    world.execute()
    assert world.query_entities(all_of=(Dirty,)) == set([entity_id])

    assert world.get_draw_commands() == []

def test_render_background_no_render_layer():
    world = WorldFactory.create_empty_world()
    entity_id = world.spawn(background, transform, enabled, dirty)
    world.register_system(BackgroundRendererSystem())

    world.execute()
    assert world.query_entities(all_of=(Dirty,)) == set([entity_id])

    assert world.get_draw_commands() == []

def test_render_background_no_enabled():
    world = WorldFactory.create_empty_world()
    entity_id = world.spawn(background, transform, render_layer, dirty)
    world.register_system(BackgroundRendererSystem())

    world.execute()
    assert world.query_entities(all_of=(Dirty,)) == set([entity_id])

    assert world.get_draw_commands() == []

def test_render_background_no_dirty():
    world = WorldFactory.create_empty_world()
    world.spawn(background, transform, render_layer, enabled)
    world.register_system(BackgroundRendererSystem())

    world.execute()

    assert world.get_draw_commands() == []
 