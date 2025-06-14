import unittest
from unittest.mock import MagicMock

from ecs import ECS, SystemProtocol


class TestECS(unittest.TestCase):

    # World    
    def test_world_starts_empty(self):
        ecs = ECS()
        self.assertEqual(0, len(ecs.entities))
        self.assertEqual(0, len(ecs.world))
        self.assertEqual(0, len(ecs.systems))

    def test_world_is_empty_after_reset(self):
        ecs = ECS()
        entity_id = ecs.create_entity()
        ecs.add_component(entity_id, 'a')
        ecs.add_system(1)

        ecs.reset()

        self.assertEqual(0, len(ecs.entities))
        self.assertEqual(0, len(ecs.world))
        self.assertEqual(0, len(ecs.systems))

    # Entity
    def test_create_entity_returns_unique_id(self):
        ecs = ECS()
        entity_ids = set()
        population_size = 1000
        for _ in range(population_size):
            entity_ids.add(ecs.create_entity())

        self.assertEqual(population_size, len(entity_ids))

    def test_delete_non_existing_entity_does_not_change_data(self):
        ecs = ECS()
        entity_id = ecs.create_entity()
        ecs.add_component(entity_id, 'a')

        ecs.delete_entity(entity_id+1)

        self.assertTrue(ecs.has_entity(entity_id))
        for component in ecs.world.keys():
            self.assertTrue(ecs.entity_has_component(entity_id, component))

    def test_delete_entity_wipes_out_all_data(self):
        ecs = ECS()
        entity_id = ecs.create_entity()
        ecs.add_component(entity_id, 'a')

        ecs.delete_entity(entity_id)

        self.assertFalse(ecs.has_entity(entity_id))
        for component in ecs.world.keys():
            self.assertFalse(ecs.entity_has_component(entity_id, component))

    # Component
    def test_add_entity_component(self):
        ecs = ECS()
        component = 'a'
        component_type = type(component)
        entity_id = ecs.create_entity()

        ecs.add_component(entity_id, component)

        self.assertTrue(ecs.has_component(component_type))
        self.assertTrue(ecs.entity_has_component(entity_id, component_type))

    def test_add_component_to_non_existing_entity(self):
        ecs = ECS()
        component = 'a'
        component_type = type(component)
        entity_id = 0

        ecs.add_component(entity_id, component)

        self.assertFalse(ecs.has_component(component_type))

    def test_add_multiple_entity_components(self):
        ecs = ECS()
        components = ['a', 3, 5.2]
        entity_id = ecs.create_entity()

        for component in components:
            ecs.add_component(entity_id, component)

        for component in components:
            component_type = type(component)
            self.assertTrue(ecs.has_component(component_type))
            self.assertTrue(ecs.entity_has_component(entity_id, component_type))

    def test_override_entity_component(self):
        ecs = ECS()
        component = 'a'
        overwrite_component = 'g'
        component_type = type(component)
        entity_id = ecs.create_entity()

        ecs.add_component(entity_id, component)
        ecs.add_component(entity_id, overwrite_component)

        self.assertEqual(1, len(ecs.world[component_type]))
        self.assertEqual(overwrite_component, ecs.get_entity_component(entity_id, component_type))

    def test_remove_entity_component(self):
        ecs = ECS()
        component = 'a'
        component_type = type(component)
        entity_id = ecs.create_entity()

        ecs.add_component(entity_id, component)
        ecs.remove_component(entity_id, component_type)

        self.assertTrue(ecs.has_component(component_type))
        self.assertFalse(ecs.entity_has_component(entity_id, component_type))
        self.assertTrue(ecs.has_entity(entity_id))
    
    def test_remove_component_from_non_existing_entity(self):
        ecs = ECS()
        component = 'a'
        component_type = type(component)
        entity_id = ecs.create_entity()

        ecs.add_component(entity_id, component)
        ecs.remove_component(entity_id+1, component_type)

        self.assertTrue(ecs.has_component(component_type))
        self.assertTrue(ecs.entity_has_component(entity_id, component_type))
    
    def test_remove_non_existing_entity_component(self):
        ecs = ECS()
        component = 'a'
        component_type = type(component)
        entity_id = ecs.create_entity()

        ecs.remove_component(entity_id, component_type)

        self.assertFalse(ecs.has_component(component_type))

    def test_get_entity_component(self):
        ecs = ECS()
        component = 'a'
        component_type = type(component)
        entity_id = ecs.create_entity()

        ecs.add_component(entity_id, component)

        obtained_component = ecs.get_entity_component(entity_id, component_type)

        self.assertEqual(obtained_component, component)

    def test_get_component_from_non_existing_entity(self):
        ecs = ECS()
        component = 'a'
        component_type = type(component)
        entity_id = ecs.create_entity()

        ecs.add_component(entity_id, component)

        obtained_component = ecs.get_entity_component(entity_id+1, component_type)

        self.assertIsNone(obtained_component)

    def test_get_non_existing_entity_component(self):
        ecs = ECS()
        component = 'a'
        component_type = type(component)
        entity_id = ecs.create_entity()

        obtained_component = ecs.get_entity_component(entity_id, component_type)

        self.assertIsNone(obtained_component)

    # System
    def test_add_system(self):
        ecs = ECS()
        ecs.add_system('a')

        self.assertTrue(ecs.has_system('a'))

    def test_add_multiple_systems(self):
        ecs = ECS()
        population_size = 1000
        for i in range(population_size):
            ecs.add_system(i)

        self.assertEqual(population_size, len(ecs.systems))

    def test_execute_systems(self):
        ecs = ECS()
        systems = [MagicMock(SystemProtocol), MagicMock(SystemProtocol), MagicMock(SystemProtocol)]
        for system in systems:
            ecs.add_system(system)

        ecs.execute()

        for system in systems:
            system.execute.assert_called_once()
        
    def test_not_execute_systems(self):
        ecs = ECS()
        systems = [MagicMock(SystemProtocol), MagicMock(SystemProtocol), MagicMock(SystemProtocol)]
        for system in systems:
            ecs.add_system(system)

        for system in systems:
            system.execute.assert_not_called()
    
    def test_get_eligible_entities_from_one_component(self):
        ecs = ECS()
        entity_id1 = ecs.create_entity()
        entity_id2 = ecs.create_entity()
        entity_id3 = ecs.create_entity()
        ecs.add_component(entity_id1, 'a')
        ecs.add_component(entity_id2, 3)
        ecs.add_component(entity_id3, 'c')

        eligible_entities = ecs.get_entities_with(type('a'))

        self.assertListEqual([entity_id1, entity_id3], eligible_entities)

    def test_get_eligible_entities_from_multiple_components(self):
        ecs = ECS()
        entity_id1 = ecs.create_entity()
        entity_id2 = ecs.create_entity()
        entity_id3 = ecs.create_entity()
        ecs.add_component(entity_id1, 'a')
        ecs.add_component(entity_id1, 2)
        ecs.add_component(entity_id1, 0.5)
        ecs.add_component(entity_id2, 3)
        ecs.add_component(entity_id2, 0.4)
        ecs.add_component(entity_id3, 'c')
        ecs.add_component(entity_id3, 0.1)

        eligible_entities = ecs.get_entities_with(type('a'), type(3), type(4.3))

        self.assertListEqual([entity_id1], eligible_entities)

    def test_get_eligible_entities_from_non_existing_component(self):
        ecs = ECS()
        entity_id1 = ecs.create_entity()
        entity_id2 = ecs.create_entity()
        entity_id3 = ecs.create_entity()
        ecs.add_component(entity_id1, 'a')
        ecs.add_component(entity_id1, 2)
        ecs.add_component(entity_id2, 3)
        ecs.add_component(entity_id3, 'c')

        eligible_entities = ecs.get_entities_with(type('a'), type(3), type(4.3))

        self.assertListEqual([], eligible_entities)

    def test_get_eligible_entities_from_empty_set_of_components(self):
        ecs = ECS()
        entity_id1 = ecs.create_entity()
        entity_id2 = ecs.create_entity()
        entity_id3 = ecs.create_entity()
        ecs.add_component(entity_id1, 'a')
        ecs.add_component(entity_id1, 2)
        ecs.add_component(entity_id2, 3)
        ecs.add_component(entity_id3, 'c')

        eligible_entities = ecs.get_entities_with()

        self.assertListEqual([], eligible_entities)
        
    # Debug
    def test_get_all_entity_components(self):
        ecs = ECS()
        entity_id = ecs.create_entity()
        ecs.add_component(entity_id, 'a')
        ecs.add_component(entity_id, 7)
        ecs.add_component(entity_id, 3.4)

        components = ecs.get_all_entity_components(entity_id)

        self.assertListEqual(['a', 7, 3.4], components)

    def test_get_all_entity_components_with_missing_components(self):
        ecs = ECS()
        entity_id = ecs.create_entity()
        second_id = ecs.create_entity()
        ecs.add_component(entity_id, 'a')
        ecs.add_component(entity_id, 7)
        ecs.add_component(second_id, 3.4)

        components = ecs.get_all_entity_components(entity_id)

        self.assertListEqual(['a', 7, None], components)

    def test_get_all_entity_components_of_non_existing_entity(self):
        ecs = ECS()
        entity_id = ecs.create_entity()
        ecs.add_component(entity_id, 'a')
        ecs.add_component(entity_id, 7)
        ecs.add_component(entity_id, 3.4)

        components = ecs.get_all_entity_components(entity_id+1)

        self.assertIsNone(components)


if __name__ == '__main__':
    unittest.main()
