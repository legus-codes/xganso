from adapters.render.commands import DrawFrame, DrawInput, DrawRectangle, DrawText
from core.primitives import Color, IVec2
from omniecs.system import System
from omniecs.types import EntityId

from ui.components.behavior import Enabled, Focused, Hovered, Pressed, Selected, Toggled
from ui.components.content import InputValue, Text
from ui.components.layout import RenderLayer, Spacing, TextAlignment, WorldTransform
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame, TextStyle
from ui.types import InteractionColors


class BaseRendererSystem(System):
    
    def on_register(self):
        self.world.register_temporary_component(Dirty)


#TODO test
class BackgroundRendererSystem(BaseRendererSystem):

    def execute(self, _: float) -> None:
        for (entity_id, (background, world_transform, layer)) in self.world.query(Background, WorldTransform, RenderLayer, all_of=(Enabled, Dirty)):
            command = DrawRectangle(global_layer=layer.layer, local_layer=0, position=world_transform.position, size=world_transform.size, color=self._get_color(entity_id, background.color))
            self.world.add_draw_command(command)

    def _get_color(self, entity_id: EntityId, colors: InteractionColors) -> Color:
        if self.world.get_component(entity_id, Pressed):
            return colors.pressed
        if self.world.get_component(entity_id, Selected) or self.world.get_component(entity_id, Toggled):
            return colors.selected
        return colors.normal


#TODO test
class FrameRendererSystem(BaseRendererSystem):

    def execute(self, _: float) -> None:
        for (entity_id, (frame, world_transform, layer)) in self.world.query(Frame, WorldTransform, RenderLayer, all_of=(Enabled, Dirty)):
            command = DrawFrame(global_layer=layer.layer, local_layer=1, position=world_transform.position, size=world_transform.size, color=self._get_color(entity_id, frame.color), width=frame.width)
            self.world.add_draw_command(command)

    def _get_color(self, entity_id: EntityId, colors: InteractionColors) -> Color:
        if self.world.get_component(entity_id, Focused):
            return colors.focused
        if self.world.get_component(entity_id, Hovered):
            return colors.hovered
        if self.world.get_component(entity_id, Selected) or self.world.get_component(entity_id, Toggled):
            return colors.selected
        return colors.normal


#TODO test
class TextRendererSystem(BaseRendererSystem):

    def execute(self, _: float) -> None:
        for (entity_id, (text, text_style, text_alignment, spacing, world_transform, layer)) in self.world.query(Text, TextStyle, TextAlignment, Spacing, WorldTransform, RenderLayer, all_of=(Enabled, Dirty)):
            input_value = self.world.get_component(entity_id, InputValue)

            if input_value:
                focused = True if self.world.get_component(entity_id, Focused) else False
                command = DrawInput(global_layer=layer.layer, local_layer=2, position=world_transform.position, size=world_transform.size, color=text_style.color.normal, 
                                    text=text.text, font_id=text_style.font, font_size=text_style.size, horizontal_alignment=text_alignment.horizontal,
                                    vertical_alignment=text_alignment.vertical, spacing=IVec2(spacing.horizontal, spacing.vertical), value=input_value.value, focused=focused)
            else:
                command = DrawText(global_layer=layer.layer, local_layer=2, position=world_transform.position, size=world_transform.size, color=text_style.color.normal,
                                   text=text.text, font_id=text_style.font, font_size=text_style.size, horizontal_alignment=text_alignment.horizontal,
                                   vertical_alignment=text_alignment.vertical, spacing=IVec2(spacing.horizontal, spacing.vertical))
            self.world.add_draw_command(command)
