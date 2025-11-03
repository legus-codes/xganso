from pydantic import BaseModel


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


class DataDescription(BaseModel):
    id: str


class UnitDataDescription(DataDescription):
    name: str
    unit_class: str
    sprites: SpriteDataDescription
    stats: StatsDataDescription
    passive: str | None = None
