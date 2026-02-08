from typing import Iterable
import pygame

from core.primitives import IVec2
from ecs_framework.managers.event_manager import Event
from adapters.input.events import KeyDown, MouseButton, MouseButtonDown, MouseMove, MouseButtonUp, QuitRequested


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
                yield KeyDown(event.unicode, event.key)

            if event.type == pygame.QUIT:
                yield QuitRequested()
