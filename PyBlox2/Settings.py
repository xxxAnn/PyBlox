from .Base import DataContainer

def _cool_pop(payload, name):
    return bool(payload.pop(name))

class BloxSettings:
    """
    Settings for a group object
    
    .. warning::
        This object is legacy

    Attributes
    -----------
    is_approval_required
    is_builders_club_required
    are_enemies_allowed
    are_group_games_visible
    are_group_funds_visible

    """
    def __init__(self, payload):
        self.is_approval_required = _cool_pop(payload, "isApprovalRequired")
        self.is_builders_club_required = _cool_pop(payload, "isBuildersClubRequired")
        self.are_enemies_allowed = _cool_pop(payload, "areEnemiesAllowed")
        self.are_group_games_visible = _cool_pop(payload, "areGroupGamesVisible")
        self.are_group_funds_visible = _cool_pop(payload, "areGroupFundsVisible")

def create_settings(payload):
    """
    .. versionadded::
        1.1

    Creates a DataContainer with all the settingsg
    Returns
    -------
    :class:`PyBlox2.Base.DataContainer`
        A DataContainer object, its object can be accessed through indexed or in the normal object notation
        This DataContainer has all the roblox group settings in camel_case notation
    """
    settings = DataContainer()

    settings['is_approval_required'] = _cool_pop(payload, "isApprovalRequired")
    settings['is_builders_club_required'] = _cool_pop(payload, "isBuildersClubRequired")
    settings['are_enemies_allowed'] = _cool_pop(payload, "areEnemiesAllowed")
    settings['are_group_games_visible'] = _cool_pop(payload, "areGroupGamesVisible")
    settings['are_group_funds_visible'] = _cool_pop(payload, "areGroupFundsVisible")

    return settings




