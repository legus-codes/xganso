from core.primitives import Rect
from ecs_framework.system import System
from ecs_framework.types import EntityId
from ui.components.behavior import Enabled, Hoverable, Hovered
from ui.components.layout import RenderLayer, WorldTransform
from ui.resources.state import PointerState


class PointerHitTestSystem(System):

    def execute(self, _: float) -> None:
        pointer = self.world.get_resource(PointerState)

        elements: list[tuple[EntityId, tuple[WorldTransform, RenderLayer]]] = list(self.world.query(WorldTransform, RenderLayer, all_of=(Enabled, Hoverable)))
        elements.sort(key=lambda x: x[1][1].layer, reverse=True)

        new_hovered = None
        for entity_id, (transform, _) in elements:
            rect = Rect.from_transform(transform.position, transform.size)
            if rect.contains(pointer.position):
                new_hovered = entity_id
                break

        if new_hovered != pointer.hovered_entity:
            if pointer.hovered_entity is not None:
                self.world.remove_component(pointer.hovered_entity, Hovered)
            if new_hovered is not None:
                self.world.add_component(new_hovered, Hovered())
            pointer.hovered_entity = new_hovered
            self.world.set_resource(pointer)
