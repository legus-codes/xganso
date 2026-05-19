from dataclasses import dataclass
import pygame

from omniecs.world import WorldFactory

from adapters.input.pygame import PygameEventConverter
from adapters.render.pygame import PygameRenderer
from core.primitives import Color, Vec2
from model.terrain import Terrain
from ui.bundles import ActivatableBundle, InputBundle, PanelLayoutBundle, HoverableBundle, PressableBundle, RectTransformBundle, SelectableBundle, SurfaceBundle, TextVisualBundle, ToggleableBundle, WidgetCoreBundle
from ui.components.command import UnsetBackgroundColorCommand, UnsetFrameColorCommand, UnsetTextColorCommand, SetBackgroundColorCommand, SetFrameColorCommand, SetTextColorCommand
from ui.components.layout import HorizontalAlignment, VerticalAlignment
from ui.resources.state import KeyboardState, PointerState
from ui.systems.behaviour_system import ActivateSystem, DeleteKeySystem, DeselectSystem, EnterKeySystem, FocusBlinkSystem, FocusSystem, HoverSystem, PressSystem, SelectSystem, TextInputSystem, ToggleSystem, UnfocusSystem
from ui.systems.command_system import SetBackgroundColorSystem, SetFrameColorSystem, SetTextColorSystem
from ui.systems.consistency_system import SelectionGroupConsistencyCheckerSystem
from ui.systems.input_system import ApplicationStateSystem, KeyboardStateSystem, PointerStateSystem
from ui.systems.intent_system import ActivateIntentSystem, KeyIntentSystem, PointerHitTestSystem, PressIntentSystem, TextIntentSystem
from ui.systems.layout_system import LayoutHierarchySystem, WorldTransformationSystem
from ui.systems.renderer_system import BackgroundRendererSystem, FrameRendererSystem, TextRendererSystem
from ui.types import TextStyleDescription
from ui.widgets import ButtonBundle, PanelBundle, RadioButtonBundle, TextBundle, TextInputBundle, ToggleBundle


@dataclass
class TextState:
    value: str
    radio: str
    terrain: Terrain
    toggle: bool


if __name__ == '__main__':
    screen_size = pygame.Vector2(1440, 775)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    pygame_input = PygameEventConverter()
    pygame_renderer = PygameRenderer(screen)

    # text = TextState('', '', Terrain(TerrainType.GRASS, 'green', 'black', True, 2), False)

    world = WorldFactory.create_world()
    world.set_resource(PointerState())
    world.set_resource(KeyboardState())

    world.register_system(SelectionGroupConsistencyCheckerSystem())

    world.register_system(LayoutHierarchySystem())
    world.register_system(WorldTransformationSystem())

    world.register_system(PointerStateSystem())
    world.register_system(KeyboardStateSystem())
    world.register_system(ApplicationStateSystem())

    world.register_system(PointerHitTestSystem())
    world.register_system(PressIntentSystem())
    world.register_system(ActivateIntentSystem())
    world.register_system(TextIntentSystem())
    world.register_system(KeyIntentSystem())

    world.register_system(HoverSystem())
    world.register_system(PressSystem())
    world.register_system(ActivateSystem())
    world.register_system(SelectSystem())
    world.register_system(DeselectSystem())
    world.register_system(ToggleSystem())
    world.register_system(FocusSystem())
    world.register_system(UnfocusSystem())
    world.register_system(FocusBlinkSystem())
    world.register_system(TextInputSystem())
    world.register_system(EnterKeySystem())
    world.register_system(DeleteKeySystem())

    world.register_system(SetFrameColorSystem())
    world.register_system(SetBackgroundColorSystem())
    world.register_system(SetTextColorSystem())    
    
    world.register_system(BackgroundRendererSystem())
    world.register_system(FrameRendererSystem())
    world.register_system(TextRendererSystem())

    # surface_color = InteractionColors(normal=Color(0, 0, 0), pressed=Color(150, 150, 150), selected=Color(200, 200, 200))
    # frame_color = InteractionColors(normal=Color(20, 20, 200), hovered=Color(200, 20, 20), focused=Color(20, 200, 20), selected=Color(20, 200, 200))
    text_color = Color(245, 245, 220)
    
    hoverable = HoverableBundle(
        enter=[SetFrameColorCommand(Color(200, 20, 20))],
        exit=[UnsetFrameColorCommand(Color(200, 20, 20))]
    )
    
    pressable = PressableBundle(
        enter=[SetBackgroundColorCommand(Color(150, 150, 150))],
        exit=[UnsetBackgroundColorCommand(Color(150, 150, 150))]
    )
    
    selectable1 = SelectableBundle(
        group='group',
        enter=[SetFrameColorCommand(Color(0, 0, 0)), SetBackgroundColorCommand(Color(200, 200, 200)), SetTextColorCommand(Color(20, 20, 20))],
        exit=[UnsetFrameColorCommand(Color(0, 0, 0)), UnsetBackgroundColorCommand(Color(200, 200, 200)), UnsetTextColorCommand(Color(20, 20, 20))],
        active=False
    )
    
    selectable2 = SelectableBundle(
        group='group',
        enter=[SetFrameColorCommand(Color(0, 0, 0)), SetBackgroundColorCommand(Color(200, 200, 200)), SetTextColorCommand(Color(20, 20, 20))],
        exit=[UnsetFrameColorCommand(Color(0, 0, 0)), UnsetBackgroundColorCommand(Color(200, 200, 200)), UnsetTextColorCommand(Color(20, 20, 20))],
        active=True
    )
    
    toggleable = ToggleableBundle(
        enter=[SetBackgroundColorCommand(Color(150, 150, 150))],
        exit=[UnsetBackgroundColorCommand(Color(150, 150, 150))],
        active=True
    )

    panel_transform = RectTransformBundle(Vec2(x=300, y=600), Vec2(x=100, y=100), layer=0)
    panel_surface = SurfaceBundle(Color(30, 30, 30), Color(150, 0, 0), 2)
    panel = PanelBundle(WidgetCoreBundle(), panel_transform, PanelLayoutBundle(), panel_surface)

    panel_id = world.spawn(*panel.components())

    text_visual = TextVisualBundle('test\n  line 2\n  end', TextStyleDescription('arial', 16, text_color), horizontal_spacing=7)
    text_transform = RectTransformBundle(Vec2(x=100, y=60), Vec2(x=200, y=400), panel_id, 1)
    text_surface = SurfaceBundle(Color(0, 0, 0), Color(20, 20, 200), 1)
    text = TextBundle(WidgetCoreBundle(), text_visual, text_transform, text_surface)

    button_visual = TextVisualBundle('Button', TextStyleDescription('arial', 16, text_color), HorizontalAlignment.center, VerticalAlignment.middle)
    button_transform = RectTransformBundle(Vec2(x=100, y=30), Vec2(x=0, y=0), panel_id, 1)
    button_surface = SurfaceBundle(Color(0, 0, 0), Color(20, 20, 200), 1)
    activatable = ActivatableBundle()
    button = ButtonBundle(WidgetCoreBundle(), button_visual, button_transform, button_surface, hoverable, pressable, activatable)

    input_text = TextVisualBundle('Text: ', TextStyleDescription('arial', 16, text_color), HorizontalAlignment.left, VerticalAlignment.middle, 5)
    input_transform = RectTransformBundle(Vec2(x=100, y=30), Vec2(x=0, y=100), panel_id, 1)
    input_surface = SurfaceBundle(Color(0, 0, 0), Color(20, 20, 200), 1)
    
    input_inputable = InputBundle('text', {'a'})
    text_input = TextInputBundle(WidgetCoreBundle(), input_text, input_transform, input_surface, hoverable, input_inputable)
  
    int_input_text = TextVisualBundle('Int: ', TextStyleDescription('arial', 16, text_color), HorizontalAlignment.left, VerticalAlignment.middle, 5)
    int_input_transform = RectTransformBundle(Vec2(x=100, y=30), Vec2(x=0, y=150), panel_id, 1)
    int_input_surface = SurfaceBundle(Color(0, 0, 0), Color(20, 20, 200), 1)
    int_input_inputable = InputBundle('0', {'a'})
    int_text_input = TextInputBundle(WidgetCoreBundle(), int_input_text, int_input_transform, int_input_surface, hoverable, int_input_inputable)
  
    radio_text = TextVisualBundle('Radio', TextStyleDescription('arial', 16, text_color), HorizontalAlignment.center, VerticalAlignment.middle)
    radio_transform = RectTransformBundle(Vec2(x=100, y=30), Vec2(x=0, y=200), panel_id, 1)
    radio_surface = SurfaceBundle(Color(0, 0, 0), Color(20, 20, 200), 1)
    radio_button = RadioButtonBundle(WidgetCoreBundle(), radio_text, radio_transform, radio_surface, hoverable, selectable1)

    radio2_text = TextVisualBundle('Radio2', TextStyleDescription('arial', 16, text_color), HorizontalAlignment.center, VerticalAlignment.middle)
    radio2_transform = RectTransformBundle(Vec2(x=100, y=30), Vec2(x=0, y=300), panel_id, 1)
    radio2_surface = SurfaceBundle(Color(0, 0, 0), Color(20, 20, 200), 1)
    radio2_button = RadioButtonBundle(WidgetCoreBundle(), radio2_text, radio2_transform, radio2_surface, hoverable, selectable2)

    toggle_text = TextVisualBundle('Toggle', TextStyleDescription('arial', 16, text_color), HorizontalAlignment.center, VerticalAlignment.middle)
    toggle_transform = RectTransformBundle(Vec2(x=100, y=30), Vec2(x=0, y=500), panel_id, 1)
    toggle_surface = SurfaceBundle(Color(0, 0, 0), Color(20, 20, 200), 1)
    toggle_activatable = ActivatableBundle()
    toggle = ToggleBundle(WidgetCoreBundle(), toggle_text, toggle_transform, toggle_surface, hoverable, toggle_activatable, toggleable)

    world.spawn(*text.components())
    world.spawn(*button.components())
    world.spawn(*text_input.components())
    world.spawn(*int_text_input.components())
    world.spawn(*radio_button.components())
    world.spawn(*radio2_button.components())
    world.spawn(*toggle.components())

    while world._running:

        events = pygame_input.execute()
        for event in events:
            world.push_event(event)

        delta_time = clock.get_time()

        world.execute(delta_time)

        pygame_renderer.render(world.get_draw_commands())

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
