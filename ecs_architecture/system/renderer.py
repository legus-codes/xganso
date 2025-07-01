import math
import pygame
from ecs_architecture.component.position import GridPosition, GridPositionChanged, ScreenPosition, WorldPosition
#from ecs_architecture.component.render_layer import RenderLayer
from ecs_architecture.component.sprite import ScreenSprite, Sprite
from ecs_framework.ecs import ECS, SystemProtocol
from editor.hex_camera import HexCamera
from model.hex_coordinate import VecF2
from model.hex_geometry import HexLayout


class SyncGridToWorldPositionSystem(SystemProtocol):

    def __init__(self, ecs: ECS, layout: HexLayout):
        self.ecs = ecs
        self.layout = layout

    def execute(self, delta_time: float):
        for entity, (grid_position, _) in self.ecs.get_entities_with_components(GridPosition, GridPositionChanged):
            world_center = self.layout.hex_to_point(grid_position.cell)
            world_position = WorldPosition(world_center)

            self.ecs.add_component(entity, world_position)
            self.ecs.remove_component(entity, GridPositionChanged)
            

class WorldToScreenPositionSystem(SystemProtocol):

    def __init__(self, ecs: ECS, camera: HexCamera):
        self.ecs = ecs
        self.camera = camera

    def execute(self, delta_time: float):
        for entity, world_position in self.ecs.get_entities_with_single_component(WorldPosition):
            screen_coordinates = self.camera.world_to_screen(world_position.point)
            screen_position = ScreenPosition(screen_coordinates)
            
            self.ecs.add_component(entity, screen_position)


class SpriteScalerSystem(SystemProtocol):

    def __init__(self, ecs: ECS, camera: HexCamera):
        self.ecs = ecs
        self.camera = camera

    def execute(self, delta_time: float):
        for entity, sprite in self.ecs.get_entities_with_single_component(Sprite):
            screen_sprite = ScreenSprite(pygame.transform.scale_by(sprite.sprite, self.camera.zoom))
            self.ecs.add_component(entity, screen_sprite)


class RendererSystem(SystemProtocol):

    def __init__(self, ecs: ECS, screen: pygame.Surface):
        self.ecs = ecs
        self.screen = screen

    def execute(self, delta_time: float):
        for _, (screen_position, sprite) in self.ecs.get_entities_with_components(ScreenPosition, ScreenSprite):
            adjusted_cell_position = screen_position.point - VecF2(*sprite.sprite.get_size()) / 2
            self.screen.blit(sprite.sprite, adjusted_cell_position.as_tuple)
            