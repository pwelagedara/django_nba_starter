from enumfields import Enum


class RoleChoice(Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    PLAYER = "PLAYER"
    COACH = "COACH"


class TournamentRoundChoice(Enum):
    FIRST_ROUND = "FIRST_ROUND"
    QUARTER_FINALS = "ADMIN"
    SEMI_FINALS = "SEMI_FINALS"
    FINALS = "FINALS"
