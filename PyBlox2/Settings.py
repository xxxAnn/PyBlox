def _cool_pop(payload, name):
    return bool(payload.pop(name))

class BloxSettings:
    
    def __init__(self, payload):
        self.is_approval_required = _cool_pop(payload, "isApprovalRequired")
        self.is_builders_club_required = _cool_pop(payload, "isBuildersClubRequired")
        self.are_enemies_allowed = _cool_pop(payload, "areEnemiesAllowed")
        self.are_group_games_visible = _cool_pop(payload, "areGroupGamesVisible")
        self.are_group_funds_visible = _cool_pop(payload, "areGroupFundsVisible")


