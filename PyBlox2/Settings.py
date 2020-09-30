"""
`Settings` is a low level submodule of Groups grouping group settings into one object

Contents:
    `BloxSettings`: No parent -> Deprecated in 1.1

Requires:
    `Base`: `DataContainer`

The following code is provided with 

    The MIT License (MIT)

    Copyright (c) Kyando 2020

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
from .Base import DataContainer

def __cool_pop(payload, name):
    return bool(payload.pop(name))

class BloxSettings:
    """
    Settings for a group object

    Attrs:
        `is_approval_required`
        `is_builders_club_required`
        `are_enemies_allowed`
        `are_group_games_visible`
        `are_group_funds_visible`

    This object will be deprecated in 1.1 in favor of a DataContainer
    """
    def __init__(self, payload):
        self.is_approval_required = __cool_pop(payload, "isApprovalRequired")
        self.is_builders_club_required = __cool_pop(payload, "isBuildersClubRequired")
        self.are_enemies_allowed = __cool_pop(payload, "areEnemiesAllowed")
        self.are_group_games_visible = __cool_pop(payload, "areGroupGamesVisible")
        self.are_group_funds_visible = __cool_pop(payload, "areGroupFundsVisible")

def create_settings(payload):
    """
    Used in 1.1+ to create a settings DataContainer
    """
    settings = DataContainer()

    settings['is_approval_required'] = __cool_pop(payload, "isApprovalRequired")
    settings['is_builders_club_required'] = __cool_pop(payload, "isBuildersClubRequired")
    settings['are_enemies_allowed'] = __cool_pop(payload, "areEnemiesAllowed")
    settings['are_group_games_visible'] = __cool_pop(payload, "areGroupGamesVisible")
    settings['are_group_funds_visible'] = __cool_pop(payload, "areGroupFundsVisible")

    return settings




