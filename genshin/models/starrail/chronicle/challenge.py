"""Starrail chronicle challenge."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    import pydantic.v1 as pydantic
else:
    try:
        import pydantic.v1 as pydantic
    except ImportError:
        import pydantic

from genshin.models.model import Aliased, APIModel
from genshin.models.starrail.character import FloorCharacter

from .base import PartialTime

__all__ = [
    "APCShadowBoss",
    "APCShadowFloor",
    "APCShadowFloorNode",
    "APCShadowSeason",
    "ChallengeBuff",
    "FictionFloor",
    "FictionFloorNode",
    "FloorNode",
    "StarRailAPCShadow",
    "StarRailChallenge",
    "StarRailChallengeSeason",
    "StarRailFloor",
    "StarRailPureFiction",
]


class FloorNode(APIModel):
    """Node for a memory of chaos floor."""

    challenge_time: PartialTime
    avatars: List[FloorCharacter]


class StarRailChallengeFloor(APIModel):
    """Base model for star rail challenge floors."""

    id: int = Aliased("maze_id")
    name: str
    star_num: int
    is_quick_clear: bool = Aliased("is_fast")


class StarRailFloor(StarRailChallengeFloor):
    """Floor in a memory of chaos challenge."""

    round_num: int
    is_chaos: bool
    node_1: FloorNode
    node_2: FloorNode


class StarRailChallengeSeason(APIModel):
    """A season of a challenge."""

    id: int = Aliased("schedule_id")
    name: str = Aliased("name_mi18n")
    status: str
    begin_time: PartialTime
    end_time: PartialTime


class StarRailChallenge(APIModel):
    """Memory of chaos challenge in a season."""

    season: int = Aliased("schedule_id")
    begin_time: PartialTime
    end_time: PartialTime

    total_stars: int = Aliased("star_num")
    max_floor: str
    total_battles: int = Aliased("battle_num")
    has_data: bool

    floors: List[StarRailFloor] = Aliased("all_floor_detail")


class ChallengeBuff(APIModel):
    """Buff used in a pure fiction or apocalyptic shadow node."""

    id: int
    name: str = Aliased("name_mi18n")
    description: str = Aliased("desc_mi18n")
    icon: str


class FictionFloorNode(FloorNode):
    """Node for a Pure Fiction floor."""

    buff: Optional[ChallengeBuff]
    score: int


class FictionFloor(StarRailChallengeFloor):
    """Floor in a Pure Fiction challenge."""

    round_num: int
    node_1: FictionFloorNode
    node_2: FictionFloorNode

    @property
    def score(self) -> int:
        """Total score of the floor."""
        return self.node_1.score + self.node_2.score


class StarRailPureFiction(APIModel):
    """Pure Fiction challenge in a season."""

    name: str
    season_id: int
    begin_time: PartialTime
    end_time: PartialTime

    total_stars: int = Aliased("star_num")
    max_floor: str
    total_battles: int = Aliased("battle_num")
    has_data: bool

    floors: List[FictionFloor] = Aliased("all_floor_detail")
    max_floor_id: int


class APCShadowFloorNode(FloorNode):
    """Node for a apocalyptic shadow floor."""

    challenge_time: Optional[PartialTime]
    buff: Optional[ChallengeBuff]
    score: int
    boss_defeated: bool

    @property
    def has_data(self) -> bool:
        """Check if the node has data."""
        return bool(self.avatars)


class APCShadowFloor(StarRailChallengeFloor):
    """Floor in an apocalyptic shadow challenge."""

    node_1: APCShadowFloorNode
    node_2: APCShadowFloorNode
    last_update_time: PartialTime

    @property
    def score(self) -> int:
        """Total score of the floor."""
        return self.node_1.score + self.node_2.score


class APCShadowBoss(APIModel):
    """Boss in an apocalyptic shadow challenge."""

    id: int
    name_mi18n: str
    icon: str


class APCShadowSeason(StarRailChallengeSeason):
    """Season of an apocalyptic shadow challenge."""

    upper_boss: APCShadowBoss
    lower_boss: APCShadowBoss


class StarRailAPCShadow(APIModel):
    """Apocalyptic shadow challenge in a season."""

    total_stars: int = Aliased("star_num")
    max_floor: str
    total_battles: int = Aliased("battle_num")
    has_data: bool

    floors: List[APCShadowFloor] = Aliased("all_floor_detail")
    seasons: List[APCShadowSeason] = Aliased("groups")
    max_floor_id: int
