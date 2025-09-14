from dataclasses import dataclass
import pygame

from ecs_framework.ecs import ECS
from ui.systems.event import EventConverterSystem
from ui.systems.mouse_event import CleanupMouseClickedSystem, CleanupMouseReleasedSystem, MouseFocusSystem, MouseHoverSystem, MousePressedSystem, MouseReleasedSystem, MouseSelectSystem, MouseToggleSystem
from ui.widgets import create_button, create_int_text_input, create_panel, create_radio_button, create_text, create_text_input, create_toggle
from ui.systems.keyboard_event import CleanupKeyDownSystem, DeleteKeySystem, EnterKeySystem, TypingKeyDownSystem
from ui.systems.renderer import CleanupRendererSystem, RelativeToRectConverter, RendererSystem
from utils.observable import Observable
from ui.elements import Button, IntTextInput, RadioButton, Text, TextInput, Toggle, Panel
from model.terrain import Terrain, TerrainType


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

    text = TextState('', '', Terrain(TerrainType.GRASS, 'green', 'black', True, 2), False)

    ecs = ECS()
    mouse = ecs.create_entity()
    keyboard = ecs.create_entity()

    panel = create_panel(ecs, pygame.Rect(500, 100, 300, 600))
    create_button(ecs, 'Button', pygame.Rect(10, 10, 100, 30), None, panel)
    create_text_input(ecs, 'Text: ', 'text', pygame.Rect(10, 100, 100, 30), panel)
    create_int_text_input(ecs, 'Int: ', '42', pygame.Rect(10, 150, 100, 30), panel)
    create_radio_button(ecs, 'Radio1', 'group', pygame.Rect(10, 200, 100, 30), panel)
    create_radio_button(ecs, 'Radio2', 'group', pygame.Rect(10, 300, 100, 30), panel)
    create_toggle(ecs, 'Toggle', pygame.Rect(10, 500, 100, 30), panel)
    create_text(ecs, 'Text', pygame.Rect(10, 400, 100, 30), panel)

    ecs.add_system(EventConverterSystem(ecs, mouse, keyboard))

    ecs.add_system(MouseHoverSystem(ecs, mouse))
    ecs.add_system(MouseFocusSystem(ecs, mouse))
    ecs.add_system(MouseToggleSystem(ecs, mouse))
    ecs.add_system(MouseSelectSystem(ecs, mouse))
    ecs.add_system(MousePressedSystem(ecs, mouse))
    ecs.add_system(MouseReleasedSystem(ecs, mouse))

    ecs.add_system(EnterKeySystem(ecs, keyboard))
    ecs.add_system(DeleteKeySystem(ecs, keyboard))
    ecs.add_system(TypingKeyDownSystem(ecs, keyboard))

    ecs.add_system(RelativeToRectConverter(ecs))
    ecs.add_system(RendererSystem(ecs, screen))

    ecs.add_system(CleanupMouseClickedSystem(ecs, mouse))
    ecs.add_system(CleanupMouseReleasedSystem(ecs, mouse))
    ecs.add_system(CleanupKeyDownSystem(ecs, keyboard))
    ecs.add_system(CleanupRendererSystem(ecs))

    panel = Panel(screen, pygame.Rect(100, 100, 300, 600), pygame.Color((30, 30, 30)), pygame.Color('red'))

    radio = Observable('value')
    panel.add_widget(Button(panel.surface, 'Button', pygame.Rect(0, 0, 100, 30), lambda: print('button')))
    panel.add_widget(TextInput(panel.surface, 'Text: ', Observable('text'), pygame.Rect(0, 100, 100, 30), 'blue'))
    panel.add_widget(IntTextInput(panel.surface, 'Int: ', Observable(0), pygame.Rect(0, 150, 100, 30), 'blue'))
    panel.add_widget(RadioButton(panel.surface, 'Radio', 'value', radio, pygame.Rect(0, 200, 100, 30)))
    panel.add_widget(RadioButton(panel.surface, 'Radio', 'value2', radio, pygame.Rect(0, 300, 100, 30)))
    panel.add_widget(Toggle(panel.surface, 'Toggle', Observable(True), pygame.Rect(0, 500, 100, 30)))
    text_widget = Text(panel.surface, 7, 20, pygame.Rect(200, 400, 100, 30))
    panel.add_widget(text_widget)
    text_widget.add_line('test')
    text_widget.add_line('  line 2')
    text_widget.add_line('  end')

    while ecs.running:

        # for event in pygame.event.get():

        #     panel.handle_event(event)

        #     if event.type == pygame.QUIT:
        #         ecs.running = False

        delta_time = clock.get_time()

        panel.draw()
        ecs.execute(delta_time)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
