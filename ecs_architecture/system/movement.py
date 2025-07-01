import math
import time
import pygame
from ecs_architecture.component.path import MoveCommand, MovementProgress, Path, PreviewPath, TargetGridPosition
from ecs_architecture.component.position import GridPosition, GridPositionChanged, WorldPosition
from ecs_framework.ecs import ECS, SystemProtocol
from editor.hex_camera import HexCamera
from model.hex_geometry import HexLayout
from model.hex_map import HexMap
from pathfinding.pathfinding import PathfindingHelper


class PathCalculatorSystem(SystemProtocol):

    def __init__(self, ecs: ECS, hex_map: HexMap):
        self.ecs = ecs
        self.hex_map = hex_map

    def execute(self, delta_time: float):
        for entity, destination in self.ecs.get_entities_with_single_component(TargetGridPosition):
            origin = self.ecs.get_entity_component(entity, GridPosition)
            path = []

            if origin is not None:
                path = PathfindingHelper.astar(self.hex_map, origin.cell, destination.cell)

            if path:
                self.ecs.add_component(entity, PreviewPath(path))
            
            self.ecs.remove_component(entity, TargetGridPosition)


class PathPreviewerSystem(SystemProtocol):

    def __init__(self, ecs: ECS, screen: pygame.Surface, layout: HexLayout, camera: HexCamera):
        self.ecs = ecs
        self.screen = screen
        self.layout = layout
        self.camera = camera

    def execute(self, delta_time: float):
        for _, preview_path in self.ecs.get_entities_with_single_component(PreviewPath):
            coordinates = []
            for cell in preview_path.path:
                hex_center = self.layout.hex_to_point(cell.coordinate)
                screen_point = self.camera.world_to_screen(hex_center)
                coordinates.append(screen_point.as_tuple)
            for index in range(len(coordinates)-1):
                pygame.draw.line(self.screen, pygame.Color('blue'), coordinates[index], coordinates[index+1], 2)


class StartMovementSystem(SystemProtocol):

    def __init__(self, ecs: ECS):
        self.ecs = ecs

    def execute(self, delta_time: float):
        for entity, _ in self.ecs.get_entities_with_single_component(MoveCommand):

            preview_path = self.ecs.get_entity_component(entity, PreviewPath)

            if preview_path is not None:
                path = Path(preview_path.path)
                self.ecs.add_component(entity, path)
                self.ecs.remove_component(entity, PreviewPath)

            self.ecs.remove_component(entity, MoveCommand)

class PathStepperSystem(SystemProtocol):

    def __init__(self, ecs: ECS, layout: HexLayout):
        self.ecs = ecs
        self.layout = layout

    def execute(self, delta_time: float):
        for entity, (grid_position, path) in self.ecs.get_entities_with_components(GridPosition, Path):
            if self.ecs.has_component(MovementProgress) and self.ecs.entity_has_component(entity, MovementProgress):
                continue

            if not path.path:
                self.ecs.remove_component(entity, Path)
                continue

            next_cell = path.path.pop()
            if next_cell.coordinate == grid_position.cell:
                continue

            movement_progress = MovementProgress(self.layout.hex_to_point(grid_position.cell), self.layout.hex_to_point(next_cell.coordinate), next_cell.coordinate)
            self.ecs.add_component(entity, movement_progress)


class MovementSystem(SystemProtocol):

    def __init__(self, ecs: ECS, layout: HexLayout, speed: int):
        self.ecs = ecs
        self.layout = layout
        self.speed = speed
    
    def execute(self, delta_time: float):
        for entity, (movement_progress, world_position) in self.ecs.get_entities_with_components(MovementProgress, WorldPosition):

            step = self.speed * delta_time
            direction = movement_progress.destination - movement_progress.origin
            length = math.hypot(*direction.as_tuple)
            normal_vector = direction / length

            world_position.point = world_position.point + normal_vector * step

            distance = math.hypot(*(movement_progress.destination - world_position.point).as_tuple)

            if distance == 0 or step >= distance:
                self.ecs.add_component(entity, GridPosition(movement_progress.cell))
                self.ecs.add_component(entity, GridPositionChanged())
                self.ecs.remove_component(entity, MovementProgress)
            