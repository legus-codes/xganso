from omniecs.world import World, WorldFactory

from adapters.render.commands import DrawText
from core.primitives import Color, IVec2, Vec2
from ui.bundles import RectTransformBundle, SurfaceBundle, TextVisualBundle, WidgetCoreBundle
from ui.components.behavior import Enabled
from ui.components.content import Text
from ui.components.layout import RenderLayer, Spacing, TextAlignment, HorizontalAlignment, WorldTransform, VerticalAlignment
from ui.components.rendering import Dirty
from ui.components.style import TextStyle
from ui.systems.layout_system import WorldTransformationSystem
from ui.systems.renderer_system import TextRendererSystem
from ui.types import InteractionColors, TextStyleDescription
from ui.widgets import TextBundle


text = Text('text')
text_style = TextStyle('arial', 16, InteractionColors(normal=Color(155, 0, 0)))
text_alignment = TextAlignment(HorizontalAlignment.center, VerticalAlignment.middle)
spacing = Spacing(5, 10)
transform = WorldTransform(Vec2(100, 100), Vec2(50, 50))
render_layer = RenderLayer(3)
enabled = Enabled()
dirty = Dirty()

def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(TextRendererSystem())
    return world


def test_render_text():
    world = create_world()
    world.spawn(text, text_style, text_alignment, spacing, transform, render_layer, enabled, dirty)

    world.execute()
    assert world.query_entities(all_of=(Dirty,)) == set()

    draw_commands = world.get_draw_commands()
    assert len(draw_commands) == 1
    
    draw_command = draw_commands[0]
    assert isinstance(draw_command, DrawText)
    assert draw_command.global_layer == 3
    assert draw_command.local_layer == 2
    assert draw_command.position == Vec2(100, 100)
    assert draw_command.text == 'text'
    assert draw_command.font_id == 'arial'
    assert draw_command.font_size == 16
    assert draw_command.size == Vec2(50, 50)
    assert draw_command.color == Color(155, 0, 0)
    assert draw_command.horizontal_alignment == HorizontalAlignment.center
    assert draw_command.vertical_alignment == VerticalAlignment.middle
    assert draw_command.spacing == IVec2(5, 10)


def test_render_text_bundle():
    core = WidgetCoreBundle()
    text = TextVisualBundle('text', TextStyleDescription('couriernew', 16, InteractionColors(normal=Color(20, 20, 20))))
    transform = RectTransformBundle(Vec2(x=50, y=50))
    surface = SurfaceBundle()

    text = TextBundle(core, text, transform, surface)

    world = WorldFactory.create_world()
    world.spawn(*text.components())
    world.register_system(WorldTransformationSystem())
    world.register_system(TextRendererSystem())

    world.execute()
    assert world.query_entities(all_of=(Dirty,)) == set()

    draw_commands = world.get_draw_commands()
    assert len(draw_commands) == 1
    
    draw_command = draw_commands[0]
    assert isinstance(draw_command, DrawText)
    assert draw_command.global_layer == 0
    assert draw_command.local_layer == 2
    assert draw_command.position == Vec2(0, 0)
    assert draw_command.text == 'text'
    assert draw_command.font_id == 'couriernew'
    assert draw_command.font_size == 16
    assert draw_command.size == Vec2(50, 50)
    assert draw_command.color == Color(20, 20, 20)
    assert draw_command.horizontal_alignment == HorizontalAlignment.left
    assert draw_command.vertical_alignment == VerticalAlignment.top
    assert draw_command.spacing == IVec2(0, 0)


def test_render_text_no_text():
    world = create_world()
    world.spawn(text_style, text_alignment, spacing, transform, render_layer, enabled, dirty)

    world.execute()

    assert world.get_draw_commands() == []


def test_render_text_no_text_style():
    world = create_world()
    world.spawn(text, text_alignment, spacing, transform, render_layer, enabled, dirty)

    world.execute()

    assert world.get_draw_commands() == []


def test_render_text_no_text_alignment():
    world = create_world()
    world.spawn(text, text_style, spacing, transform, render_layer, enabled, dirty)

    world.execute()

    assert world.get_draw_commands() == []


def test_render_text_no_spacing():
    world = create_world()
    world.spawn(text, text_style, text_alignment, transform, render_layer, enabled, dirty)

    world.execute()

    assert world.get_draw_commands() == []


def test_render_text_no_transform():
    world = create_world()
    world.spawn(text, text_style, text_alignment, spacing, render_layer, enabled, dirty)

    world.execute()

    assert world.get_draw_commands() == []


def test_render_text_no_render_layer():
    world = create_world()
    world.spawn(text, text_style, text_alignment, spacing, transform, enabled, dirty)

    world.execute()

    assert world.get_draw_commands() == []


def test_render_text_no_enabled():
    world = create_world()
    world.spawn(text, text_style, text_alignment, spacing, transform, render_layer, dirty)

    world.execute()

    assert world.get_draw_commands() == []


def test_render_text_no_dirty():
    world = create_world()
    world.spawn(text, text_style, text_alignment, spacing, transform, render_layer, enabled)

    world.execute()

    assert world.get_draw_commands() == []
