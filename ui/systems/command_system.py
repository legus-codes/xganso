from omniecs.system import System

from ui.components.command import SetBackgroundColorCommand, SetFrameColorCommand
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame


class SetFrameColorSystem(System):

    def on_register(self):
        self.world.register_temporary_component(SetFrameColorCommand)

    def execute(self, _: float) -> None:
        for (entity_id, (frame, command)) in self.world.query(Frame, SetFrameColorCommand):
            frame.color = command.color
            self.world.add_component(entity_id, Dirty())


class SetBackgroundColorSystem(System):

    def on_register(self):
        self.world.register_temporary_component(SetBackgroundColorCommand)

    def execute(self, _: float) -> None:
        for (entity_id, (background, command)) in self.world.query(Background, SetBackgroundColorCommand):
            background.color = command.color
            self.world.add_component(entity_id, Dirty())
