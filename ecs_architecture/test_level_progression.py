import unittest

from ecs_architecture.component.stats import HP, Attack, Defense
from ecs_architecture.level_progression import XP, GainXP, IncreaseLevel, Level, LevelUp, XPGained
from ecs_framework.ecs import ECS


class TestECS(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.world = ECS()
        self.unit = None

    def setUp(self):
        self.unit = self.world.create_entity()
        self.world.add_component(self.unit, XP(0, 50, 0, 1.2))
        self.world.add_component(self.unit, Level(1))
        self.world.add_component(self.unit, Attack(5, 4))
        self.world.add_component(self.unit, Defense(10, 3))
        self.world.add_component(self.unit, HP(20, 20, 2, 5))
        self.world.add_system(GainXP(self.world))
        self.world.add_system(IncreaseLevel(self.world))

    def tearDown(self):
        self.world.reset()

    def _check_xp(self, entity: int, current: int, needed: int, total: int, growth: float) -> None:
        xp: XP = self.world.get_entity_component(entity, XP)
        self.assertEqual(xp.current, current)
        self.assertEqual(xp.needed, needed)
        self.assertEqual(xp.total, total)
        self.assertEqual(xp.growth, growth)

    def _check_level(self, entity: int, current: int) -> None:
        level: Level = self.world.get_entity_component(entity, Level)
        self.assertEqual(level.current, current)

    def _check_attack(self, entity: int, base: int, growth: int) -> None:
        attack: Attack = self.world.get_entity_component(entity, Attack)
        self.assertEqual(attack.base, base)
        self.assertEqual(attack.growth, growth)

    def _check_defense(self, entity: int, base: int, growth: int) -> None:
        defense: Defense = self.world.get_entity_component(entity, Defense)
        self.assertEqual(defense.base, base)
        self.assertEqual(defense.growth, growth)

    def _check_hp(self, entity: int, current: int, max_value: int, regeneration: int, growth: int) -> None:
        hp: HP = self.world.get_entity_component(entity, HP)
        self.assertEqual(hp.current, current)
        self.assertEqual(hp.max_value, max_value)
        self.assertEqual(hp.regeneration, regeneration)
        self.assertEqual(hp.growth, growth)

    def test_unit_gains_no_xp(self):
        self.world.add_component(self.unit, XPGained(0))
        
        self.world.execute(1.0)

        self._check_xp(self.unit, 0, 50, 0, 1.2)
        self._check_level(self.unit, 1)
        self._check_attack(self.unit, 5, 4)
        self._check_defense(self.unit, 10, 3)
        self._check_hp(self.unit, 20, 20, 2, 5)
        self.assertIsNone(self.world.get_entity_component(self.unit, XPGained))
        self.assertIsNone(self.world.get_entity_component(self.unit, LevelUp))

    def test_unit_gains_xp_but_does_not_increase_level(self):
        self.world.add_component(self.unit, XPGained(10))
        
        self.world.execute(1.0)

        self._check_xp(self.unit, 10, 50, 10, 1.2)
        self._check_level(self.unit, 1)
        self._check_attack(self.unit, 5, 4)
        self._check_defense(self.unit, 10, 3)
        self._check_hp(self.unit, 20, 20, 2, 5)
        self.assertIsNone(self.world.get_entity_component(self.unit, XPGained))
        self.assertIsNone(self.world.get_entity_component(self.unit, LevelUp))

    def test_unit_gains_xp_and_increases_one_level(self):
        self.world.add_component(self.unit, XPGained(60))
        
        self.world.execute(1.0)

        self._check_xp(self.unit, 10, 60, 60, 1.2)
        self._check_level(self.unit, 2)
        self._check_attack(self.unit, 9, 4)
        self._check_defense(self.unit, 13, 3)
        self._check_hp(self.unit, 25, 25, 2, 5)
        self.assertIsNone(self.world.get_entity_component(self.unit, XPGained))
        self.assertIsNone(self.world.get_entity_component(self.unit, LevelUp))

    def test_unit_gains_xp_and_increases_multiple_levels(self):
        self.world.add_component(self.unit, XPGained(268))
        
        self.world.execute(1.0)

        self._check_xp(self.unit, 0, 103, 268, 1.2)
        self._check_level(self.unit, 5)
        self._check_attack(self.unit, 21, 4)
        self._check_defense(self.unit, 22, 3)
        self._check_hp(self.unit, 40, 40, 2, 5)
        self.assertIsNone(self.world.get_entity_component(self.unit, XPGained))
        self.assertIsNone(self.world.get_entity_component(self.unit, LevelUp))

    def test_unit_gains_xp_multiple_times(self):
        self.world.add_component(self.unit, XPGained(10))
        self.world.execute(1.0)
        self.world.add_component(self.unit, XPGained(40))
        self.world.execute(1.0)

        self._check_xp(self.unit, 0, 60, 50, 1.2)
        self._check_level(self.unit, 2)
        self._check_attack(self.unit, 9, 4)
        self._check_defense(self.unit, 13, 3)
        self._check_hp(self.unit, 25, 25, 2, 5)
        self.assertIsNone(self.world.get_entity_component(self.unit, XPGained))
        self.assertIsNone(self.world.get_entity_component(self.unit, LevelUp))

    def test_unit_heals_when_leveling_up(self):
        self.world.add_component(self.unit, HP(2, 20, 2, 5))
        self.world.add_component(self.unit, XPGained(50))
        self._check_hp(self.unit, 2, 20, 2, 5)

        self.world.execute(1.0)

        self._check_xp(self.unit, 0, 60, 50, 1.2)
        self._check_level(self.unit, 2)
        self._check_attack(self.unit, 9, 4)
        self._check_defense(self.unit, 13, 3)
        self._check_hp(self.unit, 25, 25, 2, 5)
        self.assertIsNone(self.world.get_entity_component(self.unit, XPGained))
        self.assertIsNone(self.world.get_entity_component(self.unit, LevelUp))


if __name__ == '__main__':
    unittest.main()
