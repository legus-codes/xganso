import pygame

from pygame import Vector2
from battle.unit import Character
from command import MoveCommand
from model.hex_map import CubeHexGrid, HexCell, HexMath
from editor.hex_map_view import FlatCubeHexLayout, HexDrawer, HexLayout, PointyCubeHexLayout, PointyOffsetHexLayout
from battle.battle import TurnManager

screen_size = Vector2(800, 600)
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


running = True

pointy_layout = PointyCubeHexLayout(screen_size/2, Vector2(20, 20))
flat_layout = FlatCubeHexLayout(screen_size/2, Vector2(20, 20))

hex_layout = pointy_layout

size = 9
grid = CubeHexGrid()
grid.change_size(size)

hero = Character('hero', 20, 4, 3, HexCell(0, 0), 10, pygame.Color('lightseagreen'))
enemy = Character('enemy', 10, 15, 1, HexCell(6, 3), 2, pygame.Color('mediumpurple'))
characters = [hero, enemy]

turn = TurnManager()
turn.set_characters(hero, 0)
turn.set_characters(enemy, 1)
turn.next_turn()

path = []
status = ''

while running:
    screen.fill((30, 30, 30))
    
    for cell in grid.cells:
        draw_hex(cell, hex_layout, pygame.Color('aqua'))

    planning_phase = turn.phase == 'planning' and turn.character is not None
    
    planning_action = None
    if planning_phase:
        planning_action = turn.actions

        if status == 'move':
            for cell in HexMath.hex_range(planning_action.current_position, planning_action.remaining_movement):
                if grid.has_cell(cell):
                    draw_hex(cell, hex_layout, pygame.Color('blue'))

        if status == 'attack':
            for cell in HexMath.hex_range(planning_action.current_position, planning_action.attack_range):
                if grid.has_cell(cell):
                    draw_hex(cell, hex_layout, pygame.Color('moccasin'))

        for cell in path:
            if grid.has_cell(cell):
                draw_hex(cell, hex_layout, pygame.Color('gold'))

        for index, cell in enumerate(planning_action.movement_positions):
            draw_hex(cell, hex_layout, pygame.Color('fuchsia'))
            draw_text(str(index), pygame.Color('black'), HexDrawer.hex_to_pixel(cell, hex_layout) - Vector2(5, 10))

        for index, cell in enumerate(planning_action.attack_positions):
            draw_hex(cell, hex_layout, pygame.Color('orange'))
            draw_text(str(index), pygame.Color('black'), HexDrawer.hex_to_pixel(cell, hex_layout) - Vector2(5, 10))

    for character in characters:
        draw_circle(character.position, hex_layout, character.color)
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'u':
                if planning_phase:
                    if status == 'move':
                        planning_action.undo_movement()
                    elif status == 'attack':
                        planning_action.undo_attack()
            if event.unicode == 'd':
                if planning_phase:
                    planning_action.undo_movement()
            if event.unicode == 'm':
                if planning_phase:
                    status = 'move'
            if event.unicode == 'a':
                if planning_phase:
                    status = 'attack'
                    path = []
            if event.unicode == 's':
                if planning_phase:
                    status = ''
                    path = []
            elif event.unicode == 'e':
                if planning_phase:
                    turn.execute()
            elif event.unicode == 'n':
                if turn.phase == 'executing':
                    turn.next_turn()
                    status = ''

        if event.type == pygame.MOUSEBUTTONDOWN:
            pixel = Vector2(event.pos)
            cell = HexDrawer.pixel_to_hex(pixel, hex_layout)

            if planning_phase:
                if status == 'move':
                    planning_action.plan_movement(path[0])
                    path = []
                elif status == 'attack':
                    for character in characters:
                        print(character.position, cell)
                        if character.position == cell:
                            planning_action.plan_attack(character)

        if event.type == pygame.MOUSEMOTION:
            if planning_phase:
                if status == 'move':
                    pixel = Vector2(event.pos)
                    cell = HexDrawer.pixel_to_hex(pixel, hex_layout)
                    path = HexMath.astar(planning_action.current_position, cell)[-(planning_action.remaining_movement+1):]

        if event.type == pygame.QUIT:
            running = False
    clock.tick(60)

pygame.quit()