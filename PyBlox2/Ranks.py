"""
`Ranks` is a submodule of Groups it manages the `roleSet` within the groups API

Contents:
    `BloxRank`: `BloxType`

Requires:
    `Errors`: `Module.*`
    `Base`: `BloxType`
    `.utils`: `Url`

The following code is provided through 

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

import json

from .Errors import *
from .Base import BloxType
from .utils import Url

class BloxRank(BloxType):
    """
    A rank object used to modify a user's rank 
    or modify the name, rank or description of a rank

    Attrs:
        `name`
        `id`
        `rank`
        `member_count`
        `group`: BloxGroup
        `description`
    
    Fetchables:
        `members`: List(Member.BloxMember)

    Meths:
        async `fetch`: 
    
    Examples:

        >> developers = await rank.fetch("members") # where `rank` is a group's developer rank

    Users *will* be fetched through cache when using async meth `fetch`
    """
    def __init__(self, payload, group):
        super().__init__(group.client)
        self.name = payload.pop("name")
        self.id = payload.pop("id")
        self.rank = payload.pop("rank")
        self.member_count = payload.pop("memberCount")
        self.description = payload.pop("description")
        self.group = group
        self.can_fetch("members")

    async def fetch_members(self):
        role_id = self.id
        access = Url("groups", "/v1/groups/%group_id%/roles/%id%/users", group_id=self.group.id, id=self.id)
        members_list = []
        hook = await access.get()
        iterable = hook.json["data"]

        result = await self.group._cvrt_dict_blox_member(self, iterable)

        if result == None:
            raise PyBloxException(
                "Could not find members"
                )
        
        return result
