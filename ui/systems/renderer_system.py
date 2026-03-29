from adapters.render.commands import DrawFrame, DrawRectangle
from core.primitives import Color, IVec2
from omniecs.system import System

from ui.components.behavior import Enabled
from ui.components.layout import RenderLayer, Transform
from ui.components.rendering import Dirty
from ui.components.style import Background


class BackgroundRendererSystem(System):

    def execute(self, _: float) -> None:
        for (entity_id, (background, transform, layer)) in self.world.query(Background, Transform, RenderLayer, all_of=(Enabled, Dirty)):
            command = DrawRectangle(layer.layer, transform.position, transform.size, background.color.normal)
            self.world.add_draw_command(command)
            self.world.remove_component(entity_id, Dirty)


def create_draw_rectangle() -> DrawRectangle:
    return DrawRectangle(position=IVec2(), size=IVec2(), color=Color(255, 0, 0), frame_color=(0, 0, 255), frame_width=2, layer=0)

def create_draw_frame() -> DrawFrame:
    return DrawFrame(position=IVec2(), size=IVec2(), color=Color(0, 0, 255), width=2, layer=1)
