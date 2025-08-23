from pygame import Surface, Rect
from ecs_framework.ecs import ECS
from editor.map_editor_creator import CreateMapCommand, MapCreater, MapType
from editor.map_editor_io import LoadMapCommand, MapLoader, MapSaver, SaveMapCommand
from editor.map_editor_feedback import FeedbackBroadcastSystem, FeedbackDisplayer
from editor.map_editor_viewer import Map, MapDisplaySource, MapRendererSystem
from ui.ecs_elements import create_button, create_int_text_input, create_panel, create_radio_button, create_text, create_text_input, create_toggle
from ui.ui_components import UIForceRedraw, UIVariable
from ui.ui_event_system import UIEventConverterSystem, UIKeyDownSystem, UIMouseClickedSystem, UIMousePositionSystem, UIMousePressedSystem, UIMouseReleasedSystem
from ui.ui_renderer_system import UIRelativeToRect, UIRendererSystem


class MapEditorController:

    def __init__(self, world: ECS, screen: Surface, mouse: int, keyboard: int):
        self.world = world
        self.screen = screen
        self.mouse = mouse
        self.keyboard = keyboard

        self.editor = self.create_editor()

        self.create_top_bar()
        self.create_side_bar()
        self.create_map_view()
        self.create_bottom_bar()

        self.initialize_systems()

    def create_editor(self) -> int:
        editor = self.world.create_entity()
        self.world.add_component(editor, Map(None))
        return editor

    def create_top_bar(self) -> None:
        top_bar_panel = create_panel(self.world, Rect(0, 0, 1440, 50), 'red')
        filename_text_input = create_text_input(self.world, 'Filename: ', 'hex.json', Rect(2, 25, 500, 20), top_bar_panel)
        save_button = create_button(self.world, 'Save', Rect(10, 2, 100, 20), lambda: self.save_map(filename_text_input), top_bar_panel)
        load_button = create_button(self.world, 'Load', Rect(150, 2, 100, 20), lambda: self.load_map(filename_text_input), top_bar_panel)

        radius_int_input = create_int_text_input(self.world, 'Radius: ', '5', Rect(800, 25, 350, 20), top_bar_panel)
        empty_map_button = create_button(self.world, 'Empty Map', Rect(600, 2, 150, 20), lambda: self.create_map(MapType.Empty, radius_int_input), top_bar_panel)
        hexagon_map_button = create_button(self.world, 'Hexagon Map', Rect(800, 2, 150, 20), lambda: self.create_map(MapType.Hexagon, radius_int_input), top_bar_panel)
        random_map_button = create_button(self.world, 'Random Map', Rect(1000, 2, 150, 20), lambda: self.create_map(MapType.Random, radius_int_input), top_bar_panel)

    def create_side_bar(self) -> None:
        side_bar_panel = create_panel(self.world, Rect(0, 50, 150, 700), 'blue')
        paint_tile_radio = create_radio_button(self.world, 'Paint Tile', 'edit_tools', Rect(5, 10, 140, 20), side_bar_panel)
        erase_tile_radio = create_radio_button(self.world, 'Erase Tile', 'edit_tools', Rect(5, 40, 140, 20), side_bar_panel)
        add_spawn_radio = create_radio_button(self.world, 'Add Spawn', 'edit_tools', Rect(5, 70, 140, 20), side_bar_panel)
        remove_span_radio = create_radio_button(self.world, 'Remove Spawn', 'edit_tools', Rect(5, 100, 140, 20), side_bar_panel)

        tile_picker = create_text(self.world, 'Grass', Rect(5, 130, 140, 20), side_bar_panel)
        spawn_picker = create_text(self.world, 'Team Green', Rect(5, 160, 140, 20), side_bar_panel)

        path_toggle = create_toggle(self.world, 'Path', Rect(5, 200, 140, 20), side_bar_panel)
        move_toggle = create_toggle(self.world, 'Move', Rect(5, 230, 140, 20), side_bar_panel)
        range_toggle = create_toggle(self.world, 'Range', Rect(5, 260, 140, 20), side_bar_panel)
        ring_toggle = create_toggle(self.world, 'Ring', Rect(5, 290, 140, 20), side_bar_panel)

        move_power_int_input = create_int_text_input(self.world, 'Move Power: ', '3', Rect(5, 320, 140, 20), side_bar_panel)
        distance_int_input = create_int_text_input(self.world, 'Distance: ', '3', Rect(5, 350, 140, 20), side_bar_panel)

    def create_map_view(self) -> None:
        map_view_panel = create_panel(self.world, Rect(150, 50, 1290, 700), 'yellow')
        self.world.add_component(map_view_panel, MapDisplaySource(self.editor))
        self.world.add_component(map_view_panel, UIForceRedraw())

    def create_bottom_bar(self) -> None:
        bottom_bar_panel = create_panel(self.world, Rect(0, 750, 1440, 25), 'green')
        notification_text = create_text(self.world, 'Welcome to xganso MapEditor', Rect(5, 2, 1430, 20), bottom_bar_panel)
        self.world.add_component(notification_text, FeedbackDisplayer())

    def initialize_systems(self) -> None:
        self.world.add_system(UIEventConverterSystem(self.world, self.mouse, self.keyboard))
        self.world.add_system(UIMousePositionSystem(self.world, self.mouse))
        self.world.add_system(UIMouseClickedSystem(self.world, self.mouse))
        self.world.add_system(UIMousePressedSystem(self.world, self.mouse))
        self.world.add_system(UIMouseReleasedSystem(self.world, self.mouse))
        self.world.add_system(UIKeyDownSystem(self.world, self.keyboard))

        self.world.add_system(MapCreater(self.world))
        self.world.add_system(MapLoader(self.world))
        self.world.add_system(MapSaver(self.world))
        self.world.add_system(FeedbackBroadcastSystem(self.world))

        self.world.add_system(UIRelativeToRect(self.world))
        self.world.add_system(UIRendererSystem(self.world, self.screen))
        self.world.add_system(MapRendererSystem(self.world, self.screen))

    def load_map(self, filename_entity: int):
        filename = self.world.get_entity_component(filename_entity, UIVariable)
        command = LoadMapCommand(filename.value)
        self.world.add_component(self.editor, command)

    def save_map(self, filename_entity: int):
        filename = self.world.get_entity_component(filename_entity, UIVariable)
        command = SaveMapCommand(filename.value)
        self.world.add_component(self.editor, command)

    def create_map(self, map_type: MapType, radius_entity: int):
        radius = self.world.get_entity_component(radius_entity, UIVariable)
        command = CreateMapCommand(map_type, int(radius.value))
        self.world.add_component(self.editor, command)
