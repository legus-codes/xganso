import pygame
from typing import Iterable

from core.primitives import IVec2
from adapters.input.events import KeyDown, MouseButton, MouseButtonDown, MouseMove, MouseButtonUp, QuitRequested, TextInput
from ecs_framework.types import Event


class PygameEventConverter:

    def execute(self) -> Iterable[Event]:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                yield MouseMove(IVec2(*event.pos))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    yield MouseButtonDown(IVec2(*event.pos), MouseButton.left)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    yield MouseButtonUp(IVec2(*event.pos), MouseButton.left)

            elif event.type == pygame.KEYDOWN:
                yield KeyDown(event.key)

            elif event.type == pygame.KEYUP:
                yield KeyDown(event.key)

            elif event.type == pygame.TEXTINPUT:
                yield TextInput(event.text)

            if event.type == pygame.QUIT:
                yield QuitRequested()
