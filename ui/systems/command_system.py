from omniecs.system import System

from ui.components.command import UnsetBackgroundColorCommand, UnsetFrameColorCommand, UnsetTextColorCommand, SetBackgroundColorCommand, SetFrameColorCommand, SetTextColorCommand
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame, TextStyle


class SetFrameColorSystem(System):

    def on_register(self):
        self.world.register_temporary_component(SetFrameColorCommand)
        self.world.register_temporary_component(UnsetFrameColorCommand)

    def execute(self, _: float) -> None:
        for (entity_id, (frame, command)) in self.world.query(Frame, SetFrameColorCommand):
            frame.colors.add(command.color)
            self.world.add_component(entity_id, Dirty())

        for (entity_id, (frame, command)) in self.world.query(Frame, UnsetFrameColorCommand):
            frame.colors.pop(command.color)
            self.world.add_component(entity_id, Dirty())


class SetBackgroundColorSystem(System):

    def on_register(self):
        self.world.register_temporary_component(SetBackgroundColorCommand)
        self.world.register_temporary_component(UnsetBackgroundColorCommand)

    def execute(self, _: float) -> None:
        for (entity_id, (background, command)) in self.world.query(Background, SetBackgroundColorCommand):
            background.colors.add(command.color)
            self.world.add_component(entity_id, Dirty())

        for (entity_id, (background, command)) in self.world.query(Background, UnsetBackgroundColorCommand):
            background.colors.pop(command.color)
            self.world.add_component(entity_id, Dirty())

class SetTextColorSystem(System):

    def on_register(self):
        self.world.register_temporary_component(SetTextColorCommand)
        self.world.register_temporary_component(UnsetTextColorCommand)

    def execute(self, _: float) -> None:
        for (entity_id, (text_style, command)) in self.world.query(TextStyle, SetTextColorCommand):
            text_style.colors.add(command.color)
            self.world.add_component(entity_id, Dirty())

        for (entity_id, (text_style, command)) in self.world.query(TextStyle, UnsetTextColorCommand):
            text_style.colors.pop(command.color)
            self.world.add_component(entity_id, Dirty())
