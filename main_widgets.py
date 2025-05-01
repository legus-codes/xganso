from dataclasses import dataclass
import pygame

from editor.observable import Observable
from ui.panel import Panel
from ui.widgets import Button, IntTextInput, OptionPicker, RadioButton, RadioStyle, TextInput, Toggle, Widget
from model.terrain import Terrain, TerrainType


@dataclass
class Text:
    value: str
    radio: str
    terrain: Terrain
    toggle: bool


if __name__ == '__main__':
    screen_size = pygame.Vector2(1440, 775)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    text = Text('', '', Terrain(TerrainType.GRASS, 'green', 'black', True, 2), False)

    panel = Panel(screen, pygame.Rect(100, 100, 1000, 600), pygame.Color((30, 30, 30)), pygame.Color('red'))

    radio = Observable('value')
    panel.add_widget(Button(panel.surface, 'Button', pygame.Rect(0, 0, 100, 30), None))
    panel.add_widget(TextInput(panel.surface, 'Text: ', Observable('text'), pygame.Rect(0, 100, 100, 30), 'blue'))
    panel.add_widget(IntTextInput(panel.surface, 'Int: ', Observable(0), pygame.Rect(0, 150, 100, 30), 'blue'))
    panel.add_widget(RadioButton(panel.surface, 'Radio', 'value', radio, pygame.Rect(0, 200, 100, 30)))
    panel.add_widget(RadioButton(panel.surface, 'Radio', 'value2', radio, pygame.Rect(0, 300, 100, 30)))
    panel.add_widget(Toggle(panel.surface, 'Toggle', Observable(True), pygame.Rect(0, 500, 100, 30)))

    running = True

    while running:

        for event in pygame.event.get():

            panel.handle_event(event)

            if event.type == pygame.QUIT:
                running = False

        delta_time = clock.get_time()
        panel.update(delta_time)

        screen.fill((30, 30, 30))

        panel.draw()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
