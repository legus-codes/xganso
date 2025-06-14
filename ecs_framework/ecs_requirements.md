ECS Requirements

The world initializes empty and it is cleared after a reset.

Each created entity has a unique id for identification. When an entity is deleted, all its data within the world is deleted. If there is no entity to delete, no changes should be done.

Within the ECS framework, one can add as many components to an entity as possible. When adding an existing component, it should overwrite the values and not create a duplicate component for the entity. One can also remove components from entities. The entity may still exist even if it has no components at the moment. If a component to be removed does not exist, no change should happen. One can also query for specific components of entities. When they do not exist, they should not crash, but return a null value.

It is allowed to add as many systems as wanted. The systems should have an execute method that is called each frame. The systems may only operate upon eligible entities according to a set of components that is not empty. In case of getting eligible entities that match an empty set of components, it should return an empty set of entities.

For debug purposes, it should be possible to query all the components of an entity. If the entity does not exist, it simply returns a null value.