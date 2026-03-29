from adapters.render.commands import DrawFrame, DrawRectangle
from core.primitives import Color, IVec2
from omniecs.system import System

from ui.components.behavior import Enabled
from ui.components.layout import RenderLayer, Transform
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame


class BaseRendererSystem(System):
    
    def on_register(self):
        self.world.register_temporary_component(Dirty)


class BackgroundRendererSystem(BaseRendererSystem):

    def execute(self, _: float) -> None:
        for (_, (background, transform, layer)) in self.world.query(Background, Transform, RenderLayer, all_of=(Enabled, Dirty)):
            command = DrawRectangle(global_layer=layer.layer, local_layer=0, position=transform.position, size=transform.size, color=background.color.normal)
            self.world.add_draw_command(command)


class FrameRendererSystem(BaseRendererSystem):

    def execute(self, _: float) -> None:
        for (_, (frame, transform, layer)) in self.world.query(Frame, Transform, RenderLayer, all_of=(Enabled, Dirty)):
            command = DrawFrame(global_layer=layer.layer, local_layer=1, position=transform.position, size=transform.size, color=frame.color.normal, width=frame.width)
            self.world.add_draw_command(command)


def create_draw_rectangle() -> DrawRectangle:
    return DrawRectangle(position=IVec2(), size=IVec2(), color=Color(255, 0, 0), frame_color=(0, 0, 255), frame_width=2, layer=0)

def create_draw_frame() -> DrawFrame:
    return DrawFrame(position=IVec2(), size=IVec2(), color=Color(0, 0, 255), width=2, layer=1)
