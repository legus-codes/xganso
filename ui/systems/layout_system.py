from omniecs.system import System
from omniecs.types import EntityId

from core.primitives import IVec2, Vec2
from ui.components.layout import Children, FixedItemSize, HorizontalLayout, Parent, Transform, WorldTransform
from ui.components.rendering import Dirty


#TODO test
class LayoutHierarchySystem(System):

    def execute(self, _: float) -> None:
        for entity_id, (parent,) in self.world.query(Parent, all_of=(Dirty,)):
            parent_id = parent.entity

            if not self.world.exists(parent_id):
                continue

            parent_children: Children = self.world.get_component(parent_id, Children) or Children()
            parent_children.entities.add(entity_id)
            self.world.add_component(parent_id, parent_children)
            self.world.add_component(parent_id, Dirty())

        for entity_id, (children,) in self.world.query(Children):
            children_to_remove = set()
            for child_id in children.entities:
                if not self.world.exists(child_id):
                    children_to_remove.add(child_id)
                    continue

                child_parent: Parent = self.world.get_component(child_id, Parent)
                if child_parent.entity != entity_id:
                    children_to_remove.add(child_id)
                    self.world.add_component(child_id, Dirty())

            if children_to_remove:
                children.entities.difference_update(children_to_remove)
                self.world.add_component(entity_id, children)
                self.world.add_component(entity_id, Dirty())


class HorizontalLayoutSystem(System):

    def execute(self, _: float) -> None:
        for entity_id, (children, transform, horizontal_layout) in self.world.query(Children, Transform, HorizontalLayout, none_of=(Parent,)):
            area_size = transform.size
            number_of_children = len(children.entities)
            total_spacing = horizontal_layout.spacing * (number_of_children - 1)
            total_padding: IVec2 = horizontal_layout.padding * 2

            fixed_item_size: FixedItemSize = self.world.get_component(entity_id, FixedItemSize)
            if fixed_item_size is not None:
                item_width = fixed_item_size.width
                item_height = fixed_item_size.height
            else:
                item_width = (area_size.x - total_spacing - total_padding.x) / number_of_children
                item_height = area_size.y - total_padding.y

            item_y_position = (area_size.y - item_height) / 2
            for index, child_entity in enumerate(children.entities):
                child_transform: Transform = self.world.get_component(child_entity, Transform)
                child_transform.position = Vec2((item_width + horizontal_layout.spacing) * index + horizontal_layout.padding.x, item_y_position)
                child_transform.size = Vec2(item_width, item_height)


#TODO test
class WorldTransformationSystem(System):

    def execute(self, _: float) -> None:
        for entity_id, (transform,) in self.world.query(Transform, none_of=(Parent,)):
            world_transform = WorldTransform(transform.position, transform.size)
            self.world.add_component(entity_id, world_transform)

            self._process_node_children(entity_id, world_transform)

    def _process_node_children(self, node_id: EntityId, node_world_transform: WorldTransform) -> None:
        node_children = self.world.get_component(node_id, Children)

        if node_children is None:
            return

        for child_id in node_children.entities:
            if self.world.get_component(child_id, Dirty) is None and self.world.get_component(child_id, WorldTransform) is not None:
                continue
            
            child_transform: Transform = self.world.get_component(child_id, Transform)
            if child_transform is None:
                continue

            child_world_transform = WorldTransform(child_transform.position + node_world_transform.position, child_transform.size)
            self.world.add_component(child_id, child_world_transform)

            self._process_node_children(child_id, child_world_transform)
