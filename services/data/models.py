from pydantic import BaseModel


class IdentityDataDescription(BaseModel):
    id: str


class DataDescription(BaseModel):
    identity: IdentityDataDescription


class UnitIdentityDataDescription(IdentityDataDescription):
    name: str
    unit_class: str


class SpriteDataDescription(BaseModel):
    character: str
    board: str


class BaseStatDataDescription(BaseModel):
    base: float


class GrowthStatDataDescription(BaseStatDataDescription):
    growth: float


class RegenStatDataDescription(GrowthStatDataDescription):
    regen: float


class StatsDataDescription(BaseModel):
    hp: RegenStatDataDescription
    attack: GrowthStatDataDescription
    defense: GrowthStatDataDescription
    speed: GrowthStatDataDescription
    attack_range: BaseStatDataDescription
    movement_range: BaseStatDataDescription


class SkillsDataDescription(BaseModel):
    passive: str | None = None


class UnitDataDescription(DataDescription):
    identity: UnitIdentityDataDescription
    sprites: SpriteDataDescription
    stats: StatsDataDescription
    skills: SkillsDataDescription
