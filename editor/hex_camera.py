from typing import Optional
import pygame

from model.hex_coordinate import VecF2


class HexCamera:
    MIN_ZOOM = 0.5
    MAX_ZOOM = 3.0
    ZOOM_SPEED = 0.1
    MOVE_SPEED = 10

    def __init__(self, origin: VecF2 = None, zoom: float = 1.0):
        self.zoom = zoom
        self.origin = origin or VecF2(0, 0)
        self.position = self.origin
        self.is_panning = False
        self.last_mouse_position: Optional[VecF2] = None

    def set_origin(self, origin: VecF2) -> None:
        self.origin = origin
        self.position = origin

    def world_to_screen(self, world_position: VecF2) -> VecF2:
        return world_position * self.zoom + self.position

    def screen_to_world(self, screen_position: VecF2) -> VecF2:
        return (screen_position - self.position) / self.zoom

    def zoom_by(self, amount: float) -> None:
        self.zoom += amount
        self.zoom = max(self.MIN_ZOOM, min(self.MAX_ZOOM, self.zoom))

    def move(self, offset: VecF2) -> None:
        self.position += offset
        
    def reset(self) -> None:
        self.position = self.origin
        
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEWHEEL:
            self.zoom_by(event.y * self.ZOOM_SPEED)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            self.is_panning = True
            self.last_mouse_position = VecF2(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            self.is_panning = False
            self.last_mouse_position = None

        elif event.type == pygame.MOUSEMOTION and self.is_panning and self.last_mouse_position:
            current_position = VecF2(event.pos)
            delta = current_position - self.last_mouse_position
            self.move(delta)
            self.last_mouse_position = current_position

    def handle_key_pressed(self, keys: pygame.key.ScancodeWrapper) -> None:
        offset_x, offset_y = 0, 0
        offset_x = (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]) * self.MOVE_SPEED
        offset_y = (keys[pygame.K_UP] - keys[pygame.K_DOWN]) * self.MOVE_SPEED

        if offset_x or offset_y:
            self.move(VecF2(offset_x, offset_y))

        if keys[pygame.K_SPACE]:
            self.reset()
