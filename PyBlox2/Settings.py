"""
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

def _cool_pop(payload, name):
    return bool(payload.pop(name))

class BloxSettings:
    
    def __init__(self, payload):
        self.is_approval_required = _cool_pop(payload, "isApprovalRequired")
        self.is_builders_club_required = _cool_pop(payload, "isBuildersClubRequired")
        self.are_enemies_allowed = _cool_pop(payload, "areEnemiesAllowed")
        self.are_group_games_visible = _cool_pop(payload, "areGroupGamesVisible")
        self.are_group_funds_visible = _cool_pop(payload, "areGroupFundsVisible")


