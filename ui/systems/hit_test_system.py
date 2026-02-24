from core.primitives import Rect
from ecs_framework.system import System
from ecs_framework.types import EntityId
from ui.components.behavior import Enabled, HoverIntention, Hoverable
from ui.components.layout import RenderLayer, WorldTransform
from ui.resources.state import PointerState


class PointerHitTestSystem(System):

    def on_register(self) -> None:
        self.world.register_temporary_component(HoverIntention)

    def execute(self, _: float) -> None:
        pointer = self.world.get_resource(PointerState)

        elements: list[tuple[EntityId, tuple[WorldTransform, RenderLayer]]] = list(self.world.query(WorldTransform, RenderLayer, all_of=(Enabled, Hoverable)))
        elements.sort(key=lambda x: x[1][1].layer, reverse=True)

        for entity_id, (transform, _) in elements:
            rect = Rect.from_transform(transform.position, transform.size)
            if rect.contains(pointer.position):
                self.world.add_component(entity_id, HoverIntention())
                break
