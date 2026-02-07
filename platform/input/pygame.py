from typing import List
import pygame

from core.primitives import IVec2
from ecs_framework.ecs import EventProtocol
from platform.input.events import KeyDown, MouseButton, MouseButtonDown, MouseMove, MouseButtonUp, QuitRequested


class PygameEventConverter:

    def execute(self) -> List[EventProtocol]:
        events = []

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                events.append(MouseMove(IVec2(*event.pos)))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    events.append(MouseButtonDown(IVec2(*event.pos), MouseButton.left))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    events.append(MouseButtonUp(IVec2(*event.pos), MouseButton.left))

            elif event.type == pygame.KEYDOWN:
                events.append(KeyDown(event.unicode, event.key))

            if event.type == pygame.QUIT:
                events.append(QuitRequested())

        return events
