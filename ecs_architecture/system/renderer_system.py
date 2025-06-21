import pygame
from ecs_architecture.component.grid_position import GridPosition
#from ecs_architecture.component.render_layer import RenderLayer
from ecs_architecture.component.sprite import Sprite
from ecs_framework.ecs import ECS, SystemProtocol
from editor.hex_camera import HexCamera
from model.hex_coordinate import HexCoordinate, VecF2
from model.hex_geometry import HexLayout


class RendererSystem(SystemProtocol):

    def __init__(self, ecs: ECS, screen: pygame.Surface, layout: HexLayout, camera: HexCamera):
        self.ecs = ecs
        self.screen = screen
        self.layout = layout
        self.camera = camera

    def execute(self):
        for entity in self.ecs.get_entities_with(GridPosition, Sprite):
            grid_position = self.ecs.get_entity_component(entity, GridPosition)
            sprite = self.ecs.get_entity_component(entity, Sprite)
            # render_layer = self.ecs.get_entity_component(entity, RenderLayer) if self.ecs.entity_has_component(entity, RenderLayer) else 1
            world_position = self.layout.hex_to_topleft(HexCoordinate(grid_position.q, grid_position.r))
            screen_position = self.camera.world_to_screen(world_position)
            self.screen.blit(pygame.transform.scale_by(sprite.sprite, self.camera.zoom), screen_position.as_tuple)
            