from dataclasses import dataclass
import pygame

from ecs_framework.ecs import ECS
from ui.ecs_elements import create_button, create_int_text_input, create_radio_button, create_text, create_text_input, create_toggle
from ui.ui_system import UIRendererSystem
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
    create_button(ecs, 'Button', pygame.Rect(500, 100, 100, 30))
    create_text_input(ecs, 'Text: ', pygame.Rect(500, 200, 100, 30))
    create_int_text_input(ecs, 'Int: ', pygame.Rect(500, 250, 100, 30))
    create_radio_button(ecs, 'Radio1', pygame.Rect(500, 300, 100, 30))
    create_radio_button(ecs, 'Radio2', pygame.Rect(500, 400, 100, 30))
    create_toggle(ecs, 'Toggle', pygame.Rect(500, 600, 100, 30))
    create_text(ecs, 'Text', pygame.Rect(500, 500, 100, 30))

    ecs.add_system(UIRendererSystem(ecs, screen))

    panel = Panel(screen, pygame.Rect(100, 100, 300, 600), pygame.Color((30, 30, 30)), pygame.Color('red'))

    radio = Observable('value')
    panel.add_widget(Button(panel.surface, 'Button', pygame.Rect(0, 0, 100, 30), None))
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

    running = True

    while running:

        for event in pygame.event.get():

            panel.handle_event(event)

            if event.type == pygame.QUIT:
                running = False

        delta_time = clock.get_time()

        screen.fill((30, 30, 30))

        panel.draw()
        ecs.execute()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
