import pygame

from pygame import Vector2
from battle.unit import Character, Party
from gamemanager import GameManager, Phase
from model.hex_map import CubeHexGrid, HexCell, HexMath
from editor.hex_map_view import HexDrawer, HexLayout, PointyCubeHexLayout
from map import BattleMap
import itertools

from battle.battle import PlannedAction

screen_size = Vector2(900, 700)
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()


def draw_text(text: str, color: pygame.Color, position: Vector2) -> None:
    font = pygame.font.SysFont('Arial', 20)
    img = font.render(text, True, color)
    screen.blit(img, position)


def draw_hex(cell: HexCell, layout: HexLayout, color: pygame.Color) -> None:
    corners = HexDrawer.get_hex(cell, layout)
    pygame.draw.polygon(screen, color, corners)
    pygame.draw.polygon(screen, (255, 255, 255), corners, 2)


def draw_circle(cell: HexCell, layout: HexLayout, color: pygame.Color) -> None:
    pygame.draw.circle(screen, color, HexDrawer.hex_to_pixel(cell, layout), 12)
    pygame.draw.circle(screen, (0, 0, 0), HexDrawer.hex_to_pixel(cell, layout), 12, 2)


def draw_rectangle(rectangle: pygame.Rect, color: pygame.Color) -> None:
    pygame.draw.rect(screen, color, rectangle)


def draw_arrow(origin: Vector2, target: Vector2) -> None:
    pygame.draw.line(screen, pygame.Color('black'), origin, target, 2)


def draw_party(party: Party, rectangle: pygame.Rect) -> None:
    draw_rectangle(rectangle, pygame.Color('black'))
    for index, character in enumerate(party.members):
        draw_circle(character.position, hex_layout, character.color)
        draw_text(character.name[0].capitalize(), pygame.Color('black'), HexDrawer.hex_to_pixel(character.position, hex_layout) - Vector2(7, 12))
        draw_text(f'{character.name} {character.hp}hp', pygame.Color('beige'), Vector2(rectangle.left + 5, rectangle.top + 5 + index * 30))


def draw_character_information(character: Character) -> None:
    draw_text(character.name, pygame.Color('beige'), Vector2(15, 645))

    draw_text(f'HP: {character.hp}', pygame.Color('beige'), Vector2(115, 645))
    draw_text(f'Attack: {character.attack}', pygame.Color('beige'), Vector2(115, 670))

    draw_text(f'Attack Range: {character.attack_range}', pygame.Color('beige'), Vector2(215, 645))
    draw_text(f'Movement Range: {character.movement_range}', pygame.Color('beige'), Vector2(215, 670))


running = True

pointy_layout = PointyCubeHexLayout(screen_size/2 - Vector2(0, 10), Vector2(20, 20))
hex_layout = pointy_layout

size = 9
grid = CubeHexGrid()
grid.change_size(size)

starting_position_a = list(map(lambda x: HexCell(x[0], x[1]), itertools.product([7, 8, 9], [-7, -8, -9])))
starting_position_b = list(map(lambda x: HexCell(x[0], x[1]), itertools.product([-7, -8, -9], [7, 8, 9])))

battle_map = BattleMap(grid, [starting_position_a, starting_position_b])

archer = Character('archer', 20, 3, 4, 6, pygame.Color('lightseagreen'))
knight = Character('knight', 30, 7, 1, 2, pygame.Color('lightseagreen'))
mage = Character('mage', 15, 4, 3, 3, pygame.Color('lightseagreen'))

goblin = Character('goblin', 10, 2, 2, 5, pygame.Color('mediumpurple'))
orc = Character('orc', 10, 4, 1, 3, pygame.Color('mediumpurple'))

player_party = Party('Player')
player_party.add_member(archer)
player_party.add_member(knight)
player_party.add_member(mage)

enemy_party = Party('Enemy')
enemy_party.add_member(goblin)
enemy_party.add_member(orc)

game_manager = GameManager(player_party, enemy_party, battle_map)
game_manager.setup_battle()

selected_character: Character = None
planned_action: PlannedAction = None

path = []
status = ''

while running:
    screen.fill((30, 30, 30))
    
    for cell in grid.cells:
        draw_hex(cell, hex_layout, pygame.Color('aqua'))

    draw_rectangle(pygame.Rect(5, 5, 890, 40), pygame.Color('black'))
    draw_text(f'Phase: {game_manager.phase.name}', pygame.Color('beige'), Vector2(500, 15))
    draw_text(f'Turn: {game_manager.turn_manager.party.name}', pygame.Color('beige'), Vector2(200, 15))

    draw_rectangle(pygame.Rect(5, 640, 890, 60), pygame.Color('black'))

    if selected_character:
        draw_character_information(selected_character)

        if planned_action:
            if planned_action.move_command is None:
                for cell in HexMath.hex_range(planned_action.current_position, planned_action.move_range + planned_action.attack_range):
                    if grid.has_cell(cell):
                        draw_hex(cell, hex_layout, pygame.Color('moccasin'))
                for cell in HexMath.hex_range(planned_action.current_position, planned_action.move_range):
                    if grid.has_cell(cell):
                        draw_hex(cell, hex_layout, pygame.Color('blue'))
            else:
                for cell in HexMath.hex_range(planned_action.current_position, planned_action.attack_range):
                    if grid.has_cell(cell):
                        draw_hex(cell, hex_layout, pygame.Color('moccasin'))


        for cell in path:
            if grid.has_cell(cell):
                draw_hex(cell, hex_layout, pygame.Color('gold'))

    for actions in game_manager.turn_manager.actions.values():
        if actions.move_command is not None:
            destination_pixel = HexDrawer.hex_to_pixel(actions.move_command.target, hex_layout)
            draw_arrow(HexDrawer.hex_to_pixel(actions.move_command.origin, hex_layout), destination_pixel)
            draw_hex(actions.move_command.target, hex_layout, pygame.Color('fuchsia'))
            draw_text(actions.character.name[0].capitalize(), pygame.Color('black'), destination_pixel - Vector2(7, 12))


    draw_party(player_party, pygame.Rect(10, 50, 150, 100))
    draw_party(enemy_party, pygame.Rect(740, 50, 150, 100))

    # planning_phase = turn.phase == 'planning' and turn.character is not None
    
    # planning_action = None
    # if planning_phase:
    #     planning_action = turn.actions

    #     if status == 'move':
    #         for cell in HexMath.hex_range(planning_action.current_position, planning_action.remaining_movement):
    #             if grid.has_cell(cell):
    #                 draw_hex(cell, hex_layout, pygame.Color('blue'))

    #     if status == 'attack':
    #         for cell in HexMath.hex_range(planning_action.current_position, planning_action.attack_range):
    #             if grid.has_cell(cell):
    #                 draw_hex(cell, hex_layout, pygame.Color('moccasin'))


    #     for index, cell in enumerate(planning_action.movement_positions):
    #         draw_hex(cell, hex_layout, pygame.Color('fuchsia'))
    #         draw_text(str(index), pygame.Color('black'), HexDrawer.hex_to_pixel(cell, hex_layout) - Vector2(5, 10))

    #     for index, cell in enumerate(planning_action.attack_positions):
    #         draw_hex(cell, hex_layout, pygame.Color('orange'))
    #         draw_text(str(index), pygame.Color('black'), HexDrawer.hex_to_pixel(cell, hex_layout) - Vector2(5, 10))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'p':
                game_manager.change_phase(Phase.Planning)
            elif event.unicode == 'e':
                game_manager.change_phase(Phase.Execution)
                selected_character = None
                
    #         if event.unicode == 'u':
    #             if planning_phase:
    #                 if status == 'move':
    #                     planning_action.undo_movement()
    #                 elif status == 'attack':
    #                     planning_action.undo_attack()
    #         if event.unicode == 'd':
    #             if planning_phase:
    #                 planning_action.undo_movement()

            if event.unicode == 'm':
                if selected_character and path:
                    planned_action.plan_movement(path[0])
                    path = []



    #         if event.unicode == 'a':
    #             if planning_phase:
    #                 status = 'attack'
    #                 path = []
    #         if event.unicode == 's':
    #             if planning_phase:
    #                 status = ''
    #                 path = []
    #         elif event.unicode == 'e':
    #             if planning_phase:
    #                 turn.execute()
    #         elif event.unicode == 'n':
    #             if turn.phase == 'executing':
    #                 turn.next_turn()
    #                 status = ''

        if event.type == pygame.MOUSEBUTTONDOWN:
            pixel = Vector2(event.pos)
            cell = HexDrawer.pixel_to_hex(pixel, hex_layout)

            if game_manager.phase == Phase.Planning:
                for character in game_manager.characters:
                    if character.position == cell:
                        selected_character = character
                        if character in game_manager.turn_manager.party.members:
                            planned_action = game_manager.turn_manager.actions[character]
                        break
                    selected_character = None
                    planned_action = None

    #         if planning_phase:
    #             if status == 'move':
    #                 planning_action.plan_movement(path[0])
    #                 path = []
    #             elif status == 'attack':
    #                 for character in characters:
    #                     print(character.position, cell)
    #                     if character.position == cell:
    #                         planning_action.plan_attack(character)

        if event.type == pygame.MOUSEMOTION:
            if selected_character and planned_action is not None and planned_action.move_command is None:
                pixel = Vector2(event.pos)
                cell = HexDrawer.pixel_to_hex(pixel, hex_layout)
                path = HexMath.astar(planned_action.current_position, cell)[-(planned_action.move_range+1):]

        if event.type == pygame.QUIT:
            running = False
    clock.tick(60)

pygame.quit()