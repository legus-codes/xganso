import pygame

from battle.battle import BattleManager
from battle.battle_view_ui import BattleController
from battle.unit import Party, Unit
from hexio.hex_map_io import HexMapIO

if __name__ == '__main__':
    screen_size = pygame.Vector2(1440, 775)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    archer = Unit('archer', 20, 3, 4, 6, pygame.Color('lightseagreen'))
    knight = Unit('knight', 30, 7, 1, 2, pygame.Color('lightseagreen'))
    mage = Unit('mage', 15, 4, 3, 3, pygame.Color('lightseagreen'))

    goblin = Unit('goblin', 10, 2, 2, 5, pygame.Color('mediumpurple'))
    orc = Unit('orc', 10, 4, 1, 3, pygame.Color('mediumpurple'))

    player_party = Party('Player', 'blue', [archer, knight, mage], True)
    enemy_party = Party('Enemy', 'red', [goblin, orc], False)

    parties = [player_party, enemy_party]
    battle_map = HexMapIO.load('grid.json')
    manager = BattleManager(parties, battle_map)
    manager.setup()
    battle_ui = BattleController(screen, pygame.Rect(150, 40, 1110, 695), manager)

    running = True

    while running:

        screen.fill((30, 30, 30))

        battle_ui.draw()

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
