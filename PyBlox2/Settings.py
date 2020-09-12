class BloxSettings:
    
    def __init__(self, payload):
        self.is_approval_required = bool(payload.pop("isApprovalRequired"))
        self.is_builders_club_required = bool(payload.pop("isBuildersClubRequired"))
        self.are_enemies_allowed = bool(payload.pop("areEnemiesAllowed"))
        self.are_group_games_visible = bool(payload.pop("areGroupGamesVisible"))
        self.are_group_funds_visible = bool(payload.pop("areGroupFundsVisible"))
