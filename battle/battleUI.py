import time
from typing import Optional, Tuple
import pygame

from battle.battle import BattleManager, BattlePhase
from editor.hex_map_view import HexCamera, HexDrawer, HexGridRenderer, HexLayout, PointyHexOrientation
from editor.hex_editor_controller import HexGridView, UIComponent
from ui.widgets import Button
from model.hex_coordinate import HexCoordinate


def draw_text(screen: pygame.Surface, text: str, position: pygame.Vector2, color: pygame.Color) -> None:
    font = pygame.font.SysFont('Arial', 16)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


class TurnStartTransition:

    def __init__(self, screen: pygame.Surface, controller: "BattleController"):
        self.screen = screen
        self.controller = controller
        self.fade_in_duration = 0.3
        self.hold_duration = 1.2
        self.fade_out_duration = 0.3
        self.duration = self.fade_in_duration + self.hold_duration + self.fade_out_duration

        self.overlay = pygame.Surface(self.screen.get_size())
        self.overlay.fill((0, 0, 0))
        self.font = pygame.font.SysFont(None, 72)
        self.start_time = None
        self.active = False

        self.party = None

    def start(self, party: str) -> None:
        self.start_time = time.time()
        self.active = True
        self.party = party

    def update(self) -> None:
        if not self.active:
            return
        
        elapsed = time.time() - self.start_time

        if elapsed > self.duration:
            self.active = False
            self.controller.start_turn()
            return
        
        self.draw(elapsed)

    def draw(self, elapsed: float) -> None:
        self.overlay.set_alpha(200)
        self.screen.blit(self.overlay, (0, 0))

        if elapsed < self.fade_in_duration:
            alpha = int(255 * (elapsed / self.fade_in_duration))
        elif elapsed < self.fade_in_duration + self.hold_duration:
            alpha = 255
        else:
            fade_out_elapsed = elapsed - self.fade_in_duration - self.hold_duration
            alpha = int(255 * (1 - (fade_out_elapsed / self.fade_out_duration)))

        alpha = max(0, min(255, alpha))

        text = self.font.render(f'Turn {self.party}', True, (255, 255, 255))
        text.set_alpha(alpha)

        rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, rect)


class InfoPanel:

    def __init__(self, controller: "BattleController", area: pygame.Rect, color: pygame.Color):
        self.controller = controller
        self.state = controller.state
        self.screen = controller.screen
        self.area = area
        self.color = color

    def draw(self) -> None:
        pygame.draw.rect(self.screen, self.color, self.area, 2)
        if self.controller.selected_cell is not None:
            cell = self.controller.selected_cell
            left_pad = 10
            row_size = 20
            draw_text(self.screen, 'Cell', self.area.topleft + pygame.Vector2(left_pad, row_size * 1), pygame.Color('beige'))
            draw_text(self.screen, f'  coordinate: ({cell.coordinate.q}, {cell.coordinate.r})', self.area.topleft + pygame.Vector2(left_pad, row_size * 2), pygame.Color('beige'))
             
            pygame.draw.rect(self.screen, cell.tile.color, pygame.Rect(self.area.topleft + pygame.Vector2(5, row_size * 4), pygame.Vector2(self.area.width - 10, row_size * 4)))
            draw_text(self.screen, 'Tile', self.area.topleft + pygame.Vector2(left_pad, row_size * 4), cell.tile.text_color)
            draw_text(self.screen, f'  type: {cell.tile.kind.name.title()}', self.area.topleft + pygame.Vector2(left_pad, row_size * 5), cell.tile.text_color)
            draw_text(self.screen, f'  walkable: {cell.tile.walkable}', self.area.topleft + pygame.Vector2(left_pad, row_size * 6), cell.tile.text_color)
            draw_text(self.screen, f'  move cost: {cell.tile.move_cost}', self.area.topleft + pygame.Vector2(left_pad, row_size * 7), cell.tile.text_color)
            
            pygame.draw.rect(self.screen, cell.spawn.color, pygame.Rect(self.area.topleft + pygame.Vector2(5, row_size * 9), pygame.Vector2(self.area.width - 10, row_size * 2)))
            draw_text(self.screen, 'Spawn', self.area.topleft + pygame.Vector2(left_pad, row_size * 9), cell.spawn.text_color)
            draw_text(self.screen, f'  type: {cell.spawn.kind.name.replace('_', ' ').title()}', self.area.topleft + pygame.Vector2(left_pad, row_size * 10), cell.spawn.text_color)

            if cell.is_occupied:
                pygame.draw.rect(self.screen, cell.unit.color, pygame.Rect(self.area.topleft + pygame.Vector2(5, row_size * 12), pygame.Vector2(self.area.width - 10, row_size * 7)))
                draw_text(self.screen, 'Unit', self.area.topleft + pygame.Vector2(left_pad, row_size * 12), pygame.Color('black'))
                draw_text(self.screen, f'  name: {cell.unit.name}', self.area.topleft + pygame.Vector2(left_pad, row_size * 13), pygame.Color('black'))
                draw_text(self.screen, f'  party: {cell.unit.party.name}', self.area.topleft + pygame.Vector2(left_pad, row_size * 14), pygame.Color('black'))
                draw_text(self.screen, f'  hp: {cell.unit.hp} / {cell.unit.max_hp}', self.area.topleft + pygame.Vector2(left_pad, row_size * 15), pygame.Color('black'))
                draw_text(self.screen, f'  attack: {cell.unit.attack}', self.area.topleft + pygame.Vector2(left_pad, row_size * 16), pygame.Color('black'))
                draw_text(self.screen, f'  attack range: {cell.unit.attack_range}', self.area.topleft + pygame.Vector2(left_pad, row_size * 17), pygame.Color('black'))
                draw_text(self.screen, f'  movement range: {cell.unit.movement_range}', self.area.topleft + pygame.Vector2(left_pad, row_size * 18), pygame.Color('black'))
            else:
                draw_text(self.screen, 'Unit', self.area.topleft + pygame.Vector2(left_pad, row_size * 12), pygame.Color('beige'))
                draw_text(self.screen, '  none', self.area.topleft + pygame.Vector2(left_pad, row_size * 13), pygame.Color('beige'))


class GameInfoPanel:
    def __init__(self, controller: "BattleController", area: pygame.Rect, color: pygame.Color):
        self.controller = controller
        self.state = controller.state
        self.screen = controller.screen
        self.area = area
        self.color = color

    def draw(self) -> None:
        pygame.draw.rect(self.screen, self.color, self.area, 2)
        left_pad = 10
        row_size = 20
        draw_text(self.screen, f'Round {self.state.round}', self.area.topleft + pygame.Vector2(left_pad, row_size * 1), pygame.Color('beige'))
        draw_text(self.screen, 'Battle Phase', self.area.topleft + pygame.Vector2(left_pad, row_size * 3), pygame.Color('beige'))
        draw_text(self.screen, f'  {self.state.state.name.replace('_', ' ').title()}', self.area.topleft + pygame.Vector2(left_pad, row_size * 4), pygame.Color('beige'))
            
        draw_text(self.screen, 'Turn Order', self.area.topleft + pygame.Vector2(left_pad, row_size * 6), pygame.Color('beige'))
        for index, party in enumerate(self.state.turn_order):
            draw_text(self.screen, f'  {party.name}', self.area.topleft + pygame.Vector2(left_pad, row_size * (7+index)), pygame.Color('beige'))


class ActionPanel:

    def __init__(self, controller: "BattleController", area: pygame.Rect, color: pygame.Color):
        self.controller = controller
        self.state = controller.state
        self.screen = controller.screen
        self.area = area
        self.color = color
        self.buttons = {
            BattlePhase.START_BATTLE: [Button(self.screen, 'Start Game', pygame.Rect(1265, 700, 170, 30), self.controller.start_battle)],
            BattlePhase.TURN_START: [],
            BattlePhase.PLANNING_PHASE: [
                Button(self.screen, 'Move', pygame.Rect(1265, 630, 170, 30), None),
                Button(self.screen, 'Attack', pygame.Rect(1265, 665, 170, 30), None),
                Button(self.screen, 'Execute', pygame.Rect(1265, 700, 170, 30), None)
            ]
        }

    def handle_event(self, event) -> None:
        for button in self.buttons[self.state.state]:
            button.handle_event(event)

    def draw(self) -> None:
        pygame.draw.rect(self.screen, self.color, self.area, 2)
        for button in self.buttons[self.state.state]:
            button.draw()


class HexGridView:

    def __init__(self, controller: "BattleController", area: pygame.Rect, color: pygame.Color):
        self.controller = controller
        self.state = controller.state
        self.screen = controller.screen
        self.area = area
        self.color = color
        self.renderer = HexGridRenderer(self.screen, self.area, self.controller.layout, self.controller.camera)

    def handle_event(self, event) -> None:
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button not in (4, 5)):
            coordinate = self._get_hex_mouse(event.pos)
            if coordinate is not None:
                self.controller.on_click(coordinate)

        # if event.type == pygame.MOUSEMOTION:
        #     coordinate = self._get_hex_mouse(event.pos)
        #     if coordinate is not None:
        #         self.controller.on_mouse_move(coordinate)

        # if event.type == pygame.KEYDOWN:
        #     self.controller.on_key_down(event.unicode)

        # if self.state.mode == HexEditorMode.TEST and (self.state.calculation != self.state.test_tool or self.state.used_distance != self.state.distance):
        #     self.grid_editor.update_cells()
        
    def draw(self) -> None:
        pygame.draw.rect(self.screen, self.color, self.area, 2)
        self.renderer.draw_grid(self.state.battle_map)

        # if self.state.mode == HexEditorMode.TEST and self.state.selected_cell is not None:
        #     for cell in self.state.cells:
        #         self.renderer.draw_hex(cell.coordinate, pygame.Color('gold'), pygame.Color('white'))
        #     self.renderer.draw_hex(self.state.selected_cell, pygame.Color('blue'), pygame.Color('white'))

    def _get_hex_mouse(self, mouse_position: Tuple[int, int]) -> Optional[HexCoordinate]:
        pixel = pygame.Vector2(mouse_position)
        if not self.area.collidepoint(pixel):
            return None
        return HexDrawer.pixel_to_hex(pixel, self.controller.layout, self.controller.camera)


class BattleController:

    def __init__(self, screen: pygame.Surface, grid_area: pygame.Rect, state: BattleManager):
        self.screen = screen
        self.grid_area = grid_area
        self.state = state
        self.selected_cell = None
        self.layout = HexLayout(PointyHexOrientation(), pygame.Vector2(grid_area.center), pygame.Vector2(20, 20))
        self.camera = HexCamera(1.0, pygame.Vector2(0, 0))

        self.game_info_panel = GameInfoPanel(self, pygame.Rect(0, 40, 150, 695), pygame.Color(225, 225, 225))
        self.info_panel = InfoPanel(self, pygame.Rect(1260, 40, 180, 500), pygame.Color(225, 225, 225))
        self.action_panel = ActionPanel(self, pygame.Rect(1260, 540, 180, 195), pygame.Color(100, 225, 225))

        self.turn_start_transition = TurnStartTransition(self.screen, self)
        # self.top_bar = TopBarMenu(self, pygame.Rect(0, 0, 1440, 40), pygame.Color(225, 225, 225))
        # self.tool_menu: Dict[HexEditorMode, UIComponent] = {
        #     HexEditorMode.EDIT: EditToolMenu(self, pygame.Rect(0, 40, 150, 695), pygame.Color(225, 225, 225)),
        #     HexEditorMode.TEST: TestToolMenu(self, pygame.Rect(0, 40, 150, 695), pygame.Color(100, 225, 225))
        # }
        # self.tile_palette_popup = TilePalettePopUp(self, pygame.Rect(150, 225, 100, len(self.state.tiles.tiles) * 35 + 5), pygame.Color(230, 100, 230))
        # self.spawn_palette_popup = SpawnPalettePopUp(self, pygame.Rect(150, 260, 150, len(self.state.spawns.data) * 35 + 5), pygame.Color(230, 230, 100))
        self.grid_view = HexGridView(self, pygame.Rect(150, 40, 1110, 695), pygame.Color('blue'))

    def on_click(self, coordinate: HexCoordinate) -> None:
        if self.state.state == BattlePhase.START_BATTLE:
            if self.state.battle_map.has_cell(coordinate):
                self.selected_cell = self.state.battle_map.cells[coordinate]
            else:
                self.selected_cell = None

    def start_battle(self) -> None:
        self.state.next_turn()
        self.turn_start_transition.start(self.state.turn_manager.party.name)

    def start_turn(self) -> None:
        self.state.start_planning()

    # def on_mouse_move(self, coordinate: HexCoordinate) -> None:
    #     self.editor.mouse_move(coordinate)

    # def on_key_down(self, key: chr) -> None:
    #     self.editor.key_down(key)

    def handle_event(self, event) -> None:
        self.grid_view.handle_event(event)
        self.action_panel.handle_event(event)
        self.camera.handle_event(event)

    def handle_key_pressed(self, keys: pygame.key.ScancodeWrapper) -> None:
        self.camera.handle_key_pressed(keys)

    def update(self) -> None:
        self.turn_start_transition.update()

    def draw(self) -> None:
        self.game_info_panel.draw()
        self.info_panel.draw()
        self.action_panel.draw()
        self.grid_view.draw()
