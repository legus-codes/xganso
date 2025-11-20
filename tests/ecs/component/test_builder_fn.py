import pytest
from pydantic import ValidationError
from ecs_architecture.component.stats import HP, Attack, Defense, build_attack, build_defense, build_hp


def test_build_attack():
    base = 10.4
    growth = 3.5
    attack = build_attack(base=base, growth=growth)
    assert isinstance(attack, Attack)
    assert attack.base == base
    assert attack.growth == growth

def test_build_attack_negative_base():
    base = -10.4
    growth = 3.5
    with pytest.raises(ValidationError):
        build_attack(base=base, growth=growth)

def test_build_attack_negative_growth():
    base = 10.4
    growth = -3.5
    with pytest.raises(ValidationError):
        build_attack(base=base, growth=growth)

def test_build_defense():
    base = 10.4
    growth = 3.5
    defense = build_defense(base=base, growth=growth)
    assert isinstance(defense, Defense)
    assert defense.base == base
    assert defense.growth == growth

def test_build_defense_negative_base():
    base = -10.4
    growth = 3.5
    with pytest.raises(ValidationError):
        build_defense(base=base, growth=growth)

def test_build_defense_negative_growth():
    base = 10.4
    growth = -3.5
    with pytest.raises(ValidationError):
        build_defense(base=base, growth=growth)

def test_build_hp():
    base = 10.4
    growth = 3.5
    regen = 6.4
    hp = build_hp(base=base, growth=growth, regen=regen)
    assert isinstance(hp, HP)
    assert hp.current == base
    assert hp.max_value == base
    assert hp.growth == growth
    assert hp.regeneration == regen

def test_build_hp_negative_base():
    base = -10.4
    growth = 3.5
    regen = 6.4
    with pytest.raises(ValidationError):
        build_hp(base=base, growth=growth, regen=regen)

def test_build_hp_negative_growth():
    base = 10.4
    growth = -3.5
    regen = 6.4
    with pytest.raises(ValidationError):
        build_hp(base=base, growth=growth, regen=regen)

def test_build_hp_negative_regen():
    base = 10.4
    growth = 3.5
    regen = -6.4
    with pytest.raises(ValidationError):
        build_hp(base=base, growth=growth, regen=regen)
