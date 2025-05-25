import time
from typing import Dict, List
import pygame

from battle.battle import BattleManager, BattlePhase
from battle.battle_view_state import BattleViewState
from editor.hex_editor_state import UIContext
from editor.hex_editor_ui import CellInformationPanel
from editor.hex_map_view import HexCamera, HexLayout, HexMapView
from model.hex_geometry import POINTY
from model.hex_map import HexMap
from ui.elements import Button, Panel, Text
from model.hex_coordinate import HexCoordinate, VecF2


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


class GameInformationPanel(Panel):

    def __init__(self, ui_context: UIContext, area: pygame.Rect, background: pygame.Color, frame_color: pygame.Color):
        super().__init__(ui_context.screen, area, background, frame_color)
        self.state = ui_context.state
        self.build_widgets()
        self.state.round.bind(self.on_change_round_information)
        self.state.state.bind(self.on_change_round_information)
        self.on_change_round_information(None)

    def build_widgets(self) -> None:
        self.cell_text = Text(self.surface, 8, 20, pygame.Rect(5, 5, 140, 30))
        self.add_widget(self.cell_text)

    def on_change_round_information(self, _) -> None:
        self.cell_text.reset()
        text = [
            f'Round {self.state.round.get()}',
            '',
            'Battle Phase',
            f'  {self.state.state.get().name.replace('_', ' ').title()}',
            '',
            'Turn Order',
        ]
        for index, party in enumerate(self.state.turn_order):
            text.append(f'  {party.name}')
        self.cell_text.set_text(text)


class ActionPanel(Panel):

    def __init__(self, ui_context: UIContext, area: pygame.Rect, background: pygame.Color, frame_color: pygame.Color):
        super().__init__(ui_context.screen, area, background, frame_color)
        self.controller = ui_context.controller
        self.state = ui_context.state
        self.build_widgets()
        self.state.state.bind(self.on_change_round_state)
        self.on_change_round_state(self.state.state.get())

    def build_widgets(self) -> None:
        self.buttons: Dict[BattlePhase, List[Button]] = {
            BattlePhase.START_BATTLE: [Button(self.surface, 'Start Game', pygame.Rect(5, 5, 170, 30), self.controller.start_battle)],
            BattlePhase.TURN_START: [],
            BattlePhase.PLANNING_PHASE: [
                Button(self.surface, 'Move', pygame.Rect(5, 5, 170, 30), None),
                Button(self.surface, 'Attack', pygame.Rect(5, 40, 170, 30), None),
                Button(self.surface, 'Execute', pygame.Rect(5, 75, 170, 30), None)
            ]
        }
        for button_list in self.buttons.values():
            for button in button_list:
                self.add_widget(button)

    def on_change_round_state(self, battle_phase: BattlePhase) -> None:
        for button in self.widgets: 
            button.enabled = False

        for button in self.buttons[battle_phase]:
            button.enabled = True


class BattleViewCanvas(Panel):

    def __init__(self, ui_context: UIContext, hex_map_view: HexMapView, area: pygame.Rect, background: pygame.Color, frame_color: pygame.Color):
        super().__init__(ui_context.screen, area, background, frame_color)
        self.controller = ui_context.controller
        self.state = ui_context.state
        self.hex_map_view = hex_map_view
        self.hex_map_view.set_hex_map_area(self.area)

    def set_hex_map(self, hex_map: HexMap) -> None:
        self.hex_map_view.set_hex_map(hex_map)

    def handle_event(self, event) -> None:
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button not in (4, 5)):
            if not self.area.collidepoint(event.pos):
                return
            coordinate = self.hex_map_view.screen_point_to_hex(VecF2(*event.pos))
            self.controller.handle_click(coordinate)
        
    def draw(self) -> None:
        self.hex_map_view.draw()
        self.screen.set_clip(self.area)
        self.screen.set_clip(None) 


class BattleController:

    def __init__(self, screen: pygame.Surface, grid_area: pygame.Rect, state: BattleManager):
        self.battle_view_state = BattleViewState()
        ui_context = UIContext(self, self.battle_view_state, screen)
        battle_context = UIContext(self, state, screen)
        self.screen = screen
        self.grid_area = grid_area
        self.state = state
        self.selected_cell = None
        self.layout = HexLayout(POINTY, pygame.Vector2(20, 20))
        self.camera = HexCamera()
        self.hex_map_view = HexMapView(self.screen, self.layout, self.camera)
        self.state.battle_map.bind(self.hex_map_view.set_hex_map)
        self.state.battle_map.bind(self.battle_view_state.set_hex_map)
        self.hex_map_view.set_hex_map(self.state.battle_map.get())
        self.battle_view_state.set_hex_map(self.state.battle_map.get())

        self.game_info_panel = GameInformationPanel(battle_context, pygame.Rect(0, 40, 150, 695), pygame.Color(30, 30, 30), pygame.Color(225, 225, 225))
        self.cell_info_panel = CellInformationPanel(ui_context, pygame.Rect(1260, 40, 180, 500), pygame.Color(30, 30, 30), pygame.Color(225, 225, 225))
        self.action_panel = ActionPanel(battle_context, pygame.Rect(1260, 540, 180, 195), pygame.Color(30, 30, 30), pygame.Color(100, 225, 225))

        self.turn_start_transition = TurnStartTransition(self.screen, self)
        self.grid_view = BattleViewCanvas(battle_context, self.hex_map_view, pygame.Rect(150, 40, 1110, 695), pygame.Color(30, 30, 30), pygame.Color('blue'))

    def handle_click(self, coordinate: HexCoordinate) -> None:
        self.battle_view_state.hovered_cell.set(coordinate)
            
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
        self.cell_info_panel.draw()
        self.action_panel.draw()
        self.grid_view.draw()
