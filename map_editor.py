import pygame

from ecs_framework.ecs import ECS
from editor.map_editor_controller import MapEditorController


if __name__ == '__main__':
    screen_size = pygame.Vector2(1440, 775)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    world = ECS()
    mouse = world.create_entity()
    keyboard = world.create_entity()

    map_editor = MapEditorController(world, screen, mouse, keyboard)

    while world.running:
        delta_time = clock.get_time()
        world.execute(delta_time)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
