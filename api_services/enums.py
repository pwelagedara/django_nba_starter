from enumfields import Enum


class RoleChoice(Enum):
    """Enum for User Role"""

    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    PLAYER = "PLAYER"
    COACH = "COACH"


class TournamentRoundChoice(Enum):
    """Enum for Tournament Rounds"""

    FIRST_ROUND = "FIRST_ROUND"
    QUARTER_FINALS = "QUARTER_FINALS"
    SEMI_FINALS = "SEMI_FINALS"
    FINALS = "FINALS"
