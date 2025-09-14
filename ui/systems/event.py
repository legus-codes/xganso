import pygame
from ecs_framework.ecs import ECS, SystemProtocol
from ui.components.input import KeyDown, MouseButton, MouseClicked, MousePosition, MousePressed, MouseReleased


class EventConverterSystem(SystemProtocol):

    def __init__(self, world: ECS, mouse: int, keyboard: int):
        self.world = world
        self.mouse = mouse
        self.keyboard = keyboard

    def execute(self, delta_time: float):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                self.world.add_component(self.mouse, MousePosition(event.pos))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.world.add_component(self.mouse, MouseClicked(MouseButton.left, event.pos))
                    self.world.add_component(self.mouse, MousePressed(MouseButton.left))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.world.add_component(self.mouse, MouseReleased(MouseButton.left, event.pos))
                    self.world.remove_component(self.mouse, MousePressed)
            elif event.type == pygame.KEYDOWN:
                self.world.add_component(self.keyboard, KeyDown(event.unicode, event.key))

            if event.type == pygame.QUIT:
                self.world.running = False