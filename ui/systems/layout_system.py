from omniecs.system import System
from omniecs.types import EntityId

from ui.components.layout import Children, Parent, Transform, WorldTransform
from ui.components.rendering import Dirty


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
