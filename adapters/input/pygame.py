import pygame
from typing import Iterable

from core.primitives import IVec2
from adapters.input.events import Key, KeyDown, KeyUp, MouseButton, MouseButtonDown, MouseMove, MouseButtonUp, QuitRequested, TextInput
from omniecs.types import Event


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
                key = self.get_key(event.key)
                if key:
                    yield KeyDown(key)

            elif event.type == pygame.KEYUP:
                key = self.get_key(event.key)
                if key:
                    yield KeyUp(key)

            elif event.type == pygame.TEXTINPUT:
                yield TextInput(event.text)

            if event.type == pygame.QUIT:
                yield QuitRequested()

    def get_key(self, key: int) -> Key | None:
        try:
            return Key(key)
        except ValueError:
            return None
