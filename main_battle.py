import pygame

from battle.battle import BattleManager
from battle.battle_view_ui import BattleController
from battle.unit import Party, Unit
from ecs_architecture.component.grid_position import GridPosition
from ecs_architecture.component.sprite import Sprite
from ecs_architecture.system.renderer_system import RendererSystem
from ecs_framework.ecs import ECS
from hexio.hex_map_io import HexMapIO

if __name__ == '__main__':
    screen_size = pygame.Vector2(1440, 775)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    ecs = ECS()
    archer = Unit('archer', 20, 3, 4, 6, pygame.Color('lightseagreen'))
    archer_entity = ecs.create_entity()
    ecs.add_component(archer_entity, Sprite(pygame.image.load('images\\archer_small.png')))

    knight = Unit('knight', 30, 7, 1, 2, pygame.Color('lightseagreen'))
    knight_entity = ecs.create_entity()
    ecs.add_component(knight_entity, Sprite(pygame.image.load('images\\knight_small.png')))

    mage = Unit('mage', 15, 4, 3, 3, pygame.Color('lightseagreen'))
    mage_entity = ecs.create_entity()
    ecs.add_component(mage_entity, Sprite(pygame.image.load('images\\mage_small.png')))

    rogue = Unit('rogue', 10, 10, 1, 8, pygame.Color('lightseagreen'))
    rogue_entity = ecs.create_entity()
    ecs.add_component(rogue_entity, Sprite(pygame.image.load('images\\rogue_small.png')))

    bard = Unit('bard', 25, 3, 5, 3, pygame.Color('lightseagreen'))
    bard_entity = ecs.create_entity()
    ecs.add_component(bard_entity, Sprite(pygame.image.load('images\\bard_small.png')))

    goblin = Unit('goblin', 10, 2, 2, 5, pygame.Color('mediumpurple'))
    orc = Unit('orc', 10, 4, 1, 3, pygame.Color('mediumpurple'))

    player_party = Party('Player', 'blue', [archer, knight, mage, rogue, bard], True)
    enemy_party = Party('Enemy', 'red', [goblin, orc], False)

    parties = [player_party, enemy_party]
    battle_map = HexMapIO.load('grid.json')
    manager = BattleManager(parties, battle_map)
    manager.setup()
    battle_ui = BattleController(screen, pygame.Rect(150, 40, 1110, 695), manager)

    ecs.add_component(archer_entity, GridPosition(*archer.position.vector.as_tuple))
    ecs.add_component(knight_entity, GridPosition(*knight.position.vector.as_tuple))
    ecs.add_component(mage_entity, GridPosition(*mage.position.vector.as_tuple))
    ecs.add_component(rogue_entity, GridPosition(*rogue.position.vector.as_tuple))
    ecs.add_component(bard_entity, GridPosition(*bard.position.vector.as_tuple))

    ecs.add_system(RendererSystem(ecs, screen, battle_ui.layout, battle_ui.camera))

    running = True

    while running:

        screen.fill((30, 30, 30))

        battle_ui.draw()
        ecs.execute()

        # pygame.draw.rect(screen, line_color, (0, 735, 1440, 40), 2)

        battle_ui.update()

        pygame.display.flip()

        for event in pygame.event.get():

            battle_ui.handle_event(event)

            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        battle_ui.handle_key_pressed(keys)

        clock.tick(60)

    pygame.quit()
