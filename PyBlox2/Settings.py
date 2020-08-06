class BloxSettings:
    def __init__(self, payload):
        self.is_approval_required = payload.pop("isApprovalRequired")
        self.is_builders_club_required = payload.pop("isBuildersClubRequired")
        self.are_enemies_allowed = payload.pop("areEnemiesAllowed")
        self.are_group_games_visible = payload.pop("areGroupGamesVisible")
        self.are_group_funds_visible = payload.pop("areGroupFundsVisible")