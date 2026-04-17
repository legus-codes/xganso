from adapters.render.commands import DrawFrame, DrawRectangle, DrawText
from core.primitives import Color, IVec2
from omniecs.system import System

from ui.components.behavior import Enabled
from ui.components.content import Text
from ui.components.layout import RenderLayer, Spacing, TextAlignment, WorldTransform
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame, TextStyle


class BaseRendererSystem(System):
    
    def on_register(self):
        self.world.register_temporary_component(Dirty)


class BackgroundRendererSystem(BaseRendererSystem):

    def execute(self, _: float) -> None:
        for (_, (background, world_transform, layer)) in self.world.query(Background, WorldTransform, RenderLayer, all_of=(Enabled, Dirty)):
            command = DrawRectangle(global_layer=layer.layer, local_layer=0, position=world_transform.position, size=world_transform.size, color=background.color.normal)
            self.world.add_draw_command(command)


class FrameRendererSystem(BaseRendererSystem):

    def execute(self, _: float) -> None:
        for (_, (frame, world_transform, layer)) in self.world.query(Frame, WorldTransform, RenderLayer, all_of=(Enabled, Dirty)):
            command = DrawFrame(global_layer=layer.layer, local_layer=1, position=world_transform.position, size=world_transform.size, color=frame.color.normal, width=frame.width)
            self.world.add_draw_command(command)


class TextRendererSystem(BaseRendererSystem):

    def execute(self, _: float) -> None:
        for (_, (text, text_style, text_alignment, spacing, world_transform, layer)) in self.world.query(Text, TextStyle, TextAlignment, Spacing, WorldTransform, RenderLayer, all_of=(Enabled, Dirty)):
            command = DrawText(global_layer=layer.layer, local_layer=2, position=world_transform.position, size=world_transform.size, color=text_style.color.normal, 
                               text=text.text, font_id=text_style.font, font_size=text_style.size, horizontal_alignment=text_alignment.horizontal,
                               vertical_alignment=text_alignment.vertical, spacing=IVec2(spacing.horizontal, spacing.vertical))
            self.world.add_draw_command(command)

