"""Pydantic models matching the exact JSON schema for weekly picks."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class MetaModel(BaseModel):
    """Metadata about the weekly picks."""
    week: int
    date: str
    slate_description: str
    note: str


class SourceModel(BaseModel):
    """Source with sentiment for a player recommendation."""
    name: str
    sentiment: str  # "+1", "0", "-1"


class SuggestionModel(BaseModel):
    """Prop suggestion for a player."""
    stat: str  # e.g., "passing_yards", "rushing_yards", "anytime_td"
    line: Optional[float] = None  # null for yes/no markets like anytime_td
    type: str  # "over_under" or "yes_no"
    lean: str  # "over", "under", "yes", "no"


class PlayerModel(BaseModel):
    """Player with props and recommendations."""
    name: str
    team: str
    position: str  # "QB", "RB", "WR", "TE"
    game: str
    matchup_note: str
    injury_status: str  # "active", "questionable", "out", etc.
    verified: bool
    what_to_target: str
    why: str
    sources: List[SourceModel]
    suggestions: List[SuggestionModel]


class PredictionDetailsModel(BaseModel):
    """Flexible prediction details for long shots."""
    yards: Optional[int] = None
    touchdowns: Optional[int] = None
    receptions: Optional[int] = None
    targets: Optional[int] = None
    carries: Optional[int] = None
    completions: Optional[int] = None
    attempts: Optional[int] = None


class LongShotPredictionModel(BaseModel):
    """Prediction details for a long shot."""
    label: str
    prediction: PredictionDetailsModel
    odds_bucket_estimate: str  # e.g., "+600_to_+1500"


class LongShotPlayerModel(BaseModel):
    """Player with long shot predictions."""
    name: str
    team: str
    position: str
    game: str
    long_shot: LongShotPredictionModel
    ultra_long_shot: LongShotPredictionModel


class LongShotsModel(BaseModel):
    """Container for long shot players."""
    players: List[LongShotPlayerModel]


class CategoriesModel(BaseModel):
    """All player categories."""
    qbs: List[PlayerModel] = Field(default_factory=list)
    rbs: List[PlayerModel] = Field(default_factory=list)
    wrs: List[PlayerModel] = Field(default_factory=list)
    tes: List[PlayerModel] = Field(default_factory=list)


class WeeklyPicksModel(BaseModel):
    """Root model for weekly picks - matches JSON schema exactly."""
    meta: MetaModel
    categories: CategoriesModel
    long_shots: LongShotsModel